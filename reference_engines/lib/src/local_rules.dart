/// Pure deterministic local workflow rule evaluator extracted from Notes donor.
/// Evaluates proposals only. No persistent outbox, background jobs or I/O.
library;

final class LocalRuleException implements Exception {
  const LocalRuleException(this.code);
  final String code;
  @override
  String toString() => 'LocalRuleException($code)';
}

enum LocalTrigger { itemCreated, itemUpdated, taskCompleted }
enum LocalAction { addTag, moveToCollection, pin, setPriority }

final class LocalRuleItem {
  LocalRuleItem({
    required this.id, this.title = '', this.scope = 'default',
    this.tags = const [], this.collectionId, this.pinned = false,
    this.isTask = false, this.completed = false, this.priority = 0,
    this.deleted = false,
  }) {
    if (id.trim().isEmpty || title.length > 60000 || scope.length > 120 ||
        tags.length > 100 || priority < 0 || priority > 3) {
      throw const LocalRuleException('INVALID_ITEM');
    }
  }

  final String id, title, scope;
  final List<String> tags;
  final String? collectionId;
  final bool pinned, isTask, completed, deleted;
  final int priority;

  LocalRuleItem copy({
    List<String>? tags, String? collectionId, bool? pinned, int? priority,
  }) => LocalRuleItem(
    id: id, title: title, scope: scope,
    tags: tags ?? this.tags, collectionId: collectionId ?? this.collectionId,
    pinned: pinned ?? this.pinned, priority: priority ?? this.priority,
    isTask: isTask, completed: completed, deleted: deleted,
  );

  bool sameState(LocalRuleItem other) =>
    id == other.id && title == other.title && scope == other.scope &&
    collectionId == other.collectionId && pinned == other.pinned &&
    isTask == other.isTask && completed == other.completed &&
    priority == other.priority && deleted == other.deleted &&
    _sameTags(tags, other.tags);

  static bool _sameTags(List<String> a, List<String> b) {
    if (a.length != b.length) return false;
    for (var i = 0; i < a.length; i++) {
      if (a[i] != b[i]) return false;
    }
    return true;
  }
}

final class LocalRuleDefinition {
  LocalRuleDefinition({
    required this.id, required this.trigger, required this.action,
    this.value = '', this.enabled = true, this.order = 0,
    this.scope, this.requiredTag, this.titleContains,
  }) {
    if (id.trim().isEmpty || id.length > 200 || order < 0 ||
        value.length > 200 || (scope?.length ?? 0) > 120 ||
        (requiredTag?.length ?? 0) > 80 ||
        (titleContains?.length ?? 0) > 200) {
      throw const LocalRuleException('INVALID_RULE');
    }
    if (action == LocalAction.addTag &&
        (value.trim().isEmpty || value.length > 80)) {
      throw const LocalRuleException('INVALID_TAG');
    }
    if (action == LocalAction.moveToCollection && value.trim().isEmpty) {
      throw const LocalRuleException('INVALID_COLLECTION');
    }
    if (action == LocalAction.setPriority &&
        (int.tryParse(value) == null ||
         int.parse(value) < 0 || int.parse(value) > 3)) {
      throw const LocalRuleException('INVALID_PRIORITY');
    }
    if (action == LocalAction.pin && value.trim().isNotEmpty) {
      throw const LocalRuleException('INVALID_PIN');
    }
  }

  final String id, value;
  final LocalTrigger trigger;
  final LocalAction action;
  final bool enabled;
  final int order;
  final String? scope, requiredTag, titleContains;

  factory LocalRuleDefinition.fromMap(Map<String, dynamic> value) {
    final trigger = LocalTrigger.values.where(
      (e) => e.name == value['trigger']).firstOrNull;
    if (trigger == null) throw const LocalRuleException('UNSUPPORTED_TRIGGER');
    final action = LocalAction.values.where(
      (e) => e.name == value['action']).firstOrNull;
    if (action == null) throw const LocalRuleException('UNSUPPORTED_ACTION');
    return LocalRuleDefinition(
      id: value['id']?.toString() ?? '', trigger: trigger, action: action,
      value: value['value']?.toString() ?? '',
      enabled: value['enabled'] != false, order: (value['order'] as num?)?.toInt() ?? 0,
      scope: value['scope'] as String?,
      requiredTag: value['requiredTag'] as String?,
      titleContains: value['titleContains'] as String?,
    );
  }
}

final class LocalRuleEvaluation {
  const LocalRuleEvaluation(this.item, this.appliedRuleIds, this.trigger);
  final LocalRuleItem item;
  final List<String> appliedRuleIds;
  final LocalTrigger? trigger;
}

abstract final class LocalRuleEngine {
  static LocalRuleEvaluation evaluate({
    required LocalRuleItem? before,
    required LocalRuleItem incoming,
    required Iterable<LocalRuleDefinition> rules,
    Set<String> validCollectionIds = const {},
    String authorizedScope = 'default',
  }) {
    final source = rules.toList(growable: false);
    if (source.length > 100) throw const LocalRuleException('TOO_MANY_RULES');
    if (source.map((r) => r.id).toSet().length != source.length) {
      throw const LocalRuleException('DUPLICATE_RULE');
    }
    if (incoming.deleted || before?.deleted == true ||
        incoming.scope != authorizedScope ||
        (before != null && (before.id != incoming.id || before.scope != incoming.scope))) {
      return LocalRuleEvaluation(incoming, const [], null);
    }
    final LocalTrigger? trigger;
    if (before == null) {
      trigger = LocalTrigger.itemCreated;
    } else if (before.isTask && incoming.isTask &&
        !before.completed && incoming.completed) {
      trigger = LocalTrigger.taskCompleted;
    } else {
      trigger = before.sameState(incoming) ? null : LocalTrigger.itemUpdated;
    }
    if (trigger == null) return LocalRuleEvaluation(incoming, const [], null);
    source.sort((a, b) {
      final order = a.order.compareTo(b.order);
      return order != 0 ? order : a.id.compareTo(b.id);
    });
    var result = incoming;
    final applied = <String>[];
    for (final rule in source) {
      if (!rule.enabled || rule.trigger != trigger ||
          (rule.scope != null && rule.scope != authorizedScope) ||
          (rule.requiredTag != null && !result.tags.any(
            (t) => t.toLowerCase() == rule.requiredTag!.toLowerCase())) ||
          (rule.titleContains != null && !result.title.toLowerCase().contains(
            rule.titleContains!.toLowerCase()))) {
        continue;
      }
      final old = result;
      switch (rule.action) {
        case LocalAction.addTag:
          if (!result.tags.any((t) => t.toLowerCase() == rule.value.toLowerCase())) {
            result = result.copy(tags: [...result.tags, rule.value]);
          }
        case LocalAction.moveToCollection:
          if (validCollectionIds.contains(rule.value) &&
              result.collectionId != rule.value) {
            result = result.copy(collectionId: rule.value);
          }
        case LocalAction.pin:
          if (!result.pinned) result = result.copy(pinned: true);
        case LocalAction.setPriority:
          if (result.isTask && result.priority != int.parse(rule.value)) {
            result = result.copy(priority: int.parse(rule.value));
          }
      }
      if (!identical(result, old)) applied.add(rule.id);
    }
    return LocalRuleEvaluation(result, List.unmodifiable(applied), trigger);
  }
}
