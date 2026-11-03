import 'package:golden_reference_engines/golden_reference_engines.dart';
import 'package:test/test.dart';

void main() {
  const sha='0123456789abcdef0123456789abcdef01234567';
  test('synthetic fixtures stable across replay, distributions, and bounds', () {
    final fixture=SyntheticGeoFixture(id:'f1',seed:42,count:200);
    final first=fixture.generate();
    final second=fixture.generate();
    expect(first.map((p)=>'${p.latitude},${p.longitude}'),
        second.map((p)=>'${p.latitude},${p.longitude}'));
    expect(first.map((p)=>p.id).toSet().length,200);
    expect(SyntheticGeoFixture(id:'f2',seed:42,count:200,
      distribution:FixtureDistribution.sameLocation).generate()
      .every((p)=>p.latitude==45),isTrue);
    final seam=SyntheticGeoFixture(id:'s',seed:3,count:20,
      distribution:FixtureDistribution.antimeridian).generate();
    expect(seam.every((p)=>p.longitude.abs()>179),isTrue);
    expect(()=>SyntheticGeoFixture(id:'huge',seed:0,count:10001),
      throwsA(isA<FixtureReferenceException>()));
  });

  test('benchmark checks identity and exports inspectable run metadata', () {
    final points=SyntheticGeoFixture(id:'grid200',seed:123,count:200).generate();
    final out=ReferencePerformanceHarness.measure(
      sourceSha:sha,fixtureId:'grid200',operation:'clusterGrid',
      runnerProfile:'CI-Dart-VM',sampleIterations:4,
      perform:()=>SpatialReferenceClustering.clusterGrid(
        points,zoom:11).expand((c)=>c.points).map((p)=>p.id).toList()..sort());
    expect(out.outputCount,200);
    expect(out.sampleMicros,hasLength(4));
    expect(out.p95Micros,greaterThanOrEqualTo(out.p50Micros));
    expect(out.toJson()['sourceSha'],sha);
    expect(out.integrityDigest,isA<int>());
  });

  test('benchmark fails closed if output changes or source is malformed', () {
    var next=0;
    expect(()=>ReferencePerformanceHarness.measure(
      sourceSha:sha,fixtureId:'f',operation:'probe',runnerProfile:'CI',
      perform:()=>['${++next}']),throwsA(isA<FixtureReferenceException>()
        .having((e)=>e.code,'code','INCONSISTENT_OUTPUT')));
    expect(()=>ReferencePerformanceHarness.measure(
      sourceSha:'unverified',fixtureId:'f',operation:'probe',
      runnerProfile:'CI',perform:()=>['ok']),
      throwsA(isA<FixtureReferenceException>().having(
          (e)=>e.code,'code','INVALID_MEASUREMENT')));
  });
}
