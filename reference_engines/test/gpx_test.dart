import 'package:golden_reference_engines/golden_reference_engines.dart';
import 'package:test/test.dart';

void main() {
  const namespaced = '''<?xml version="1.0"?>
<gpx version="1.1" xmlns="http://www.topografix.com/GPX/1/1">
  <metadata><name>Alps &amp; lakes</name></metadata>
  <trk><name>Trail</name><trkseg>
    <trkpt lat="45.0" lon="10.0"><ele>120</ele><time>2026-11-03T12:00:00+02:00</time></trkpt>
    <trkpt lat="46.0" lon="11.0"/>
  </trkseg><trkseg><trkpt lat="46.1" lon="11.1"/></trkseg></trk>
  <rte><name>Return</name><rtept lat="45.0" lon="10.0"/></rte>
  <wpt lat="45.3" lon="10.3"><name>A &amp; B</name></wpt>
</gpx>''';

  test('namespaced GPX 1.1 tracks/segments, routes, waypoints and UTC', () {
    final result = GpxReferenceEngine.parse(namespaced);
    expect(result.originalPointCount, 5);
    final doc = result.document;
    expect(doc.tracks.single.segments, hasLength(2));
    expect(doc.routes.single.points, hasLength(1));
    expect(doc.waypoints.single.name, 'A & B');
    expect(doc.tracks.single.segments.first.first.timeUtc!.toIso8601String(),
        '2026-11-03T10:00:00.000Z');
    expect(doc.name, 'Alps & lakes');
  });

  test('roundtrip preserves route segment ordering, time and XML escaping', () {
    final first = GpxReferenceEngine.parse(namespaced).document;
    final output = GpxReferenceEngine.export(first);
    final second = GpxReferenceEngine.parse(output).document;
    expect(second.pointCount, first.pointCount);
    expect(second.tracks.single.segments, hasLength(2));
    expect(second.waypoints.single.name, 'A & B');
    expect(second.tracks.single.segments.first.first.timeUtc,
        first.tracks.single.segments.first.first.timeUtc);
  });

  test('rejects wrong root, DTD/entities, malformed XML and empty payload', () {
    expect(() => GpxReferenceEngine.parse('<html/>'),
        throwsA(isA<GpxFormatException>().having((e) => e.code, 'code', 'NOT_GPX')));
    expect(() => GpxReferenceEngine.parse(
        '<!DOCTYPE gpx [<!ENTITY x SYSTEM "file:///etc/passwd">]><gpx>&x;</gpx>'),
        throwsA(isA<GpxFormatException>().having((e) => e.code, 'code', 'UNSAFE_XML')));
    expect(() => GpxReferenceEngine.parse('<gpx><broken></gpx>'), throwsA(isA<GpxFormatException>()));
    expect(() => GpxReferenceEngine.parse('<gpx version="1.1"/>'),
        throwsA(isA<GpxFormatException>().having((e) => e.code, 'code', 'EMPTY_GPX')));
  });

  test('rejects bad coordinates and resource ceilings', () {
    expect(() => GpxReferenceEngine.parse(
        '<gpx><wpt lat="91" lon="10"/></gpx>'),
        throwsA(isA<GpxFormatException>().having((e) => e.code, 'code', 'INVALID_COORDINATE')));
    expect(() => GpxReferenceEngine.parse(
        '<gpx><wpt lat="0" lon="0"/><wpt lat="0" lon="1"/></gpx>',
        limits: const GpxLimits(maxPoints: 1)),
        throwsA(isA<GpxFormatException>().having((e) => e.code, 'code', 'TOO_MANY_POINTS')));
    expect(() => GpxReferenceEngine.parse(namespaced,
        limits: const GpxLimits(maxBytes: 40)),
        throwsA(isA<GpxFormatException>().having((e) => e.code, 'code', 'TOO_LARGE')));
  });

  test('simplification preserves endpoints and protected indices', () {
    final points = List.generate(5000,
        (i) => GpxPoint(45.0, 10 + i / 100000.0));
    final simple = GpxReferenceEngine.simplify(points, 3,
        protectedIndices: {1234});
    expect(simple.first, same(points.first));
    expect(simple.last, same(points.last));
    expect(simple, contains(same(points[1234])));
    expect(simple.length, lessThan(5000));
    expect(() => GpxReferenceEngine.simplify(points, -2), throwsArgumentError);
  });
}
