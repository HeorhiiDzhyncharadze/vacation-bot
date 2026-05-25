import datetime
import math
from strings import STRINGS, MONTHS

SHIFT = 12.0


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
    rate = total / duration
    rem_h = opening_balance_h + total - used_h
    rem_d = rem_h / SHIFT
    total_d = total / SHIFT
    current_month = datetime.date.today().month

    # Build table rows first so month-name filtering in callers/tests hits
    # the table rows rather than the contract summary line (which also
    # contains start/end month names).
    table_rows = []
    for n in range(1, duration + 1):
        cal = (start_m - 1 + (n - 1)) % 12 + 1
        accrued_h = rate * n
        avail_h = opening_balance_h + accrued_h - used_h
        accrued_d = accrued_h / SHIFT
        avail_d = avail_h / SHIFT
        arrow = " ←" if cal == current_month else ""
        table_rows.append(f"{months[cal - 1]:<11}{accrued_d:>8.1f}{avail_d:>8.1f}{arrow}")

    lines = [
        s['report_header'],
        "",
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
