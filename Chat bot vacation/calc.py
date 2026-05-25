import datetime
import math
from strings import STRINGS, MONTHS

SHIFT = 12.0
WORKDAY = 8.0    # standard working hours per day (Hungarian Labour Code)


def parse_positive(text: str) -> float:
    val = float(text.replace(",", ".").strip())
    if not math.isfinite(val) or val <= 0:
        raise ValueError
    return val


def parse_nonneg(text: str) -> float:
    val = float(text.replace(",", ".").strip())
    if not math.isfinite(val) or val < 0:
        raise ValueError
    return val


def parse_finite(text: str) -> float:
    """Accept any finite number including negatives. Used for opening balance."""
    val = float(text.replace(",", ".").strip())
    if not math.isfinite(val):
        raise ValueError
    return val


def parse_nonneg_int(text: str) -> int:
    """Parse a non-negative integer. Used for age and children count."""
    val = int(text.strip())
    if val < 0:
        raise ValueError
    return val


def vacation_days_hu(age: int, num_children: int) -> int:
    """Vacation days per Hungarian Labour Code (Act I of 2012, §§ 117-118).

    age: full years completed.
    num_children: children under 16.
    """
    if age >= 45:   age_bonus = 10
    elif age >= 43: age_bonus = 9
    elif age >= 41: age_bonus = 8
    elif age >= 39: age_bonus = 7
    elif age >= 37: age_bonus = 6
    elif age >= 35: age_bonus = 5
    elif age >= 33: age_bonus = 4
    elif age >= 31: age_bonus = 3
    elif age >= 28: age_bonus = 2
    elif age >= 25: age_bonus = 1
    else:           age_bonus = 0

    if num_children >= 3:   child_bonus = 7
    elif num_children == 2: child_bonus = 4
    elif num_children == 1: child_bonus = 2
    else:                   child_bonus = 0

    return 20 + age_bonus + child_bonus


def vacation_hours_hu(age: int, num_children: int) -> float:
    """Annual vacation hours per Hungarian Labour Code (days × WORKDAY).

    Law defines vacation in standard 8-hour working days.
    Result is the full-year entitlement in hours.
    """
    return vacation_days_hu(age, num_children) * WORKDAY


def build_report(
    total: float,
    used_days: float,
    start_m: int,
    end_m: int,
    lang: str,
    opening_balance_h: float = 0.0,
) -> str:
    s = STRINGS[lang]
    months = MONTHS[lang]
    used_h = used_days * SHIFT
    duration = (end_m - start_m) % 12 + 1
    rate = total / 12                                    # monthly accrual at annual rate
    rem_h = opening_balance_h + rate * duration - used_h  # accrued over period minus used
    rem_d = rem_h / SHIFT
    total_d = total / SHIFT
    current_month = datetime.date.today().month

    # Build table rows; simultaneously capture current-month available days for headline.
    table_rows = []
    current_avail_d = None
    current_month_name = None
    for n in range(1, duration + 1):
        cal = (start_m - 1 + (n - 1)) % 12 + 1
        accrued_h = rate * n
        avail_h = opening_balance_h + accrued_h - used_h
        accrued_d = accrued_h / SHIFT
        avail_d = avail_h / SHIFT
        arrow = " ←" if cal == current_month else ""
        if cal == current_month:
            current_avail_d = avail_d
            current_month_name = months[cal - 1]
        table_rows.append(f"{months[cal - 1]:<11}{accrued_d:>8.1f}{avail_d:>8.1f}{arrow}")

    # Start with header, then optional headline (big answer for non-tech users).
    lines = [s['report_header'], ""]
    if current_avail_d is not None:
        if current_avail_d >= 0:
            lines.append(s['now_available_pos'].format(
                month=current_month_name, days=current_avail_d))
        else:
            lines.append(s['now_available_neg'].format(
                month=current_month_name, days=abs(current_avail_d)))
        lines.append("")

    lines += [
        "```",
        f"{s['col_month']:<11}{s['col_accrued']:>8}{s['col_avail']:>8}",
        "─" * 27,
    ]
    lines.extend(table_rows)
    lines.append("```")
    lines.append("")
    lines.append(s['contract_line'].format(start=months[start_m - 1], end=months[end_m - 1], dur=duration))
    if opening_balance_h != 0.0:
        bal_d = opening_balance_h / SHIFT
        lines.append(s['report_balance_line'].format(bal=opening_balance_h, bal_d=bal_d))
    lines.append(s['total_line'].format(total_h=total, total_d=total_d, rem_d=rem_d))
    lines.append("")
    lines.append(s['disclaimer'])

    return "\n".join(lines)
