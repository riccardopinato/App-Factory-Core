import 'package:test/test.dart';
import 'package:golden_reference_engines/golden_reference_engines.dart';

void main() {
  group('local deterministic MinHash/LSH', () {
    test('same normalized text gives exact Jaccard and stable IDs', () {
      final hits = LocalMinHashLshReference.suggest(
        query: 'Caffè in camper vicino al lago',
        authorizedCandidates: [
          const LocalDuplicateDocument(
            id: 'z', text: 'caffè in CAMPER vicino al lago'),
          const LocalDuplicateDocument(
            id: 'a', text: 'Caffè in camper vicino al lago'),
          const LocalDuplicateDocument(
            id: 'x', text: 'guida navigazione per il mare'),
        ],
      );
      expect(hits.map((e) => e.id), ['a', 'z']);
      expect(hits.every((e) => e.jaccard == 1), isTrue);
      expect(hits.every((e) => e.matchingBands == 16), isTrue);
    });

    test('filters hidden and trashed documents before producing suggestions', () {
      final hits = LocalMinHashLshReference.suggest(
        query: 'nota riunione progetto studio',
        authorizedCandidates: [
          const LocalDuplicateDocument(
              id: 'hidden', text: 'nota riunione progetto studio',
              visible: false),
          const LocalDuplicateDocument(
              id: 'trash', text: 'nota riunione progetto studio',
              deleted: true),
          const LocalDuplicateDocument(
              id: 'public', text: 'nota riunione progetto studio'),
        ],
      );
      expect(hits.map((e) => e.id), ['public']);
    });

    test('rejects duplicate ID, unbounded input and invalid thresholds', () {
      expect(() => LocalMinHashLshReference.suggest(
        query: 'testo abbastanza lungo',
        authorizedCandidates: [
          const LocalDuplicateDocument(id: 'a', text: 'testo abbastanza lungo'),
          const LocalDuplicateDocument(id: 'a', text: 'testo abbastanza lungo'),
        ],
      ), throwsA(isA<OnDeviceMathError>()));
      expect(() => LocalMinHashLshReference.suggest(
        query: 'testo abbastanza lungo',
        authorizedCandidates: [
          const LocalDuplicateDocument(id: 'a', text: 'testo abbastanza lungo'),
          const LocalDuplicateDocument(id: 'b', text: 'testo abbastanza lungo'),
        ], maxCandidates: 1,
      ), throwsA(isA<OnDeviceMathError>()));
      expect(() => LocalMinHashLshReference.suggest(
        query: 'testo abbastanza lungo',
        authorizedCandidates: const [],
        minimumJaccard: double.nan,
      ), throwsA(isA<OnDeviceMathError>()));
      expect(() => LocalMinHashLshReference.shingles(List.filled(4001, 'x').join()),
          throwsA(isA<OnDeviceMathError>()));
    });

    test('empty and short text abstain, do not imply duplicates', () {
      expect(LocalMinHashLshReference.suggest(
        query: 'solo',
        authorizedCandidates: const [
          LocalDuplicateDocument(id: 'a', text: 'solo'),
        ],
      ), isEmpty);
      expect(LocalMinHashLshReference.shingles('a'), isEmpty);
    });
  });

  group('local Multinomial Naive Bayes reference', () {
    final training = <LocalLabeledText>[
      const LocalLabeledText(
        id: 's1', label: 'studio', text: 'esame lezione ripasso'),
      const LocalLabeledText(
        id: 's2', label: 'studio', text: 'esame corso studio'),
      const LocalLabeledText(
        id: 'w1', label: 'lavoro', text: 'fattura preventivo acquisti'),
      const LocalLabeledText(
        id: 'w2', label: 'lavoro', text: 'fattura ordine magazzino'),
      const LocalLabeledText(
        id: 'hidden', label: 'salute', text: 'esame lezione',
        visible: false),
    ];

    test('selects explicitly trained categories with uncalibrated margin', () {
      final result = LocalNaiveBayesReference.classify(
        document: 'esame lezione',
        authorizedTrainingRows: training,
      );
      expect(result, isNotNull);
      expect(result!.label, 'studio');
      expect(result.logScoreMargin, greaterThan(0));
      expect(result.evidenceTokens, 2);
      expect(result.trainingRows, 4);
    });

    test('abstains for unseen terms and insufficient training', () {
      expect(LocalNaiveBayesReference.classify(
        document: 'astronave vulcano',
        authorizedTrainingRows: training,
      ), isNull);
      expect(LocalNaiveBayesReference.classify(
        document: 'esame',
        authorizedTrainingRows: training.take(3),
      ), isNull);
      expect(LocalNaiveBayesReference.classify(
        document: '',
        authorizedTrainingRows: training,
      ), isNull);
    });

    test('rejects invalid IDs, config and oversized documents', () {
      expect(() => LocalNaiveBayesReference.classify(
        document: 'esame',
        authorizedTrainingRows: [
          training.first,
          training.first,
        ],
      ), throwsA(isA<OnDeviceMathError>()));
      expect(() => LocalNaiveBayesReference.classify(
        document: 'esame',
        authorizedTrainingRows: training,
        maxTrainingRows: 3,
      ), throwsA(isA<OnDeviceMathError>()));
      expect(() => LocalNaiveBayesReference.classify(
        document: List.filled(4001, 'x').join(),
        authorizedTrainingRows: training,
      ), throwsA(isA<OnDeviceMathError>()));
    });
  });
}
