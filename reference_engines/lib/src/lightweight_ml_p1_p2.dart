/// Small bounded CPU-only reference math for locally evaluated ML candidates.
/// Not a production predictor, a personal diagnosis, or a battery estimate.
/// Consumers own permissions, user-approved data and downstream actions.
library;

import 'dart:math' as math;

import 'on_device_algorithms.dart';

final class MlVectorRow {
  const MlVectorRow({
    required this.id,
    required this.features,
    this.label,
    this.visible = true,
    this.deleted = false,
  });
  final String id;
  final List<double> features;
  final String? label;
  final bool visible;
  final bool deleted;
}

final class MlNeighbor {
  const MlNeighbor(this.id, this.distance, this.label);
  final String id;
  final double distance;
  final String? label;
}

final class MlLogisticModel {
  const MlLogisticModel(this.weights, this.intercept);
  final List<double> weights;
  final double intercept;

  double predictProbability(List<double> features) {
    if (features.length != weights.length ||
        features.any((v) => !v.isFinite)) {
      throw const OnDeviceMathError('INVALID_LOGISTIC_INPUT');
    }
    var score = intercept;
    for (var i = 0; i < weights.length; i++) {
      score += weights[i] * features[i];
    }
    return _sigmoid(score);
  }

  static double _sigmoid(double v) {
    if (v >= 0) {
      final e = math.exp(-v);
      return 1 / (1 + e);
    }
    final e = math.exp(v);
    return e / (1 + e);
  }
}

abstract final class LocalPredictionReference {
  static void _validateSeries(List<double> values, {int max = 10000}) {
    if (values.isEmpty || values.length > max || values.any((v) => !v.isFinite)) {
      throw const OnDeviceMathError('INVALID_SERIES');
    }
  }

  /// Exponential level smoothing. Caller chooses actual sample interval.
  static List<double> ewma(List<double> values, {double alpha = 0.2}) {
    _validateSeries(values);
    if (!alpha.isFinite || alpha <= 0 || alpha > 1) {
      throw const OnDeviceMathError('INVALID_SMOOTHING_ALPHA');
    }
    var level = values.first;
    final output = <double>[level];
    for (final sample in values.skip(1)) {
      level = alpha * sample + (1 - alpha) * level;
      output.add(level);
    }
    return List.unmodifiable(output);
  }

  /// Holt linear trend forecast; not seasonal, no confidence intervals.
  static List<double> holt(
    List<double> values, {
    double alpha = 0.3,
    double beta = 0.2,
    int horizon = 3,
  }) {
    _validateSeries(values);
    if (values.length < 3 || horizon < 1 || horizon > 365 ||
        !alpha.isFinite || !beta.isFinite ||
        alpha <= 0 || alpha > 1 || beta <= 0 || beta > 1) {
      throw const OnDeviceMathError('INVALID_HOLT_CONFIG');
    }
    var level = values.first;
    var trend = values[1] - values.first;
    for (final value in values.skip(1)) {
      final previous = level;
      level = alpha * value + (1 - alpha) * (level + trend);
      trend = beta * (level - previous) + (1 - beta) * trend;
    }
    return List.unmodifiable(List<double>.generate(
      horizon, (i) => level + (i + 1) * trend,
    ));
  }

  /// Additive seasonal Holt-Winters; needs >=3 full periods (cold start guard).
  /// Negative forecasts are possible and must be domain-clamped by consumers.
  static List<double> holtWinters(
    List<double> values, {
    required int seasonLength,
    double alpha = 0.3,
    double beta = 0.15,
    double gamma = 0.2,
    int horizon = 3,
  }) {
    _validateSeries(values, max: 2000);
    if (seasonLength < 2 || seasonLength > 48 ||
        values.length < 3 * seasonLength || horizon < 1 || horizon > 365 ||
        !alpha.isFinite || !beta.isFinite || !gamma.isFinite ||
        alpha <= 0 || alpha > 1 || beta <= 0 || beta > 1 ||
        gamma <= 0 || gamma > 1) {
      throw const OnDeviceMathError('INVALID_HOLT_WINTERS_CONFIG');
    }
    final firstMean = values.take(seasonLength).reduce((a, b) => a + b) /
        seasonLength;
    final secondMean = values.skip(seasonLength).take(seasonLength)
        .reduce((a, b) => a + b) / seasonLength;
    var level = firstMean;
    var trend = (secondMean - firstMean) / seasonLength;
    final seasonal = List<double>.generate(
      seasonLength, (i) => values[i] - firstMean,
    );
    for (var t = seasonLength; t < values.length; t++) {
      final idx = t % seasonLength;
      final previousLevel = level;
      final previousSeasonal = seasonal[idx];
      level = alpha * (values[t] - previousSeasonal) +
          (1 - alpha) * (level + trend);
      trend = beta * (level - previousLevel) + (1 - beta) * trend;
      seasonal[idx] = gamma * (values[t] - level) +
          (1 - gamma) * previousSeasonal;
    }
    return List.unmodifiable(List<double>.generate(
      horizon,
      (i) => level + (i + 1) * trend +
          seasonal[(values.length + i) % seasonLength],
    ));
  }

  /// Exact small-N Euclidean kNN (not an approximate geo index).
  /// Features must be normalized by the caller; no GPS/Wi-Fi access.
  static List<MlNeighbor> kNearest({
    required List<double> query,
    required Iterable<MlVectorRow> authorizedRows,
    int k = 3,
    int maxRows = 1000,
  }) {
    if (query.isEmpty || query.length > 32 || query.any((e) => !e.isFinite) ||
        k < 1 || k > 50 || maxRows < 1 || maxRows > 1000) {
      throw const OnDeviceMathError('INVALID_KNN_CONFIG');
    }
    final found = <MlNeighbor>[];
    final seen = <String>{};
    var count = 0;
    for (final row in authorizedRows) {
      if (++count > maxRows) throw const OnDeviceMathError('UNBOUNDED_KNN');
      if (row.id.trim().isEmpty || !seen.add(row.id) ||
          row.features.length != query.length ||
          row.features.any((v) => !v.isFinite)) {
        throw const OnDeviceMathError('INVALID_KNN_ROW');
      }
      if (!row.visible || row.deleted) continue;
      var squared = 0.0;
      for (var i = 0; i < query.length; i++) {
        final delta = row.features[i] - query[i];
        squared += delta * delta;
      }
      if (!squared.isFinite) throw const OnDeviceMathError('KNN_OVERFLOW');
      found.add(MlNeighbor(row.id, math.sqrt(squared), row.label));
    }
    found.sort((a, b) {
      final c = a.distance.compareTo(b.distance);
      return c != 0 ? c : a.id.compareTo(b.id);
    });
    return List.unmodifiable(found.take(k));
  }

  /// Fixed-step full-batch binary logistic regression on labeled rows.
  /// Output is NOT calibrated for user-facing risk percentages; evaluate
  /// holdout Brier score and prevalence before displaying probability.
  static MlLogisticModel trainLogistic({
    required List<List<double>> observations,
    required List<int> outcomes,
    int epochs = 200,
    double learningRate = 0.1,
    double l2 = 0.01,
  }) {
    if (observations.length != outcomes.length || observations.length < 10 ||
        observations.length > 2000 ||
        epochs < 1 || epochs > 500 ||
        !learningRate.isFinite || learningRate <= 0 || learningRate > 1 ||
        !l2.isFinite || l2 < 0 || l2 > 1) {
      throw const OnDeviceMathError('INVALID_LOGISTIC_CONFIG');
    }
    final dimension = observations.first.length;
    if (dimension < 1 || dimension > 24 ||
        observations.any((row) => row.length != dimension ||
            row.any((x) => !x.isFinite || x.abs() > 100)) ||
        outcomes.any((y) => y != 0 && y != 1) ||
        !outcomes.contains(0) || !outcomes.contains(1)) {
      throw const OnDeviceMathError('INVALID_LOGISTIC_DATA');
    }
    final w = List<double>.filled(dimension, 0);
    var intercept = 0.0;
    for (var epoch = 0; epoch < epochs; epoch++) {
      final gradient = List<double>.filled(dimension, 0);
      var biasGradient = 0.0;
      for (var row = 0; row < observations.length; row++) {
        var score = intercept;
        for (var col = 0; col < dimension; col++) {
          score += w[col] * observations[row][col];
        }
        final difference = MlLogisticModel._sigmoid(score) - outcomes[row];
        biasGradient += difference;
        for (var col = 0; col < dimension; col++) {
          gradient[col] += difference * observations[row][col];
        }
      }
      final inverseN = 1 / observations.length;
      for (var col = 0; col < dimension; col++) {
        w[col] -= learningRate *
            (gradient[col] * inverseN + l2 * w[col]);
      }
      intercept -= learningRate * biasGradient * inverseN;
      if (!intercept.isFinite || w.any((v) => !v.isFinite)) {
        throw const OnDeviceMathError('LOGISTIC_DIVERGENCE');
      }
    }
    return MlLogisticModel(List.unmodifiable(w), intercept);
  }
}
