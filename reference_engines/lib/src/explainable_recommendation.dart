/// Deterministic, explainable local ranking of ALREADY eligible content.
/// No rights verification, implicit publication, behavioral tracking or cloud AI.
library;

final class RecommendationReferenceException implements Exception {
  const RecommendationReferenceException(this.code);
  final String code;
}

final class RecommendationCandidate {
  RecommendationCandidate({
    required this.id, required this.groupId,
    this.tags = const {}, this.locale,
    this.visible = true, this.published = true, this.reviewed = true,
    this.licensed = true,
  }) {
    if (id.trim().isEmpty || groupId.trim().isEmpty ||
        id.length > 200 || groupId.length > 200) {
      throw const RecommendationReferenceException('INVALID_CANDIDATE');
    }
  }
  final String id, groupId;
  final Set<String> tags;
  final String? locale;
  final bool visible, published, reviewed, licensed;

  bool get eligible => visible && published && reviewed && licensed;
}

final class RecommendationContext {
  const RecommendationContext({
    this.interests = const {},
    this.locale,
    this.excludedIds = const {},
    this.limit = 20,
    this.maxPerGroup = 2,
  });
  final Set<String> interests;
  final String? locale;
  final Set<String> excludedIds;
  final int limit, maxPerGroup;
}

final class RecommendationReferenceHit {
  const RecommendationReferenceHit(this.item, this.score, this.reasonCodes);
  final RecommendationCandidate item;
  final int score;
  final List<String> reasonCodes;
}

abstract final class ExplainableReferenceRecommender {
  static List<RecommendationReferenceHit> rank({
    required Iterable<RecommendationCandidate> items,
    required RecommendationContext context,
  }) {
    if (context.limit < 0 || context.limit > 500 ||
        context.maxPerGroup < 1 || context.maxPerGroup > 500) {
      throw const RecommendationReferenceException('INVALID_LIMIT');
    }
    // A conflicting duplicate record cannot make an otherwise inaccessible
    // item eligible. Fail closed on ID-level privacy and editorial metadata.
    final grouped = <String, List<RecommendationCandidate>>{};
    for (final item in items) {
      grouped.putIfAbsent(item.id, () => []).add(item);
    }
    final candidates = <RecommendationReferenceHit>[];
    for (final group in grouped.entries) {
      if (context.excludedIds.contains(group.key) ||
          group.value.any((item) => !item.eligible)) continue;
      // A canonical item may have multiple locale variants. Deterministically
      // choose the best localized variant after ranking each variant.
      final variants = <RecommendationReferenceHit>[];
      for (final item in group.value) {
        final interests = item.tags.map((e) => e.toLowerCase()).toSet();
        final matching = context.interests.any(
          (interest) => interests.contains(interest.toLowerCase()));
        final localeMatch = context.locale != null && item.locale == context.locale;
        final reasons = <String>[];
        var score = 0;
        if (matching) { score += 40; reasons.add('interest'); }
        if (localeMatch) { score += 4; reasons.add('locale'); }
        variants.add(RecommendationReferenceHit(
          item, score, List.unmodifiable(reasons)));
      }
      variants.sort((a, b) {
        final s = b.score.compareTo(a.score);
        if (s != 0) return s;
        return (a.item.locale ?? '').compareTo(b.item.locale ?? '');
      });
      candidates.add(variants.first);
    }
    candidates.sort((a, b) {
      final diff = b.score.compareTo(a.score);
      return diff == 0 ? a.item.id.compareTo(b.item.id) : diff;
    });
    final perGroup = <String, int>{};
    final selected = <RecommendationReferenceHit>[];
    for (final candidate in candidates) {
      final group = candidate.item.groupId;
      if ((perGroup[group] ?? 0) >= context.maxPerGroup) continue;
      perGroup[group] = (perGroup[group] ?? 0) + 1;
      selected.add(candidate);
      if (selected.length == context.limit) break;
    }
    return List.unmodifiable(context.limit == 0 ? <RecommendationReferenceHit>[] : selected);
  }
}
