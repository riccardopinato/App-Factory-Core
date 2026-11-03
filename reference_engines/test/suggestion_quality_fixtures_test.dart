import 'package:golden_reference_engines/golden_reference_engines.dart';
import 'package:test/test.dart';

void main() {
  test('Italian context fixture yields inspectable relevance metrics', () {
    final result = SuggestionQualityFixtures.evaluate(
      ranking: ['progetto-foto', 'nota-ricetta', 'task-studio'],
      relevantIds: {'progetto-foto', 'task-studio'},
      forbiddenIds: {'vault-personale'},
      k: 3,
    );
    expect(result.precisionAtK, closeTo(2 / 3, 0.00001));
    expect(result.recallAtK, 1);
    expect(result.reciprocalRank, 1);
    expect(result.privacyGatePassed, isTrue);
  });

  test('privacy and duplicate defects remain visible in metrics', () {
    final result = SuggestionQualityFixtures.evaluate(
      ranking: ['secret', 'expected', 'expected'],
      relevantIds: {'expected'},
      forbiddenIds: {'secret'},
      k: 3,
    );
    expect(result.forbiddenHits, 1);
    expect(result.duplicateHits, 1);
    expect(result.privacyGatePassed, isFalse);
    expect(result.reciprocalRank, 0.5);
  });

  test('empty fixture is explicit and invalid k is rejected', () {
    final result = SuggestionQualityFixtures.evaluate(
      ranking: [],
      relevantIds: const {},
      forbiddenIds: const {},
      k: 5,
    );
    expect(result.precisionAtK, 0);
    expect(result.recallAtK, 1);
    expect(result.reciprocalRank, 0);
    expect(
      () => SuggestionQualityFixtures.evaluate(
        ranking: [],
        relevantIds: const {},
        forbiddenIds: const {},
        k: 0,
      ),
      throwsFormatException,
    );
  });
}
