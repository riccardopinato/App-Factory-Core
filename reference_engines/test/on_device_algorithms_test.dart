import 'package:test/test.dart';
import 'package:golden_reference_engines/golden_reference_engines.dart';

void main() {
  group('bounded fuzzy search', () {
    test('Unicode tokens, typo and exact match with stable ID tie break', () {
      final hits = LocalFuzzyReference.search('riunone', [
        const LocalTextCandidate(id: 'c', text: 'Oggi: riunione alle 15'),
        const LocalTextCandidate(id: 'a', text: 'riunione con Carlo'),
        const LocalTextCandidate(id: 'b', text: 'pranzo'),
      ]);
      expect(hits.map((h) => h.candidate.id), ['a', 'c']);
      expect(hits.every((h) => h.distance == 1), isTrue);
      expect(LocalFuzzyReference.distance('caffè', 'caffè'), 0);
    });

    test('hidden and deleted sources do not leak', () {
      final hits = LocalFuzzyReference.search('segreto', [
        const LocalTextCandidate(id: 'private', text: 'segreto', visible: false),
        const LocalTextCandidate(id: 'trash', text: 'segreto', deleted: true),
        const LocalTextCandidate(id: 'public', text: 'segreto'),
      ]);
      expect(hits.map((h) => h.candidate.id), ['public']);
    });

    test('refuses duplicate IDs, oversize and unbounded scans', () {
      expect(
        () => LocalFuzzyReference.search('test', [
          const LocalTextCandidate(id: 'a', text: 'test'),
          const LocalTextCandidate(id: 'a', text: 'test'),
        ]), throwsA(isA<OnDeviceMathError>()),
      );
      expect(
        () => LocalFuzzyReference.search('test', [
          const LocalTextCandidate(id: 'a', text: 'test'),
          const LocalTextCandidate(id: 'b', text: 'test'),
        ], maxCandidates: 1), throwsA(isA<OnDeviceMathError>()),
      );
    });

    test('distance cutoff is bounded and deterministic', () {
      expect(LocalFuzzyReference.distance('casa', 'caso', cutoff: 2), 1);
      expect(LocalFuzzyReference.distance('abc', 'xyz', cutoff: 1), 2);
      expect(LocalFuzzyReference.distance('', '', cutoff: 0), 0);
    });
  });

  group('local TF-IDF keywords', () {
    test('returns existing tokens and bounded comparable scores', () {
      final keywords = LocalTfidfReference.keywords(
        document: 'camper camper batteria',
        visibleCorpus: ['camper luci', 'batteria casa', 'ricetta'],
      );
      expect(keywords.map((e) => e.term), ['camper', 'batteria']);
      expect(keywords.every((e) => e.score.isFinite), isTrue);
      expect(keywords.first.score, greaterThan(keywords.last.score));
    });

    test('Unicode tokenizer, custom stopwords, empty and zero corpus', () {
      final tokens = LocalTfidfReference.tokenize(
        'Caffè déjà oggi', stopwords: {'oggi'},
      );
      expect(tokens, ['caffè', 'déjà']);
      expect(
        LocalTfidfReference.keywords(
          document: 'notes', visibleCorpus: [],
        ), isEmpty,
      );
    });

    test('rejects oversized corpus while leaving input untouched', () {
      expect(
        () => LocalTfidfReference.keywords(
          document: 'uno', visibleCorpus: List.filled(5001, 'uno'),
        ), throwsA(isA<OnDeviceMathError>()),
      );
    });
  });

  group('EWMA adaptive threshold', () {
    test('needs consecutive high samples and hysteresis to reset', () {
      var s = const LocalSignalState(baseline: 10);
      s = LocalAdaptiveSignalReference.step(state: s, sample: 11);
      expect(s.triggered, isFalse);
      s = LocalAdaptiveSignalReference.step(state: s, sample: 25);
      expect(s.triggered, isFalse);
      s = LocalAdaptiveSignalReference.step(state: s, sample: 24);
      expect(s.triggered, isTrue);
      s = LocalAdaptiveSignalReference.step(state: s, sample: 20);
      expect(s.triggered, isTrue);
      s = LocalAdaptiveSignalReference.step(state: s, sample: 10);
      expect(s.triggered, isTrue);
      s = LocalAdaptiveSignalReference.step(state: s, sample: 10);
      expect(s.triggered, isFalse);
    });

    test('rejects bad sensor configuration and nonfinite input', () {
      expect(
        () => LocalAdaptiveSignalReference.step(
          state: const LocalSignalState(baseline: 0), sample: double.nan,
        ), throwsA(isA<OnDeviceMathError>()),
      );
      expect(
        () => LocalAdaptiveSignalReference.step(
          state: const LocalSignalState(baseline: 0),
          sample: 4, enterDelta: 2, exitDelta: 3,
        ), throwsA(isA<OnDeviceMathError>()),
      );
    });
  });
}
