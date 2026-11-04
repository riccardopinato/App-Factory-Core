import 'package:golden_reference_engines/golden_reference_engines.dart';
import 'package:test/test.dart';

/// Fifty independent IT/EN synthetic gates over the pure source policy.
/// Device latency, user utility and consumer authorization remain unverified.
void main() {
  ContextualSuggestion candidate(
    String id, {
    bool permitted = true,
    bool visible = true,
    bool deleted = false,
    bool blocked = false,
    String revision = 'v1',
    String expected = 'v1',
  }) =>
      ContextualSuggestion(
        id: id,
        sourceId: 'source-$id',
        groupId: id,
        action: 'open',
        reasonCodes: const {'explicit_source'},
        sourceRevision: revision,
        expectedRevision: expected,
        permitted: permitted,
        visible: visible,
        deleted: deleted,
        blocked: blocked,
      );

  for (final locale in ['it', 'en']) {
    for (var scenario = 0; scenario < 25; scenario++) {
      test('$locale scenario $scenario: fail closed and order parity', () {
        final id = '$locale-scenario-$scenario';
        final eligible = candidate('allowed-$id');
        final denied = switch (scenario % 5) {
          0 => candidate('denied-$id', permitted: false),
          1 => candidate('denied-$id', visible: false),
          2 => candidate('denied-$id', deleted: true),
          3 => candidate('denied-$id', blocked: true),
          _ => candidate('denied-$id', expected: 'v2'),
        };
        final list = [
          denied,
          candidate('duplicate-$id'),
          eligible,
          candidate('duplicate-$id', permitted: false),
        ];
        List<ContextualSuggestionHit> rank(Iterable<ContextualSuggestion> input) =>
            ContextualSuggestionEngine.propose(
              candidates: input,
              reasonWeights: const {'explicit_source': 10},
              limit: 3,
            );
        final forward = rank(list);
        final reversed = rank(list.reversed);
        expect(forward.map((item) => item.suggestion.id), ['allowed-$id']);
        expect(
          reversed.map((item) => item.suggestion.id),
          forward.map((item) => item.suggestion.id),
        );
        expect(forward.single.reasons, ['explicit_source']);
        final metric = SuggestionQualityFixtures.evaluate(
          ranking: forward.map((item) => item.suggestion.id),
          relevantIds: {'allowed-$id'},
          forbiddenIds: {'denied-$id', 'duplicate-$id'},
          k: 1,
        );
        expect(metric.precisionAtK, 1);
        expect(metric.recallAtK, 1);
        expect(metric.privacyGatePassed, isTrue);
        expect(metric.duplicateHits, 0);
      });
    }
  }

  for (final size in [500, 5000]) {
    test('$size authorized candidates: deterministic bounded top 3', () {
      final candidates = List.generate(
        size,
        (index) => candidate('item-${index.toString().padLeft(5, '0')}'),
      );
      final forward = ContextualSuggestionEngine.propose(
        candidates: candidates,
        reasonWeights: const {'explicit_source': 10},
        limit: 3,
      );
      final reversed = ContextualSuggestionEngine.propose(
        candidates: candidates.reversed,
        reasonWeights: const {'explicit_source': 10},
        limit: 3,
      );
      expect(forward.length, 3);
      expect(
        forward.map((item) => item.suggestion.id),
        reversed.map((item) => item.suggestion.id),
      );
      expect(forward.map((item) => item.suggestion.id).toSet().length, 3);
    });
  }
}
