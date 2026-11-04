import 'package:test/test.dart';
import 'package:golden_reference_engines/golden_reference_engines.dart';

void main() {
  group('P1/P2 smoothing kNN and logistic', () {
    test('EWMA preserves constant series and limits single-spike jump', () {
      expect(LocalPredictionReference.ewma([5, 5, 5]), [5, 5, 5]);
      expect(LocalPredictionReference.ewma([10, 10, 30], alpha: 0.2),
          [10, 10, closeTo(14, 1e-9)]);
    });

    test('Holt extends linear series and Winters handles seasonality', () {
      final holt = LocalPredictionReference.holt([10, 12, 14, 16, 18],
          alpha: 0.5, beta: 0.5, horizon: 2);
      expect(holt[0], closeTo(20, 1e-9));
      expect(holt[1], closeTo(22, 1e-9));
      final winter = LocalPredictionReference.holtWinters(
        [10, 20, 10, 20, 10, 20, 10, 20], seasonLength: 2, horizon: 2);
      expect(winter.length, 2);
      expect(winter.every((v) => v.isFinite), isTrue);
      expect(winter[1], greaterThan(winter[0]));
    });

    test('KNN uses authorized rows, normalized features and stable ties', () {
      final found = LocalPredictionReference.kNearest(
        query: [0, 0], k: 2,
        authorizedRows: const [
          MlVectorRow(id: 'b', features: [1, 0]),
          MlVectorRow(id: 'a', features: [-1, 0]),
          MlVectorRow(id: 'secret', features: [0, 0], visible: false),
          MlVectorRow(id: 'trash', features: [0, 0], deleted: true),
          MlVectorRow(id: 'far', features: [20, 20]),
        ],
      );
      expect(found.map((e) => e.id), ['a', 'b']);
      expect(found.every((e) => e.distance == 1), isTrue);
    });

    test('logistic training learns separable labels but not calibrated risk', () {
      final observations = <List<double>>[
        for (var i = -10; i < 0; i++) [i / 10.0],
        for (var i = 1; i <= 10; i++) [i / 10.0],
      ];
      final outcomes = <int>[...List.filled(10, 0), ...List.filled(10, 1)];
      final model = LocalPredictionReference.trainLogistic(
        observations: observations, outcomes: outcomes);
      expect(model.predictProbability([0.9]),
          greaterThan(model.predictProbability([-0.9])));
      expect(model.predictProbability([0.9]), greaterThan(0.5));
      expect(model.predictProbability([-0.9]), lessThan(0.5));
    });

    test('refuses invalid config rather than silently inferring', () {
      expect(() => LocalPredictionReference.ewma([0, 1],
          alpha: double.nan), throwsA(isA<OnDeviceMathError>()));
      expect(() => LocalPredictionReference.holt([1, 2]),
          throwsA(isA<OnDeviceMathError>()));
      expect(() => LocalPredictionReference.holtWinters(
          [1, 2, 3, 4], seasonLength: 2),
          throwsA(isA<OnDeviceMathError>()));
      expect(() => LocalPredictionReference.kNearest(
        query: [0], authorizedRows: const [
          MlVectorRow(id: 'dup', features: [0]),
          MlVectorRow(id: 'dup', features: [1]),
        ]),
        throwsA(isA<OnDeviceMathError>()));
      expect(() => LocalPredictionReference.trainLogistic(
        observations: List.filled(10, [0.0]),
        outcomes: List.filled(10, 1)), throwsA(isA<OnDeviceMathError>()));
    });
  });

  group('P3 anomaly and temporal sequence references', () {
    final sample = const <MlVectorRow>[
      MlVectorRow(id: 'a', features: [0]),
      MlVectorRow(id: 'b', features: [0.1]),
      MlVectorRow(id: 'c', features: [0.2]),
      MlVectorRow(id: 'd', features: [0.3]),
      MlVectorRow(id: 'outlier', features: [12]),
    ];

    test('LOF assigns higher density anomaly to a separated sample', () {
      final ranked = LocalPatternReference.localOutlierFactor(sample, k: 2);
      final outlier = ranked.singleWhere((e) => e.id == 'outlier').score;
      final typical = ranked.singleWhere((e) => e.id == 'b').score;
      expect(outlier, greaterThan(typical));
    });

    test('Isolation Forest is seeded, bounded and deterministic', () {
      final a = LocalPatternReference.isolationForest(sample, trees: 8);
      final b = LocalPatternReference.isolationForest(sample.reversed, trees: 8);
      expect(a.map((x) => x.id), b.map((x) => x.id));
      for (var i = 0; i < a.length; i++) {
        expect(a[i].score, closeTo(b[i].score, 1e-12));
        expect(a[i].score, inInclusiveRange(0, 1));
      }
      expect(LocalPatternReference.isolationForest(sample.take(2)), isEmpty);
    });

    test('HMM Viterbi recovers sequence for labeled emission tables', () {
      final states = LocalPatternReference.hmmViterbi(
        initial: [0.5, 0.5],
        transitions: [[0.9, 0.1], [0.1, 0.9]],
        emissions: [[0.9, 0.1], [0.1, 0.9]],
        observations: [0, 0, 1, 1],
      );
      expect(states, [0, 0, 1, 1]);
      expect(LocalPatternReference.hmmViterbi(
        initial: [0.5, 0.5],
        transitions: [[0.9, 0.1], [0.1, 0.9]],
        emissions: [[0.9, 0.1], [0.1, 0.9]],
        observations: [],
      ), isEmpty);
    });

    test('HAC average-link produces stable small-group dendrogram cut', () {
      const rows = <MlVectorRow>[
        MlVectorRow(id: 'd', features: [10]),
        MlVectorRow(id: 'b', features: [0.1]),
        MlVectorRow(id: 'c', features: [10.1]),
        MlVectorRow(id: 'a', features: [0]),
      ];
      final clusters = LocalPatternReference.agglomerativeAverageLinkage(
        authorizedRows: rows, targetClusters: 2,
      );
      expect(clusters, [
        ['a', 'b'],
        ['c', 'd'],
      ]);
    });

    test('rejects invalid HMM, LOF, HAC and numeric observations', () {
      expect(() => LocalPatternReference.localOutlierFactor(sample, k: 0),
          throwsA(isA<OnDeviceMathError>()));
      expect(() => LocalPatternReference.hmmViterbi(
        initial: [0.6, 0.6],
        transitions: [[0.9, 0.1], [0.1, 0.9]],
        emissions: [[0.9, 0.1], [0.1, 0.9]],
        observations: [0],
      ), throwsA(isA<OnDeviceMathError>()));
      expect(() => LocalPatternReference.agglomerativeAverageLinkage(
        authorizedRows: sample, targetClusters: 6,
      ), throwsA(isA<OnDeviceMathError>()));
      expect(() => LocalPatternReference.isolationForest([
        const MlVectorRow(id: 'bad', features: [double.nan]),
      ]), throwsA(isA<OnDeviceMathError>()));
    });
  });

  group('P3 PCA/SVD bounded low rank projections', () {
    final observations = <List<double>>[
      [1, 1], [2, 2], [3, 3], [4, 4],
    ];

    test('centered PCA yields zero-centered one-axis projection', () {
      final projection = LocalProjectionReference.project(
        observations, count: 1);
      expect(projection.mean, [2.5, 2.5]);
      expect(projection.components.length, 1);
      expect(projection.projected.length, 4);
      expect(projection.projected.map((e) => e.first)
          .reduce((a, b) => a + b), closeTo(0, 1e-9));
    });

    test('uncentered TruncatedSVD proxy leaves mean at zero', () {
      final projection = LocalProjectionReference.project(
        observations, count: 1, center: false);
      expect(projection.mean, [0, 0]);
      expect(projection.projected.every((r) =>
          r.length == 1 && r.first.isFinite), isTrue);
    });

    test('rejects too few rows and mismatching feature dimensions', () {
      expect(() => LocalProjectionReference.project(
        [[1, 2], [3, 4]], count: 1),
        throwsA(isA<OnDeviceMathError>()));
      expect(() => LocalProjectionReference.project(
        [[1, 2], [3], [4, 5]], count: 1),
        throwsA(isA<OnDeviceMathError>()));
    });
  });
}
