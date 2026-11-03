import 'dart:convert';
import 'dart:io';

import 'package:golden_reference_engines/golden_reference_engines.dart';
import 'package:test/test.dart';

void main() {
  final json = jsonDecode(
    File('../contracts/engine_reuse_acceptance_v1.json').readAsStringSync(),
  ) as Map<String, dynamic>;
  final groups = (json['contracts'] as List).cast<Map<String, dynamic>>();
  final expectedIds = {
    'search.lexical.hit', 'search.permissions', 'search.deleted',
    'search.lexical.fallback', 'search.engine.mismatch',
    'rules.create.tag', 'rules.duplicate.noop', 'rules.deleted.noop',
    'rules.missing.target', 'rules.invalid.action',
  };
  final observed = <String>{};
  for (final group in groups) {
    if (group['id'] != 'hybrid_local_search_engine' &&
        group['id'] != 'local_rules_automation_engine') continue;
    for (final raw in group['cases'] as List) {
      final vector = raw as Map<String, dynamic>;
      final id = vector['id'] as String;
      observed.add(id);
      test('portable reference vector $id', () {
        final data = vector['input'] as Map<String, dynamic>;
        final expected = vector['expected'] as Map<String, dynamic>;
        if (id.startsWith('search.')) {
          if (id == 'search.engine.mismatch') {
            final stored = SearchIndexIdentity(
              data['storedEngineId'] as String,
              data['storedDimensions'] as int, const {},
            );
            expect(() => stored.verify(
                data['requestedEngineId'] as String, 192, const []),
                throwsA(isA<SearchReferenceException>().having(
                  (e) => e.code, 'code', expected['errorCode'])));
            return;
          }
          final records = (data['documents'] as List)
              .cast<Map<String, dynamic>>().map((row) => SearchReferenceDocument(
                id: row['id'] as String, text: row['text'] as String,
                revision: row['revision'] as int? ?? 0,
                visible: row['visible'] as bool? ?? true,
                deleted: row['deleted'] as bool? ?? false,
              )).toList();
          final result = HybridReferenceSearch.search(
            query: data['query'] as String, documents: records,
            semanticAvailable: data['semanticAvailable'] as bool? ?? true,
          );
          expect(result.hits.map((e) => e.document.id).toList(), expected['ids']);
          if (expected['mode'] != null) expect(result.mode, expected['mode']);
        } else {
          LocalRuleItem parseItem(Map<String, dynamic> row) => LocalRuleItem(
            id: row['id'] as String, title: row['title'] as String? ?? '',
            tags: (row['tags'] as List?)?.cast<String>() ?? const [],
            collectionId: row['collectionId'] as String?,
            deleted: row['deleted'] as bool? ?? false,
          );
          final rules = (data['rules'] as List)
            .cast<Map<String, dynamic>>();
          if (id == 'rules.invalid.action') {
            expect(() => rules.map(LocalRuleDefinition.fromMap).toList(),
              throwsA(isA<LocalRuleException>().having(
                (e) => e.code, 'code', expected['errorCode'])));
            return;
          }
          final result = LocalRuleEngine.evaluate(
            before: data['before'] == null ? null :
                parseItem(data['before'] as Map<String, dynamic>),
            incoming: parseItem(data['after'] as Map<String, dynamic>),
            validCollectionIds: (data['collections'] as List?)
                ?.cast<String>().toSet() ?? const {},
            rules: rules.map(LocalRuleDefinition.fromMap),
          );
          expect(result.appliedRuleIds, expected['appliedRules']);
          if (expected.containsKey('tags')) expect(result.item.tags, expected['tags']);
          if (expected.containsKey('collectionId')) {
            expect(result.item.collectionId, expected['collectionId']);
          }
        }
      });
    }
  }
  test('portable vectors are not silently skipped', () {
    expect(observed, expectedIds);
  });
}
