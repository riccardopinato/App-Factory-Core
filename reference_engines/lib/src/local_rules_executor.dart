/// Port-based, idempotent local rule execution.
library;

import 'local_rules.dart';

/// Durable commit obligations are owned by the APP, not the reference engine.
/// A conforming implementation MUST save both the new domain state and a
/// receipt keyed by (authorizedScope,eventId) in one atomic transaction.
/// The port MUST reject replay if the stored fingerprint differs.
abstract interface class LocalRuleCommitPort {
  Future<LocalRuleCommitReceipt> commitOnce({
    required String eventKey,
    required String fingerprint,
    required LocalRuleEvaluation proposal,
  });
}

final class LocalRuleCommitReceipt {
  const LocalRuleCommitReceipt({
    required this.eventKey,
    required this.fingerprint,
    required this.item,
    required this.appliedRuleIds,
    required this.replayed,
  });
  final String eventKey, fingerprint;
  final LocalRuleItem item;
  final List<String> appliedRuleIds;
  final bool replayed;
}

final class LocalRuleExecutionEvent {
  LocalRuleExecutionEvent({
    required this.eventId,
    required this.sourceRevision,
    required this.payloadDigest,
    required this.incoming,
    this.before,
  }) {
    if (eventId.trim().isEmpty || eventId.length > 250 ||
        sourceRevision < 0 || sourceRevision > 0x7fffffff ||
        !RegExp(r'^[0-9a-f]{64}$').hasMatch(payloadDigest) ||
        (before != null && before!.id != incoming.id)) {
      throw const LocalRuleException('INVALID_EVENT');
    }
  }

  final String eventId;
  final int sourceRevision;
  /// Caller-produced SHA-256 of canonical event payload.
  final String payloadDigest;
  final LocalRuleItem incoming;
  final LocalRuleItem? before;

  /// Stable, collision-free representation of the recorded event identity and
  /// source revision and caller-supplied payload SHA-256.
  String get fingerprint =>
      '${incoming.id.length}:${incoming.id}/$sourceRevision/$payloadDigest';
}

abstract final class LocalRulesReferenceExecutor {
  /// This method DOES NOT persist. The injected port decides whether its
  /// backend can guarantee atomic write + durable idempotency.
  static Future<LocalRuleCommitReceipt> execute({
    required LocalRuleExecutionEvent event,
    required Iterable<LocalRuleDefinition> rules,
    required LocalRuleCommitPort port,
    required String authorizedScope,
    required bool canCommit,
    Set<String> validCollectionIds = const {},
  }) async {
    if (!canCommit || authorizedScope.isEmpty ||
        event.incoming.scope != authorizedScope ||
        (event.before != null && event.before!.scope != authorizedScope)) {
      throw const LocalRuleException('FORBIDDEN_SCOPE');
    }
    final evaluation = LocalRuleEngine.evaluate(
      before: event.before,
      incoming: event.incoming,
      rules: rules,
      validCollectionIds: validCollectionIds,
      authorizedScope: authorizedScope,
    );

    String encode(String text) => '${text.length}:$text';
    final eventKey =
        '${encode(authorizedScope)}|${encode(event.eventId)}';
    final receipt = await port.commitOnce(
      eventKey: eventKey,
      fingerprint: event.fingerprint,
      proposal: evaluation,
    );
    if (receipt.eventKey != eventKey ||
        receipt.fingerprint != event.fingerprint ||
        receipt.item.id != event.incoming.id ||
        receipt.item.scope != authorizedScope) {
      throw const LocalRuleException('INVALID_COMMIT_RECEIPT');
    }
    return receipt;
  }
}
