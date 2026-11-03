import 'package:golden_reference_engines/golden_reference_engines.dart';
import 'package:test/test.dart';

void main() {
  test('Gregorian date validates and roundtrips, no device timezone dependency', () {
    final date = CivilDate.parse('2028-02-29');
    expect(date.toString(), '2028-02-29');
    expect(CivilDate.fromDateTime(date.toUtcDateTime()), date);
    expect(() => CivilDate(2027, 2, 29), throwsArgumentError);
    expect(() => CivilDate.parse('2026-13-01'), throwsArgumentError);
    expect(() => CivilDate.parse('26-1-1'), throwsFormatException);
  });

  test('explicit monthly overflow modes', () {
    final date = CivilDate(2027, 1, 31);
    expect(CivilRecurrence.nextMonthly(date).toString(), '2027-02-28');
    expect(CivilRecurrence.nextMonthly(date, overflow: OverflowPolicy.skip), isNull);
    expect(() => CivilRecurrence.nextMonthly(date, overflow: OverflowPolicy.reject), throwsStateError);
    expect(CivilRecurrence.nextMonthly(CivilDate(2028, 1, 31)).toString(), '2028-02-29');
    expect(CivilRecurrence.nextMonthly(CivilDate(2026, 12, 31)).toString(), '2027-01-31');
  });

  test('leap policies are explicit', () {
    final leap = CivilDate(2028, 2, 29);
    expect(CivilRecurrence.nextYearly(leap, leapDayPolicy: LeapDayPolicy.february28).toString(), '2029-02-28');
    expect(CivilRecurrence.nextYearly(leap, leapDayPolicy: LeapDayPolicy.march1).toString(), '2029-03-01');
    expect(CivilRecurrence.nextYearly(leap, leapDayPolicy: LeapDayPolicy.skip), isNull);
  });

  test('nth and last weekday from World Days donor', () {
    expect(CivilRecurrence.nthWeekday(2026, 7, DateTime.saturday, 1).toString(), '2026-07-04');
    expect(CivilRecurrence.lastWeekday(2026, 9, DateTime.thursday).toString(), '2026-09-24');
    expect(() => CivilRecurrence.nthWeekday(2026, 2, DateTime.monday, 5), throwsStateError);
    expect(() => CivilRecurrence.nthWeekday(2026, 7, 8, 1), throwsArgumentError);
  });

  test('series deduplication, cross-year spans and unresolved dates', () {
    final span = CivilDateSpan(CivilDate(2026, 12, 31), CivilDate(2027, 1, 2));
    final resolved = CivilRecurrence.resolveYear(2027, [
      OneOffCivilRule(span),
      OneOffCivilRule(span),
      const LastCivilMonthDayRule(2),
    ]);
    expect(resolved.resolved, isTrue);
    expect(resolved.spans.map((s) => s.start.toString()), ['2026-12-31', '2027-02-28']);
    expect(CivilRecurrence.resolveYear(2028, [OneOffCivilRule(span)]).spans, isEmpty);
    final missing = CivilRecurrence.resolveYear(2027, [const OverrideCivilRule({})]);
    expect(missing.resolved, isFalse);
    expect(missing.spans, isEmpty);
    expect(CivilRecurrence.occurrenceId('series-a', CivilDate(2027, 2, 28)),
        'series-a@2027-02-28#0');
  });
}
