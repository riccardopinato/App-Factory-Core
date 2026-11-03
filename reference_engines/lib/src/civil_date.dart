/// Gregorian civil dates: the date is independent of device timezone.
library;

enum OverflowPolicy { clamp, skip, reject }
enum LeapDayPolicy { february28, march1, skip }

final class CivilDate implements Comparable<CivilDate> {
  CivilDate(this.year, this.month, this.day) {
    if (year < 1 || year > 9999 || month < 1 || month > 12 ||
        day < 1 || day > daysInMonth(year, month)) {
      throw ArgumentError.value('$year-$month-$day', 'date', 'Invalid civil date');
    }
  }

  final int year;
  final int month;
  final int day;

  static int daysInMonth(int year, int month) {
    if (year < 1 || year > 9999 || month < 1 || month > 12) {
      throw ArgumentError('Invalid year/month');
    }
    return DateTime.utc(year, month + 1, 0).day;
  }

  static CivilDate parse(String input) {
    if (!RegExp(r'^\d{4}-\d{2}-\d{2}$').hasMatch(input)) {
      throw FormatException('Invalid ISO civil date', input);
    }
    return CivilDate(int.parse(input.substring(0, 4)),
        int.parse(input.substring(5, 7)), int.parse(input.substring(8, 10)));
  }

  factory CivilDate.fromDateTime(DateTime input) =>
      CivilDate(input.year, input.month, input.day);

  DateTime toUtcDateTime() => DateTime.utc(year, month, day);

  int get weekday => toUtcDateTime().weekday;

  @override
  int compareTo(CivilDate other) {
    final y = year.compareTo(other.year);
    if (y != 0) return y;
    final m = month.compareTo(other.month);
    return m != 0 ? m : day.compareTo(other.day);
  }

  @override
  bool operator ==(Object other) => other is CivilDate &&
      year == other.year && month == other.month && day == other.day;

  @override
  int get hashCode => Object.hash(year, month, day);

  @override
  String toString() => '${year.toString().padLeft(4, '0')}-'
      '${month.toString().padLeft(2, '0')}-'
      '${day.toString().padLeft(2, '0')}';
}

final class CivilDateSpan {
  CivilDateSpan(this.start, this.end) {
    if (start.compareTo(end) > 0) throw ArgumentError('start after end');
  }
  final CivilDate start;
  final CivilDate end;

  bool overlapsYear(int year) =>
      start.compareTo(CivilDate(year, 12, 31)) <= 0 &&
      end.compareTo(CivilDate(year, 1, 1)) >= 0;

  String get identity => '$start/$end';
}

sealed class CivilRule {
  const CivilRule();
}

final class FixedCivilDateRule extends CivilRule {
  const FixedCivilDateRule(this.month, this.day);
  final int month, day;
}

final class NthCivilWeekdayRule extends CivilRule {
  const NthCivilWeekdayRule(this.month, this.weekday, this.occurrence);
  final int month, weekday, occurrence;
}

final class LastCivilWeekdayRule extends CivilRule {
  const LastCivilWeekdayRule(this.month, this.weekday);
  final int month, weekday;
}

final class LastCivilMonthDayRule extends CivilRule {
  const LastCivilMonthDayRule(this.month);
  final int month;
}

final class FixedCivilRangeRule extends CivilRule {
  const FixedCivilRangeRule(this.startMonth, this.startDay,
      this.endMonth, this.endDay);
  final int startMonth, startDay, endMonth, endDay;
}

final class OverrideCivilRule extends CivilRule {
  const OverrideCivilRule(this.byYear);
  final Map<int, CivilDateSpan> byYear;
}

final class OneOffCivilRule extends CivilRule {
  const OneOffCivilRule(this.span);
  final CivilDateSpan span;
}

final class CivilResolution {
  const CivilResolution(this.spans, this.resolved);
  final List<CivilDateSpan> spans;
  final bool resolved;
}

abstract final class CivilRecurrence {
  static CivilDate? nextMonthly(CivilDate date,
      {OverflowPolicy overflow = OverflowPolicy.clamp}) {
    final year = date.month == 12 ? date.year + 1 : date.year;
    final month = date.month == 12 ? 1 : date.month + 1;
    final maxDay = CivilDate.daysInMonth(year, month);
    if (date.day > maxDay) {
      return switch (overflow) {
        OverflowPolicy.clamp => CivilDate(year, month, maxDay),
        OverflowPolicy.skip => null,
        OverflowPolicy.reject => throw StateError('Missing monthly date')
      };
    }
    return CivilDate(year, month, date.day);
  }

  static CivilDate? nextYearly(CivilDate date,
      {required LeapDayPolicy leapDayPolicy}) {
    final year = date.year + 1;
    if (date.month == 2 && date.day == 29 &&
        CivilDate.daysInMonth(year, 2) < 29) {
      return switch (leapDayPolicy) {
        LeapDayPolicy.february28 => CivilDate(year, 2, 28),
        LeapDayPolicy.march1 => CivilDate(year, 3, 1),
        LeapDayPolicy.skip => null,
      };
    }
    return CivilDate(year, date.month, date.day);
  }

  static CivilDate nthWeekday(int year, int month, int weekday, int occurrence) {
    _checkWeekday(weekday);
    if (occurrence < 1 || occurrence > 5) {
      throw ArgumentError.value(occurrence, 'occurrence', 'Expected 1..5');
    }
    final first = CivilDate(year, month, 1);
    final day = 1 + (weekday - first.weekday + 7) % 7 +
        (occurrence - 1) * 7;
    if (day > CivilDate.daysInMonth(year, month)) {
      throw StateError('Nonexistent nth weekday');
    }
    return CivilDate(year, month, day);
  }

  static CivilDate lastWeekday(int year, int month, int weekday) {
    _checkWeekday(weekday);
    final last = CivilDate(year, month, CivilDate.daysInMonth(year, month));
    final day = last.day - (last.weekday - weekday + 7) % 7;
    return CivilDate(year, month, day);
  }

  static CivilResolution resolveYear(int year, List<CivilRule> rules) {
    CivilDate.daysInMonth(year, 1);
    final spans = <CivilDateSpan>[];
    var resolved = true;
    for (final rule in rules) {
      CivilDateSpan? span;
      switch (rule) {
        case FixedCivilDateRule r:
          span = CivilDateSpan(CivilDate(year, r.month, r.day),
              CivilDate(year, r.month, r.day));
        case NthCivilWeekdayRule r:
          final date = nthWeekday(year, r.month, r.weekday, r.occurrence);
          span = CivilDateSpan(date, date);
        case LastCivilWeekdayRule r:
          final date = lastWeekday(year, r.month, r.weekday);
          span = CivilDateSpan(date, date);
        case LastCivilMonthDayRule r:
          final date = CivilDate(year, r.month,
              CivilDate.daysInMonth(year, r.month));
          span = CivilDateSpan(date, date);
        case FixedCivilRangeRule r:
          final start = CivilDate(year, r.startMonth, r.startDay);
          final end = CivilDate(
              r.endMonth < r.startMonth ||
                      (r.endMonth == r.startMonth && r.endDay < r.startDay)
                  ? year + 1 : year, r.endMonth, r.endDay);
          span = CivilDateSpan(start, end);
        case OverrideCivilRule r:
          span = r.byYear[year];
          if (span == null) resolved = false;
        case OneOffCivilRule r:
          if (r.span.overlapsYear(year)) span = r.span;
      }
      if (span != null) spans.add(span);
    }
    final byIdentity = <String, CivilDateSpan>{
      for (final span in spans) span.identity: span,
    };
    final distinct = byIdentity.values.toList()
      ..sort((a, b) => a.start.compareTo(b.start));
    return CivilResolution(List.unmodifiable(distinct), resolved);
  }

  static String occurrenceId(String seriesId, CivilDate day,
      {int exceptionRevision = 0}) {
    if (seriesId.trim().isEmpty || exceptionRevision < 0) {
      throw ArgumentError('Invalid occurrence identity');
    }
    return '$seriesId@${day.toString()}#$exceptionRevision';
  }

  static void _checkWeekday(int weekday) {
    if (weekday < DateTime.monday || weekday > DateTime.sunday) {
      throw ArgumentError.value(weekday, 'weekday', 'Expected Mon..Sun 1..7');
    }
  }
}
