import 'dart:convert';
import 'dart:io';

import 'package:golden_reference_engines/golden_reference_engines.dart';
import 'package:test/test.dart';

void main() {
  final corpus = jsonDecode(File('../contracts/engine_reuse_acceptance_v1.json')
      .readAsStringSync()) as Map<String, dynamic>;
  final contracts = (corpus['contracts'] as List).cast<Map<String, dynamic>>();
  for (final group in contracts) {
    if (group['id'] != 'gpx_interoperability_engine' &&
        group['id'] != 'civil_date_recurrence_engine') continue;
    for (final dynamic raw in group['cases'] as List) {
      final vector = raw as Map<String, dynamic>;
      test('portable contract vector ${vector['id']}', () {
        final id = vector['id'] as String;
        final input = vector['input'] as Map<String, dynamic>;
        final expected = vector['expected'] as Map<String, dynamic>;
        if (id == 'gpx.track.valid' || id == 'gpx.invalid.lat' ||
            id == 'gpx.wrong.root' || id == 'gpx.external.entity') {
          void act() {
            final result = GpxReferenceEngine.parse(input['xml'] as String);
            expect(result.document.tracks.length, expected['trackCount']);
            expect(result.document.pointCount, expected['pointCount']);
          }
          if (vector['kind'] == 'reject') {
            expect(act, throwsA(isA<GpxFormatException>().having(
                (e) => e.code, 'errorCode', expected['errorCode'])));
          } else {
            act();
          }
        } else if (id == 'gpx.export.roundtrip') {
          final points = (input['points'] as List).cast<Map<String, dynamic>>();
          final doc = GpxDocument(routes: [
            GpxRoute(points.map((p) => GpxPoint(
                (p['lat'] as num).toDouble(), (p['lon'] as num).toDouble(),
                timeUtc: p['utc'] == null ? null :
                    DateTime.parse(p['utc'] as String))).toList())
          ]);
          final again = GpxReferenceEngine.parse(
              GpxReferenceEngine.export(doc)).document;
          expect(again.pointCount, expected['pointCount']);
          expect(again.routes.single.points.first.latitude,
              doc.routes.single.points.first.latitude);
        } else if (id == 'civil.month.clamp') {
          final date = CivilDate.parse(input['date'] as String);
          expect(CivilRecurrence.nextMonthly(date).toString(), expected['next']);
        } else if (id == 'civil.leap') {
          expect(CivilRecurrence.nextYearly(CivilDate.parse(input['date'] as String),
              leapDayPolicy: LeapDayPolicy.february28).toString(), expected['next']);
        } else if (id == 'civil.nth.weekday') {
          expect(CivilRecurrence.nthWeekday(input['year'] as int, input['month'] as int,
              DateTime.saturday, input['ordinal'] as int).toString(), expected['date']);
        } else if (id == 'civil.last.weekday') {
          expect(CivilRecurrence.lastWeekday(input['year'] as int, input['month'] as int,
              DateTime.thursday).toString(), expected['date']);
        } else if (id == 'civil.lunar.unknown') {
          final result = CivilRecurrence.resolveYear(input['year'] as int,
              [const OverrideCivilRule({})]);
          expect(result.resolved, expected['resolved']);
          expect(result.spans, isEmpty);
        } else {
          fail('Unhandled v28 accepted vector: $id');
        }
      });
    }
  }
}
