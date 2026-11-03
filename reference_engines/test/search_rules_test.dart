import 'package:golden_reference_engines/golden_reference_engines.dart';
import 'package:test/test.dart';

void main() {
  test('hash feature synonym retrieval and lexical-only fallback', () {
    const engine = LocalHashEmbeddingEngine();
    final documents = [
      SearchReferenceDocument(id: 'b', text: 'Auto elettrica con batteria'),
      SearchReferenceDocument(id: 'a', text: 'Cura del giardino')
    ];
    final semantic = HybridReferenceSearch.search(
        query: 'macchina', documents: documents);
    expect(semantic.hits.first.document.id, 'b');
    expect(semantic.hits.first.reasons, contains('feature_hash'));
    final lexical = HybridReferenceSearch.search(
        query: 'macchina', documents: documents, semanticAvailable: false);
    expect(lexical.hits, isEmpty);
    expect(lexical.mode, 'lexical');
    expect(engine.embed('macchina'), hasLength(192));
  });
  test('visibility, freshness and stable source order are fail-closed', () {
    final a = SearchReferenceDocument(id: 'a', text: 'Montagna', revision: 2);
    final z = SearchReferenceDocument(id: 'z', text: 'Montagna', revision: 1);
    final private = SearchReferenceDocument(
        id: 'private', text: 'Montagna', visible: false);
    final documents = [private, z, a];
    final r1 = HybridReferenceSearch.search(
      query: 'montagna', documents: documents, semanticAvailable: false);
    final r2 = HybridReferenceSearch.search(
      query: 'montagna', documents: documents.reversed,
      semanticAvailable: false);
    expect(r1.hits.map((e) => e.document.id), ['a', 'z']);
    expect(r2.hits.map((e) => e.document.id), ['a', 'z']);
    final index = SearchIndexIdentity('lexical', 1, {'a': 2, 'z': 1, 'private': 0});
    // A stored index with incompatible dimensions must be rebuilt explicitly.
    expect(() => HybridReferenceSearch.search(query: 'montagna',
      documents: documents, semanticAvailable: false, storedIndex: index),
      throwsA(isA<SearchReferenceException>()));
    expect(() => HybridReferenceSearch.search(query: 'montagna',
      documents: [a, SearchReferenceDocument(id:'a',text:'Different',revision:2)]),
      throwsA(isA<SearchReferenceException>().having((e)=>e.code,'code',
        'CONFLICTING_DOCUMENT_REVISION')));
    expect(() => HybridReferenceSearch.search(query: 'x' * 1001, documents: documents),
      throwsA(isA<SearchReferenceException>()));
  });
  test('local rules stable order, scope isolation, no recursion and idempotence', () {
    final item = LocalRuleItem(id: 'n', title: 'Project', scope: 'work');
    final first = LocalRuleEngine.evaluate(
      before: null, incoming: item, authorizedScope: 'work',
      rules: [
        LocalRuleDefinition(id: 'b', trigger: LocalTrigger.itemCreated,
          action: LocalAction.pin, order: 2),
        LocalRuleDefinition(id: 'a', trigger: LocalTrigger.itemCreated,
          action: LocalAction.addTag, value: 'work', order: 1),
      ]);
    expect(first.appliedRuleIds, ['a', 'b']);
    expect(first.item.tags, ['work']);
    expect(first.item.pinned, isTrue);
    final replay = LocalRuleEngine.evaluate(
      before: first.item, incoming: first.item, authorizedScope: 'work',
      rules: [LocalRuleDefinition(id: 'a',
          trigger: LocalTrigger.itemCreated,
          action: LocalAction.addTag, value: 'work')]);
    expect(replay.appliedRuleIds, isEmpty);
    final forbidden = LocalRuleEngine.evaluate(before: null, incoming: item,
      authorizedScope: 'other', rules: [LocalRuleDefinition(id: 'pin',
      trigger: LocalTrigger.itemCreated, action: LocalAction.pin)]);
    expect(forbidden.item.pinned, isFalse);
    expect(() => LocalRuleEngine.evaluate(before: null, incoming: item,
      rules: List.generate(101, (i) => LocalRuleDefinition(
          id: 'r$i',trigger: LocalTrigger.itemCreated,action: LocalAction.pin))),
      throwsA(isA<LocalRuleException>().having((e)=>e.code,'code','TOO_MANY_RULES')));
  });
}
