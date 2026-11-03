import 'dart:async';

import 'package:golden_reference_engines/golden_reference_engines.dart';
import 'package:test/test.dart';

final class MemoryTransactionalPort implements LocalRuleCommitPort {
  MemoryTransactionalPort(this.receipts);
  final Map<String, LocalRuleCommitReceipt> receipts;
  int commitCount = 0;
  bool failBeforeCommit = false;

  @override
  Future<LocalRuleCommitReceipt> commitOnce({
    required String eventKey,
    required String fingerprint,
    required LocalRuleEvaluation proposal,
  }) async {
    // This fake models a serialized database transaction's atomic boundary;
    // it is NOT a real durable backend.
    if (failBeforeCommit) throw StateError('Simulated transaction rollback');
    final previous = receipts[eventKey];
    if (previous != null) {
      if (previous.fingerprint != fingerprint ||
          !previous.item.sameState(proposal.item)) {
        throw const LocalRuleException('IDEMPOTENCY_CONFLICT');
      }
      return LocalRuleCommitReceipt(
        eventKey: previous.eventKey,
        fingerprint: previous.fingerprint,
        item: previous.item,
        appliedRuleIds: previous.appliedRuleIds,
        replayed: true,
      );
    }
    commitCount++;
    final result = LocalRuleCommitReceipt(
      eventKey:eventKey,fingerprint:fingerprint,item:proposal.item,
      appliedRuleIds:List.unmodifiable(proposal.appliedRuleIds),replayed:false,
    );
    receipts[eventKey] = result;
    return result;
  }
}

void main() {
  const payloadDigest = '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef';
  LocalRuleItem item({String id='item-1',String scope='work'}) =>
      LocalRuleItem(id:id,scope:scope,title:'Task note');

  final rule = LocalRuleDefinition(
    id:'on-create-tag',trigger:LocalTrigger.itemCreated,
    action:LocalAction.addTag,value:'new',
  );

  test('first apply and restart replay use only one transactional effect',() async {
    final state=<String,LocalRuleCommitReceipt>{};
    final event=LocalRuleExecutionEvent(
        eventId:'ev-1',sourceRevision:4,payloadDigest:payloadDigest,incoming:item());
    Future<LocalRuleCommitReceipt> run(MemoryTransactionalPort port) =>
      LocalRulesReferenceExecutor.execute(
        event:event,rules:[rule],port:port,
        authorizedScope:'work',canCommit:true);
    final firstStore=MemoryTransactionalPort(state);
    final first=await run(firstStore);
    expect(first.replayed,false);
    expect(first.item.tags,['new']);
    expect(first.appliedRuleIds,['on-create-tag']);
    final restartedStore=MemoryTransactionalPort(state);
    final again=await run(restartedStore);
    expect(again.replayed,true);
    expect(restartedStore.commitCount,0);
    expect(firstStore.commitCount,1);
    expect(state.length,1);
  });

  test('crash before commit has no phantom receipt; retry succeeds',() async {
    final receipts=<String,LocalRuleCommitReceipt>{};
    final port=MemoryTransactionalPort(receipts)..failBeforeCommit=true;
    final event=LocalRuleExecutionEvent(
      eventId:'ev-fail',sourceRevision:1,payloadDigest:payloadDigest,incoming:item());
    Future<LocalRuleCommitReceipt> call() =>
      LocalRulesReferenceExecutor.execute(
        event:event,rules:[rule],port:port,
        authorizedScope:'work',canCommit:true);
    await expectLater(call(),throwsStateError);
    expect(receipts,isEmpty);
    port.failBeforeCommit=false;
    final recovered=await call();
    expect(recovered.replayed,false);
    expect(recovered.item.tags,['new']);
  });

  test('scope and permission rejected before any write',() async {
    final store=MemoryTransactionalPort({});
    final event=LocalRuleExecutionEvent(
        eventId:'no',sourceRevision:1,payloadDigest:payloadDigest,incoming:item());
    await expectLater(LocalRulesReferenceExecutor.execute(
      event:event,rules:[rule],port:store,
      authorizedScope:'other',canCommit:true),
      throwsA(isA<LocalRuleException>().having(
          (e)=>e.code,'code','FORBIDDEN_SCOPE')));
    await expectLater(LocalRulesReferenceExecutor.execute(
      event:event,rules:[rule],port:store,
      authorizedScope:'work',canCommit:false),
      throwsA(isA<LocalRuleException>()));
    expect(store.commitCount,0);
  });

  test('same event id with different revision fails closed',() async {
    final store=MemoryTransactionalPort({});
    Future<void> apply(int revision) async {
      await LocalRulesReferenceExecutor.execute(
        event:LocalRuleExecutionEvent(
          eventId:'duplicate',sourceRevision:revision,payloadDigest:payloadDigest,incoming:item()),
        rules:[rule],port:store,authorizedScope:'work',canCommit:true);
    }
    await apply(1);
    await expectLater(apply(2),throwsA(isA<LocalRuleException>()
      .having((e)=>e.code,'code','IDEMPOTENCY_CONFLICT')));
    expect(store.commitCount,1);
  });

  test('concurrent duplicate calls cannot apply twice with atomic port',() async {
    final store=MemoryTransactionalPort({});
    final event=LocalRuleExecutionEvent(
      eventId:'race',sourceRevision:1,payloadDigest:payloadDigest,incoming:item());
    final results=await Future.wait(List.generate(8,(_) =>
      LocalRulesReferenceExecutor.execute(
        event:event,rules:[rule],port:store,
        authorizedScope:'work',canCommit:true)));
    expect(results.where((r)=>!r.replayed).length,1);
    expect(store.commitCount,1);
  });
}
