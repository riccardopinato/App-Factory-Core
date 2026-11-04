/// Experimental, bounded *reference only* anomaly/sequence/clustering math.
/// Not a production detector, diagnosis, sensor permission or model package.
library;

import 'dart:math' as math;

import 'lightweight_ml_p1_p2.dart';
import 'on_device_algorithms.dart';

final class MlAnomalyScore {
  const MlAnomalyScore(this.id, this.score);
  final String id;
  /// LOF around 1 is locally typical; IF closer to 1 is more isolated.
  final double score;
}

abstract final class LocalPatternReference {
  static List<MlVectorRow> _validRows(
    Iterable<MlVectorRow> source, {
    int max = 128,
    int dimensions = 16,
  }) {
    final rows = <MlVectorRow>[];
    final seen = <String>{};
    var count = 0;
    var dimension = -1;
    for (final row in source) {
      if (++count > max) throw const OnDeviceMathError('UNBOUNDED_PATTERN_ROWS');
      if (row.id.trim().isEmpty || !seen.add(row.id)) {
        throw const OnDeviceMathError('INVALID_PATTERN_ID');
      }
      if (!row.visible || row.deleted) continue;
      if (dimension < 0) dimension = row.features.length;
      if (dimension < 1 || dimension > dimensions ||
          row.features.length != dimension ||
          row.features.any((x) => !x.isFinite || x.abs() > 1e6)) {
        throw const OnDeviceMathError('INVALID_PATTERN_FEATURES');
      }
      rows.add(row);
    }
    rows.sort((a, b) => a.id.compareTo(b.id));
    return rows;
  }

  static double _distance(List<double> a, List<double> b) {
    var sum = 0.0;
    for (var i = 0; i < a.length; i++) {
      final delta = a[i] - b[i];
      sum += delta * delta;
    }
    return math.sqrt(sum);
  }

  /// Deterministic LOF over a tiny authorized numeric snapshot; O(N²).
  /// This is outlier scoring of a fixed cohort, NOT LOF novelty scoring.
  static List<MlAnomalyScore> localOutlierFactor(
    Iterable<MlVectorRow> authorizedRows, {
    int k = 3,
  }) {
    final rows = _validRows(authorizedRows, max: 100);
    final n = rows.length;
    if (k < 2 || k > 20) throw const OnDeviceMathError('INVALID_LOF_K');
    if (n <= k) return const [];
    final dist = List.generate(n, (_) => List<double>.filled(n, 0));
    for (var i = 0; i < n; i++) {
      for (var j = i + 1; j < n; j++) {
        final d = _distance(rows[i].features, rows[j].features);
        dist[i][j] = d;
        dist[j][i] = d;
      }
    }
    final nearest = <List<int>>[];
    final kd = <double>[];
    for (var i = 0; i < n; i++) {
      final idx = <int>[for (var j = 0; j < n; j++) if (j != i) j];
      idx.sort((a, b) {
        final c = dist[i][a].compareTo(dist[i][b]);
        return c != 0 ? c : rows[a].id.compareTo(rows[b].id);
      });
      nearest.add(idx.take(k).toList());
      kd.add(dist[i][idx[k - 1]]);
    }
    final density = List<double>.filled(n, 0);
    for (var i = 0; i < n; i++) {
      var reach = 0.0;
      for (final j in nearest[i]) {
        reach += math.max(kd[j], dist[i][j]);
      }
      density[i] = 1 / math.max(reach / k, 1e-9);
    }
    return List.unmodifiable(List.generate(n, (i) {
      var ratio = 0.0;
      for (final j in nearest[i]) {
        ratio += density[j] / density[i];
      }
      return MlAnomalyScore(rows[i].id, ratio / k);
    }));
  }

  static double _pathLength(
    List<MlVectorRow> rows,
    List<double> target,
    math.Random random,
    int depth,
    int maxDepth,
  ) {
    if (rows.length <= 1) return depth.toDouble();
    if (depth >= maxDepth) return depth + _expectedPath(rows.length);
    final features = <int>[];
    for (var f = 0; f < target.length; f++) {
      final minV = rows.map((r) => r.features[f]).reduce(math.min);
      final maxV = rows.map((r) => r.features[f]).reduce(math.max);
      if (maxV > minV) features.add(f);
    }
    if (features.isEmpty) return depth + _expectedPath(rows.length);
    final feature = features[random.nextInt(features.length)];
    final minV = rows.map((r) => r.features[feature]).reduce(math.min);
    final maxV = rows.map((r) => r.features[feature]).reduce(math.max);
    final pivot = minV + random.nextDouble() * (maxV - minV);
    final left = rows.where((r) => r.features[feature] < pivot).toList();
    final right = rows.where((r) => r.features[feature] >= pivot).toList();
    if (left.isEmpty || right.isEmpty) {
      return depth + _expectedPath(rows.length);
    }
    return _pathLength(target[feature] < pivot ? left : right,
        target, random, depth + 1, maxDepth);
  }

  static double _expectedPath(int size) {
    if (size <= 1) return 0;
    if (size == 2) return 1;
    // harmonic approximation, sufficient for a bounded candidate reference.
    return 2 * (math.log(size - 1) + 0.5772156649) -
        2 * (size - 1) / size;
  }

  /// Small, seeded, no-external-weights Isolation Forest path-score proxy.
  /// Rebuilds random partitions per item; not a fitted/persisted production model.
  static List<MlAnomalyScore> isolationForest(
    Iterable<MlVectorRow> authorizedRows, {
    int trees = 24,
    int maxDepth = 8,
    int seed = 7,
  }) {
    final rows = _validRows(authorizedRows);
    if (trees < 4 || trees > 64 || maxDepth < 2 || maxDepth > 16) {
      throw const OnDeviceMathError('INVALID_ISOLATION_CONFIG');
    }
    if (rows.length < 4) return const [];
    final scale = _expectedPath(rows.length);
    return List.unmodifiable(rows.map((row) {
      var total = 0.0;
      for (var i = 0; i < trees; i++) {
        total += _pathLength(rows, row.features,
            math.Random(seed + i * 104729), 0, maxDepth);
      }
      return MlAnomalyScore(row.id, math.pow(2, -total / trees / scale).toDouble());
    }));
  }

  static void _probabilities(List<double> probabilities) {
    if (probabilities.isEmpty || probabilities.any((p) =>
        !p.isFinite || p < 0 || p > 1) ||
        (probabilities.reduce((a, b) => a + b) - 1).abs() > 1e-6) {
      throw const OnDeviceMathError('INVALID_HMM_DISTRIBUTION');
    }
  }

  /// Pure Viterbi over already-discretized observations.
  /// The user/app must supply independently trained transition/emission tables.
  static List<int> hmmViterbi({
    required List<double> initial,
    required List<List<double>> transitions,
    required List<List<double>> emissions,
    required List<int> observations,
  }) {
    final states = initial.length;
    if (states < 2 || states > 12 || observations.length > 1000 ||
        transitions.length != states || emissions.length != states) {
      throw const OnDeviceMathError('INVALID_HMM_CONFIG');
    }
    _probabilities(initial);
    final symbols = emissions.first.length;
    if (symbols < 2 || symbols > 32 ||
        transitions.any((row) => row.length != states) ||
        emissions.any((row) => row.length != symbols) ||
        observations.any((o) => o < 0 || o >= symbols)) {
      throw const OnDeviceMathError('INVALID_HMM_SHAPE');
    }
    for (final row in [...transitions, ...emissions]) {
      _probabilities(row);
    }
    if (observations.isEmpty) return const [];
    double logProb(double value) => value == 0 ? double.negativeInfinity : math.log(value);
    var previous = List.generate(states, (s) =>
        logProb(initial[s]) + logProb(emissions[s][observations.first]));
    final backtrace = <List<int>>[];
    for (final observed in observations.skip(1)) {
      final current = List<double>.filled(states, double.negativeInfinity);
      final prevState = List<int>.filled(states, 0);
      for (var target = 0; target < states; target++) {
        for (var from = 0; from < states; from++) {
          final candidate = previous[from] + logProb(transitions[from][target]);
          if (candidate > current[target]) {
            current[target] = candidate;
            prevState[target] = from;
          }
        }
        current[target] += logProb(emissions[target][observed]);
      }
      previous = current;
      backtrace.add(prevState);
    }
    var best = 0;
    for (var s = 1; s < states; s++) {
      if (previous[s] > previous[best]) best = s;
    }
    if (previous[best] == double.negativeInfinity) return const [];
    final path = List<int>.filled(observations.length, 0);
    path[path.length - 1] = best;
    for (var t = path.length - 2; t >= 0; t--) {
      path[t] = backtrace[t][path[t + 1]];
    }
    return List.unmodifiable(path);
  }

  /// O(N³+) average-linkage HAC on <=80 items; not appropriate for 10k POIs.
  static List<List<String>> agglomerativeAverageLinkage({
    required Iterable<MlVectorRow> authorizedRows,
    required int targetClusters,
  }) {
    final rows = _validRows(authorizedRows, max: 80, dimensions: 12);
    if (rows.isEmpty || targetClusters < 1 || targetClusters > rows.length) {
      throw const OnDeviceMathError('INVALID_HAC_CONFIG');
    }
    final original = <String, MlVectorRow>{for (final r in rows) r.id: r};
    final clusters = <List<String>>[
      for (final row in rows) [row.id],
    ];
    double averageDistance(List<String> a, List<String> b) {
      var sum = 0.0;
      for (final x in a) {
        for (final y in b) {
          sum += _distance(original[x]!.features, original[y]!.features);
        }
      }
      return sum / (a.length * b.length);
    }
    while (clusters.length > targetClusters) {
      var bestI = 0;
      var bestJ = 1;
      var bestDistance = double.infinity;
      for (var i = 0; i < clusters.length; i++) {
        for (var j = i + 1; j < clusters.length; j++) {
          final distance = averageDistance(clusters[i], clusters[j]);
          if (distance < bestDistance) {
            bestDistance = distance;
            bestI = i;
            bestJ = j;
          }
        }
      }
      final merged = [...clusters[bestI], ...clusters[bestJ]]..sort();
      clusters.removeAt(bestJ);
      clusters.removeAt(bestI);
      clusters.add(merged);
      clusters.sort((a, b) => a.first.compareTo(b.first));
    }
    return List.unmodifiable(clusters.map((row) => List<String>.unmodifiable(row)));
  }
}

final class MlProjection {
  const MlProjection(this.mean, this.components, this.projected);
  final List<double> mean;
  final List<List<double>> components;
  final List<List<double>> projected;
}

/// PCA-style centered projection or TruncatedSVD-style uncentered projection.
/// Fixed-iteration covariance/Gram power method, <=24 dims; NOT a full SVD.
abstract final class LocalProjectionReference {
  static MlProjection project(
    List<List<double>> rows, {
    bool center = true,
    int count = 2,
  }) {
    if (rows.length < 3 || rows.length > 400 ||
        rows.first.length < 2 || rows.first.length > 24 ||
        count < 1 || count > 3) {
      throw const OnDeviceMathError('INVALID_PROJECTION_CONFIG');
    }
    final d = rows.first.length;
    if (count > d || rows.any((row) =>
        row.length != d || row.any((v) => !v.isFinite || v.abs() > 1e6))) {
      throw const OnDeviceMathError('INVALID_PROJECTION_DATA');
    }
    final mean = List<double>.filled(d, 0);
    if (center) {
      for (final row in rows) {
        for (var col = 0; col < d; col++) {
          mean[col] += row[col] / rows.length;
        }
      }
    }
    final gram = List.generate(d, (_) => List<double>.filled(d, 0));
    for (final row in rows) {
      for (var i = 0; i < d; i++) {
        for (var j = 0; j < d; j++) {
          gram[i][j] +=
              (row[i] - mean[i]) * (row[j] - mean[j]) / rows.length;
        }
      }
    }
    double dot(List<double> a, List<double> b) {
      var result = 0.0;
      for (var i = 0; i < d; i++) {
        result += a[i] * b[i];
      }
      return result;
    }
    List<double> multiply(List<double> vector) =>
        List.generate(d, (i) => dot(gram[i], vector));
    final components = <List<double>>[];
    for (var component = 0; component < count; component++) {
      List<double> vector = List.generate(d,
          (i) => 1 / (i + component + 1.15));
      for (var step = 0; step < 80; step++) {
        final next = multiply(vector);
        for (final previous in components) {
          final projection = dot(next, previous);
          for (var i = 0; i < d; i++) {
            next[i] -= projection * previous[i];
          }
        }
        final norm = math.sqrt(dot(next, next));
        if (norm < 1e-12 || !norm.isFinite) {
          vector = [];
          break;
        }
        vector = [for (final x in next) x / norm];
      }
      if (vector.isEmpty) break;
      final firstSignificant = vector.firstWhere(
        (x) => x.abs() > 1e-10, orElse: () => 0,
      );
      if (firstSignificant < 0) vector = [for (final x in vector) -x];
      components.add(List.unmodifiable(vector));
    }
    final projected = <List<double>>[
      for (final row in rows)
        [for (final axis in components)
          dot([for (var i = 0; i < d; i++) row[i] - mean[i]], axis)],
    ];
    return MlProjection(
      List.unmodifiable(mean),
      List.unmodifiable(components),
      List.unmodifiable(projected.map((r) => List<double>.unmodifiable(r))),
    );
  }
}
