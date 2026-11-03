import 'package:golden_reference_engines/golden_reference_engines.dart';
import 'package:test/test.dart';

void main() {
  ContextualSuggestion proposal(
    String id, {
    String group = 'a',
    Set<String> reasons = const {'missing_next_action'},
    bool visible = true,
    bool permitted = true,
    bool deleted = false,
    bool blocked = false,
    String revision = '2',
    String expected = '2',
  }) =>
      ContextualSuggestion(
        id: id,
        sourceId: 'source-$id',
        groupId: group,
        action: 'review',
        reasonCodes: reasons,
        sourceRevision: revision,
        expectedRevision: expected,
        visible: visible,
        permitted: permitted,
        deleted: deleted,
        blocked: blocked,
      );

  const weights = {
    'missing_next_action': 10,
    'due_soon': 5,
    'blocked': -20,
  };

  test('only authorized current sources produce proposals', () {
    final output = ContextualSuggestionEngine.propose(
      candidates: [
        proposal('ok'),
        proposal('hidden', visible: false),
        proposal('forbidden', permitted: false),
        proposal('deleted', deleted: true),
        proposal('blocked', blocked: true),
        proposal('stale', expected: '3'),
      ],
      reasonWeights: weights,
    );
    expect(output.map((e) => e.suggestion.id), ['ok']);
    expect(output.single.reasons, ['missing_next_action']);
  });

  test('stable ranking, reasons and per-group diversity', () {
    final candidates = [
      proposal('b', group: 'one'),
      proposal('a', group: 'one'),
      proposal('c', group: 'one', reasons: {'due_soon'}),
      proposal('d', group: 'two', reasons: {'due_soon'}),
    ];
    final a = ContextualSuggestionEngine.propose(
      candidates: candidates,
      reasonWeights: weights,
      maxPerGroup: 2,
    );
    final b = ContextualSuggestionEngine.propose(
      candidates: candidates.reversed,
      reasonWeights: weights,
      maxPerGroup: 2,
    );
    expect(a.map((e) => e.suggestion.id), ['a', 'b', 'd']);
    expect(b.map((e) => e.suggestion.id), ['a', 'b', 'd']);
    expect(a.first.score, 10);
  });

  test('duplicate identities fail closed, even if one is permitted', () {
    final results = ContextualSuggestionEngine.propose(
      candidates: [
        proposal('same'),
        proposal('same', permitted: false),
      ],
      reasonWeights: weights,
    );
    expect(results, isEmpty);
  });

  test('policy is bounded and supports honest empty result', () {
    expect(
      ContextualSuggestionEngine.propose(
        candidates: [proposal('x', reasons: {'unknown'})],
        reasonWeights: weights,
      ),
      isEmpty,
    );
    expect(
      () => ContextualSuggestionEngine.propose(
        candidates: [],
        reasonWeights: weights,
        maxPerGroup: 0,
      ),
      throwsA(isA<ContextualSuggestionException>()),
    );
    expect(
      ContextualSuggestionEngine.propose(
        candidates: [proposal('x')],
        reasonWeights: weights,
        limit: 0,
      ),
      isEmpty,
    );
  });
}
