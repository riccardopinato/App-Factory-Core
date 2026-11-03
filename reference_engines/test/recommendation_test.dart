import 'package:golden_reference_engines/golden_reference_engines.dart';
import 'package:test/test.dart';

void main() {
  RecommendationCandidate item(String id, String group, {
    Set<String> tags = const {}, String? locale,
    bool visible = true, bool published = true,
    bool reviewed = true, bool licensed = true,
  }) => RecommendationCandidate(id: id, groupId: group,
      tags: tags, locale: locale, visible: visible,
      published: published, reviewed: reviewed, licensed: licensed);

  test('eligibility filters BEFORE score, including conflicting ID versions', () {
    final results = ExplainableReferenceRecommender.rank(items: [
      item('hide', 'one', tags: {'photo'}, visible: false),
      item('draft', 'one', tags: {'photo'}, published: false),
      item('license', 'one', tags: {'photo'}, licensed: false),
      item('review', 'one', tags: {'photo'}, reviewed: false),
      item('ok', 'two', tags: {'photo'}),
      item('duplicate', 'third', tags: {'photo'}),
      item('duplicate', 'third', tags: {'photo'}, visible: false),
    ], context: const RecommendationContext(interests: {'photo'}));
    expect(results.map((e) => e.item.id), ['ok']);
    expect(results.single.reasonCodes, ['interest']);
    expect(results.single.score, 40);
  });

  test('stable ties, input shuffle, locale preference and per-group cap', () {
    final list = [
      item('c','j1',tags:{'photo'},locale:'en'),
      item('a','j1',tags:{'photo'},locale:'en'),
      item('b','j1',tags:{'photo'},locale:'en'),
      item('d','j2',tags:{'photo'},locale:'en'),
      item('d','j2',tags:{'photo'},locale:'it'),
    ];
    const ctx = RecommendationContext(
        interests: {'photo'}, locale: 'it', maxPerGroup: 2);
    final first = ExplainableReferenceRecommender.rank(items:list, context:ctx);
    final reverse = ExplainableReferenceRecommender.rank(
        items:list.reversed, context:ctx);
    expect(first.map((e) => e.item.id), ['d','a','b']);
    expect(reverse.map((e) => e.item.id), ['d','a','b']);
    expect(first.first.item.locale, 'it');
    expect(first.first.reasonCodes, ['interest','locale']);
    expect(first.map((e) => e.item.id).toSet().length, 3);
  });

  test('honest empty and bounded score/exclusions', () {
    expect(ExplainableReferenceRecommender.rank(items:[],
        context:const RecommendationContext()),isEmpty);
    expect(ExplainableReferenceRecommender.rank(
      items:[item('id', 'group')],
      context:const RecommendationContext(excludedIds:{'id'})), isEmpty);
    expect(ExplainableReferenceRecommender.rank(
      items:[item('id', 'group')],
      context:const RecommendationContext(limit:0)), isEmpty);
    expect(()=>ExplainableReferenceRecommender.rank(items:[],
        context:const RecommendationContext(maxPerGroup:0)),
        throwsA(isA<RecommendationReferenceException>()));
  });
}
