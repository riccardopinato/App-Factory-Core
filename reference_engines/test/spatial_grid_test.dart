import 'package:golden_reference_engines/golden_reference_engines.dart';
import 'package:test/test.dart';

void main() {
  SpatialPoint point(String id,double lat,double lon) => SpatialPoint(id,lat,lon);
  List<String> signature(List<SpatialCluster> groups) => groups
      .map((c) => '${c.id}:${c.points.map((p) => p.id).join(",")}').toList();

  test('zoom grid separates nearby points at high zoom only', () {
    final input = [point('b',45,10.012),point('a',45,10.001)];
    expect(SpatialReferenceClustering.clusterGrid(input,zoom:8),hasLength(1));
    expect(SpatialReferenceClustering.clusterGrid(input,zoom:16),hasLength(2));
    expect(signature(SpatialReferenceClustering.clusterGrid(input,zoom:8)),
      signature(SpatialReferenceClustering.clusterGrid(input.reversed.toList(),zoom:8)));
  });

  test('antimeridian seam merges the same row, including longitude ±180', () {
    final east = point('e',45,179.9999);
    final west = point('w',45,-179.9999);
    expect(SpatialReferenceClustering.clusterGrid([east,west],zoom:8),hasLength(1));
    expect(SpatialReferenceClustering.clusterGrid(
      [point('a',10,180),point('b',10,-180)],zoom:14),hasLength(1));
  });

  test('high-latitude and different rows stay bounded and deterministic', () {
    final ps=[point('c',89.99,1),point('a',89.99,1),point('b',-89.99,1)];
    final out=SpatialReferenceClustering.clusterGrid(ps,zoom:12);
    expect(out.expand((c)=>c.points).length,3);
    expect(out.any((c)=>c.points.length==2),isTrue);
  });

  test('grid rejects duplicates, over-budget and invalid zoom', () {
    final a=point('a',0,0);
    expect(()=>SpatialReferenceClustering.clusterGrid([a,a],zoom:12),
      throwsA(isA<SpatialReferenceException>().having((e)=>e.code,'code','DUPLICATE_ID')));
    expect(()=>SpatialReferenceClustering.clusterGrid([a,a],zoom:12,maxPoints:1),
      throwsA(isA<SpatialReferenceException>().having((e)=>e.code,'code','TOO_MANY_POINTS')));
    expect(()=>SpatialReferenceClustering.clusterGrid([],zoom:double.nan),
      throwsA(isA<SpatialReferenceException>()));
  });

  test('grid handles 10000 local POIs with no dropped points', () {
    final input=List.generate(10000,(i)=>point('p${i.toString().padLeft(5,"0")}',
      -60.0+(i%100)*0.2,-150.0+(i~/100)*0.3));
    final result=SpatialReferenceClustering.clusterGrid(input,zoom:14);
    expect(result.expand((c)=>c.points).length,10000);
    expect(result.expand((c)=>c.points.map((p)=>p.id)).toSet().length,10000);
  });
}
