import 'package:golden_reference_engines/golden_reference_engines.dart';
import 'package:test/test.dart';

void main() {
  SpatialPoint p(String id, double lat, double lon) => SpatialPoint(id, lat, lon);
  test('stable across input ordering; chain connectivity and isolated point', () {
    final points = [p('c', 0, .0018), p('a', 0, 0),
      p('d', 5, 5), p('b', 0, .0009)];
    List<String> signature(List<SpatialPoint> input) =>
        SpatialReferenceClustering.cluster(input, radiusMeters: 105)
          .map((c) => '${c.id}:${c.points.map((p) => p.id).join(",")}').toList();
    expect(signature(points), ['a:a,b,c', 'd:d']);
    expect(signature(points.reversed.toList()), signature(points));
  });
  test('antimeridian and zero radius', () {
    final east = p('east', 0, 179.9999), west = p('west', 0, -179.9999);
    expect(SpatialReferenceClustering.distanceMeters(east, west), lessThan(30));
    expect(SpatialReferenceClustering.cluster([west,east],radiusMeters:30).length,1);
    expect(SpatialReferenceClustering.cluster([west,east],radiusMeters:0).length,2);
    expect(SpatialReferenceClustering.cluster([p('a',0,0),p('b',0,0)],
      radiusMeters:0).single.points.length,2);
  });
  test('invalid configuration and coordinates fail closed', () {
    expect(() => p('x', 91, 0), throwsA(isA<SpatialReferenceException>()));
    expect(() => p('x', 0, double.nan), throwsA(isA<SpatialReferenceException>()));
    expect(() => SpatialReferenceClustering.cluster([],radiusMeters:-1),
      throwsA(isA<SpatialReferenceException>()));
    expect(() => SpatialReferenceClustering.cluster([],radiusMeters:double.infinity),
      throwsA(isA<SpatialReferenceException>()));
    expect(() => SpatialReferenceClustering.cluster([p('a',0,0),p('a',0,1)],
      radiusMeters:100), throwsA(isA<SpatialReferenceException>()));
    expect(() => SpatialReferenceClustering.cluster([p('a',0,0),p('b',0,1)],
      radiusMeters:100,maxPoints:1), throwsA(isA<SpatialReferenceException>()));
  });
  test('zero-radius seam and pole equivalence', () {
    expect(SpatialReferenceClustering.distanceMeters(
      p('a',0,180),p('b',0,-180)), 0);
    expect(SpatialReferenceClustering.distanceMeters(
      p('a',90,10),p('b',90,-120)), 0);
    expect(SpatialReferenceClustering.cluster([
      p('a',0,180),p('b',0,-180)],radiusMeters:0).single.points.length,2);
    expect(SpatialReferenceClustering.cluster([
      p('a',-90,0),p('b',-90,170)],radiusMeters:0).single.points.length,2);
  });
  test('lazy input stops after cap plus one, without exhausting generator', () {
    var produced = 0;
    Iterable<SpatialPoint> unbounded() sync* {
      while (true) {
        produced++;
        yield p('point_$produced', 0, 0);
      }
    }
    expect(() => SpatialReferenceClustering.cluster(unbounded(),
      radiusMeters:0,maxPoints:3),
      throwsA(isA<SpatialReferenceException>()
        .having((e) => e.code,'code','TOO_MANY_POINTS')));
    expect(produced,4);
  });
}
