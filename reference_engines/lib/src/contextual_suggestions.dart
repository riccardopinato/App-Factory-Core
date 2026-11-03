/// Pure, explainable proposals over caller-authorized domain projections.
/// No personal records, persistence, network access or automatic actions.
library;

final class ContextualSuggestionException implements Exception {
  const ContextualSuggestionException(this.code);
  final String code;
}

final class ContextualSuggestion {
  const ContextualSuggestion({
    required this.id,
    required this.sourceId,
    required this.groupId,
    required this.action,
    required this.reasonCodes,
    required this.sourceRevision,
    required this.expectedRevision,
    this.permitted = false,
    this.visible = false,
    this.deleted = false,
    this.blocked = false,
  });

  final String id;
  final String sourceId;
  final String groupId;
  final String action;
  final Set<String> reasonCodes;
  final String sourceRevision;
  final String expectedRevision;
  final bool permitted;
  final bool visible;
  final bool deleted;
  final bool blocked;

  bool get eligible =>
      permitted &&
      visible &&
      !deleted &&
      !blocked &&
      sourceRevision.isNotEmpty &&
      sourceRevision == expectedRevision;
}

final class ContextualSuggestionHit {
  const ContextualSuggestionHit({
    required this.suggestion,
    required this.score,
    required this.reasons,
  });

  final ContextualSuggestion suggestion;
  final int score;
  final List<String> reasons;
}

abstract final class ContextualSuggestionEngine {
  /// Weights are caller-defined product policy, not trained inference.
  /// Unknown reasons are ignored, never silently treated as evidence.
  static List<ContextualSuggestionHit> propose({
    required Iterable<ContextualSuggestion> candidates,
    required Map<String, int> reasonWeights,
    Set<String> excludedIds = const {},
    int limit = 3,
    int maxPerGroup = 2,
  }) {
    if (limit < 0 ||
        limit > 30 ||
        maxPerGroup < 1 ||
        maxPerGroup > 30 ||
        reasonWeights.length > 30 ||
        reasonWeights.entries.any(
          (e) =>
              e.key.trim().isEmpty ||
              e.key.length > 80 ||
              e.value < -100 ||
              e.value > 100,
        )) {
      throw const ContextualSuggestionException('INVALID_POLICY');
    }

    final grouped = <String, List<ContextualSuggestion>>{};
    for (final candidate in candidates) {
      if (candidate.id.trim().isEmpty ||
          candidate.id.length > 200 ||
          candidate.groupId.trim().isEmpty ||
          candidate.sourceId.trim().isEmpty ||
          candidate.action.trim().isEmpty ||
          candidate.reasonCodes.length > 30) {
        throw const ContextualSuggestionException('INVALID_CANDIDATE');
      }
      grouped.putIfAbsent(candidate.id, () => []).add(candidate);
    }
    final results = <ContextualSuggestionHit>[];
    for (final entry in grouped.entries) {
      // Conflicting variants, access flags or revisions fail closed.
      if (excludedIds.contains(entry.key) || entry.value.length != 1) {
        continue;
      }
      final candidate = entry.value.single;
      if (!candidate.eligible) continue;
      final reasons = candidate.reasonCodes
          .where(reasonWeights.containsKey)
          .toList(growable: false)
        ..sort();
      if (reasons.isEmpty) continue;
      final score = reasons.fold<int>(
        0,
        (total, reason) => total + reasonWeights[reason]!,
      );
      results.add(
        ContextualSuggestionHit(
          suggestion: candidate,
          score: score,
          reasons: List.unmodifiable(reasons),
        ),
      );
    }
    results.sort((a, b) {
      final byScore = b.score.compareTo(a.score);
      if (byScore != 0) return byScore;
      return a.suggestion.id.compareTo(b.suggestion.id);
    });
    final accepted = <ContextualSuggestionHit>[];
    final groupCount = <String, int>{};
    for (final hit in results) {
      if (accepted.length >= limit) break;
      final groupId = hit.suggestion.groupId;
      if ((groupCount[groupId] ?? 0) >= maxPerGroup) continue;
      groupCount[groupId] = (groupCount[groupId] ?? 0) + 1;
      accepted.add(hit);
    }
    return List.unmodifiable(accepted);
  }
}
