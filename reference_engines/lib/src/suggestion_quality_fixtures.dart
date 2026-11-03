/// Evaluation of ranked local suggestions against a curated, synthetic corpus.
/// Metrics are fixture-relative; they are not observed product effectiveness.
library;

final class SuggestionQualityMetrics {
  const SuggestionQualityMetrics({
    required this.precisionAtK,
    required this.recallAtK,
    required this.reciprocalRank,
    required this.forbiddenHits,
    required this.duplicateHits,
  });

  final double precisionAtK;
  final double recallAtK;
  final double reciprocalRank;
  final int forbiddenHits;
  final int duplicateHits;

  bool get privacyGatePassed => forbiddenHits == 0;
}

abstract final class SuggestionQualityFixtures {
  static SuggestionQualityMetrics evaluate({
    required Iterable<String> ranking,
    required Set<String> relevantIds,
    required Set<String> forbiddenIds,
    required int k,
  }) {
    if (k < 1 || k > 500) {
      throw const FormatException('INVALID_K');
    }
    final selected = ranking.take(k).toList(growable: false);
    final unique = selected.toSet();
    final hits = unique.intersection(relevantIds).length;
    final forbidden = selected.where(forbiddenIds.contains).length;
    final reciprocal = selected.indexWhere(relevantIds.contains);
    return SuggestionQualityMetrics(
      precisionAtK: hits / k,
      recallAtK: relevantIds.isEmpty ? 1 : hits / relevantIds.length,
      reciprocalRank: reciprocal < 0 ? 0 : 1 / (reciprocal + 1),
      forbiddenHits: forbidden,
      duplicateHits: selected.length - unique.length,
    );
  }
}
