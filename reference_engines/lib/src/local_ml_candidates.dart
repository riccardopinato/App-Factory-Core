/// Bounded, deterministic, first-party *candidate* reference engines for
/// lexical near-duplicate proposals and supervised document classification.
/// No user data is stored, transmitted, deleted, merged or relabeled here.
/// Callers MUST authorize source rows before constructing these snapshots.
library;

import 'dart:math' as math;

import 'on_device_algorithms.dart';

final class LocalDuplicateDocument {
  const LocalDuplicateDocument({
    required this.id,
    required this.text,
    this.visible = true,
    this.deleted = false,
  });
  final String id;
  final String text;
  final bool visible;
  final bool deleted;
}

final class LocalDuplicateSuggestion {
  const LocalDuplicateSuggestion({
    required this.id,
    required this.jaccard,
    required this.matchingBands,
  });
  final String id;
  /// Exact shingle Jaccard AFTER probabilistic MinHash/LSH preselection.
  final double jaccard;
  final int matchingBands;
}

/// 64 deterministic MinHash components in 16 bands of 4. False negatives are
/// possible and MUST be evaluated against a full-scan baseline in the caller.
/// Candidate set is limited; for few notes a full exact-Jaccard scan may win.
/// Never use this approximate algorithm as authority for merging/deletion.
abstract final class LocalMinHashLshReference {
  static final RegExp _terms = RegExp(
    r'[\p{L}\p{M}\p{N}]+', unicode: true,
  );
  static const int _prime = 2147483647;
  static const int _hashes = 64;
  static const int _rowsPerBand = 4;

  static Set<String> shingles(String text) {
    if (text.length > 4000) {
      throw const OnDeviceMathError('OVERSIZE_DUPLICATE_TEXT');
    }
    final tokens = _terms.allMatches(text.toLowerCase()).map((e) => e.group(0)!)
        .where((word) => word.runes.length >= 2 && word.runes.length <= 48)
        .toList(growable: false);
    if (tokens.length > 300) {
      throw const OnDeviceMathError('TOO_MANY_DUPLICATE_TOKENS');
    }
    if (tokens.length < 2) return const <String>{};
    return Set.unmodifiable({
      for (var i = 1; i < tokens.length; i++)
        '${tokens[i - 1]} \u0001 ${tokens[i]}',
    });
  }

  static int _stableHash(String value) {
    var hash = 5381;
    for (final rune in value.runes) {
      // Up to 2^31 * 33: exact integer arithmetic on VM and JS.
      hash = ((hash * 33) + rune) & 0x7fffffff;
    }
    return hash;
  }

  static List<int> _signature(Set<String> features) {
    final result = List<int>.filled(_hashes, _prime);
    for (final feature in features) {
      final hashed = _stableHash(feature);
      for (var i = 0; i < _hashes; i++) {
        final a = ((i + 1) * 1009) % 20000 + 1;
        final b = ((i + 1) * 7919) % 20000;
        final value = (a * hashed + b) % _prime;
        if (value < result[i]) result[i] = value;
      }
    }
    return result;
  }

  static int _matchingBands(List<int> a, List<int> b) {
    var matches = 0;
    for (var band = 0; band < _hashes ~/ _rowsPerBand; band++) {
      final start = band * _rowsPerBand;
      var equal = true;
      for (var row = 0; row < _rowsPerBand; row++) {
        if (a[start + row] != b[start + row]) {
          equal = false;
          break;
        }
      }
      if (equal) matches++;
    }
    return matches;
  }

  static double _jaccard(Set<String> a, Set<String> b) {
    if (a.isEmpty || b.isEmpty) return 0;
    final shared = a.where(b.contains).length;
    return shared / (a.length + b.length - shared);
  }

  static List<LocalDuplicateSuggestion> suggest({
    required String query,
    required Iterable<LocalDuplicateDocument> authorizedCandidates,
    int maxCandidates = 500,
    int limit = 10,
    double minimumJaccard = 0.75,
  }) {
    if (maxCandidates < 1 || maxCandidates > 500 || limit < 1 || limit > 50 ||
        !minimumJaccard.isFinite ||
        minimumJaccard < 0.5 || minimumJaccard > 1) {
      throw const OnDeviceMathError('INVALID_DUPLICATE_CONFIG');
    }
    final queryFeatures = shingles(query);
    if (queryFeatures.isEmpty) return const [];
    final querySignature = _signature(queryFeatures);
    final seen = <String>{};
    final suggestions = <LocalDuplicateSuggestion>[];
    var count = 0;
    for (final candidate in authorizedCandidates) {
      if (++count > maxCandidates) {
        throw const OnDeviceMathError('TOO_MANY_DUPLICATE_CANDIDATES');
      }
      if (candidate.id.trim().isEmpty || candidate.id.length > 128 ||
          !seen.add(candidate.id)) {
        throw const OnDeviceMathError('INVALID_DUPLICATE_ID');
      }
      if (!candidate.visible || candidate.deleted) continue;
      final features = shingles(candidate.text);
      if (features.isEmpty) continue;
      final matchingBands = _matchingBands(querySignature, _signature(features));
      if (matchingBands == 0) continue;
      final similarity = _jaccard(queryFeatures, features);
      if (similarity >= minimumJaccard) {
        suggestions.add(LocalDuplicateSuggestion(
          id: candidate.id,
          jaccard: similarity,
          matchingBands: matchingBands,
        ));
      }
    }
    suggestions.sort((a, b) {
      final comparison = b.jaccard.compareTo(a.jaccard);
      return comparison != 0 ? comparison : a.id.compareTo(b.id);
    });
    return List.unmodifiable(suggestions.take(limit));
  }
}

final class LocalLabeledText {
  const LocalLabeledText({
    required this.id,
    required this.label,
    required this.text,
    this.visible = true,
    this.deleted = false,
  });
  final String id;
  final String label;
  final String text;
  final bool visible;
  final bool deleted;
}

final class LocalTextPrediction {
  const LocalTextPrediction({
    required this.label,
    required this.logScoreMargin,
    required this.evidenceTokens,
    required this.trainingRows,
  });
  final String label;
  /// Log-score margin vs second class. NOT a calibrated probability.
  final double logScoreMargin;
  final int evidenceTokens;
  final int trainingRows;
}

/// Bounded Multinomial Naive Bayes with Laplace smoothing and a
/// conservative abstention on unseen vocabulary/insufficient label samples.
/// No sentiment or mental-state inference is certified by this classifier.
/// Labels come from explicit, user-approved examples.
abstract final class LocalNaiveBayesReference {
  static final RegExp _terms = RegExp(
    r'[\p{L}\p{M}\p{N}]+', unicode: true,
  );

  static List<String> _tokens(String text) {
    if (text.length > 4000) {
      throw const OnDeviceMathError('OVERSIZE_CLASSIFICATION_TEXT');
    }
    final tokens = _terms.allMatches(text.toLowerCase())
        .map((e) => e.group(0)!)
        .where((e) => e.runes.length >= 2 && e.runes.length <= 48)
        .toList(growable: false);
    if (tokens.length > 300) {
      throw const OnDeviceMathError('TOO_MANY_CLASSIFICATION_TOKENS');
    }
    return tokens;
  }

  static LocalTextPrediction? classify({
    required String document,
    required Iterable<LocalLabeledText> authorizedTrainingRows,
    int maxTrainingRows = 300,
    int minimumRowsPerLabel = 2,
  }) {
    if (maxTrainingRows < 4 || maxTrainingRows > 300 ||
        minimumRowsPerLabel < 2 || minimumRowsPerLabel > 30) {
      throw const OnDeviceMathError('INVALID_CLASSIFICATION_CONFIG');
    }
    final query = _tokens(document);
    if (query.isEmpty) return null;
    final seen = <String>{};
    final samples = <String, int>{};
    final termCounts = <String, Map<String, int>>{};
    final totalTerms = <String, int>{};
    final vocabulary = <String>{};
    var rowCount = 0;
    var eligibleRows = 0;
    for (final row in authorizedTrainingRows) {
      if (++rowCount > maxTrainingRows) {
        throw const OnDeviceMathError('TOO_MANY_TRAINING_ROWS');
      }
      if (row.id.trim().isEmpty || row.id.length > 128 || !seen.add(row.id) ||
          row.label.trim().isEmpty || row.label.length > 64) {
        throw const OnDeviceMathError('INVALID_TRAINING_ROW');
      }
      if (!row.visible || row.deleted) continue;
      final tokens = _tokens(row.text);
      if (tokens.isEmpty) continue;
      eligibleRows++;
      samples[row.label] = (samples[row.label] ?? 0) + 1;
      final byLabel = termCounts.putIfAbsent(row.label, () => <String, int>{});
      for (final term in tokens) {
        vocabulary.add(term);
        byLabel[term] = (byLabel[term] ?? 0) + 1;
        totalTerms[row.label] = (totalTerms[row.label] ?? 0) + 1;
      }
    }
    if (samples.length < 2 ||
        samples.values.any((n) => n < minimumRowsPerLabel)) {
      return null;
    }
    final recognized = query.where(vocabulary.contains).toList(growable: false);
    if (recognized.isEmpty) return null;
    final labels = samples.keys.toList()..sort();
    final scores = <String, double>{};
    for (final label in labels) {
      var score = math.log(samples[label]! / eligibleRows);
      final denom = totalTerms[label]! + vocabulary.length;
      final byLabel = termCounts[label]!;
      for (final term in recognized) {
        score += math.log(((byLabel[term] ?? 0) + 1) / denom);
      }
      scores[label] = score;
    }
    labels.sort((a, b) {
      final comparison = scores[b]!.compareTo(scores[a]!);
      return comparison != 0 ? comparison : a.compareTo(b);
    });
    final best = labels.first;
    return LocalTextPrediction(
      label: best,
      logScoreMargin: scores[best]! - scores[labels[1]]!,
      evidenceTokens: recognized.length,
      trainingRows: eligibleRows,
    );
  }
}
