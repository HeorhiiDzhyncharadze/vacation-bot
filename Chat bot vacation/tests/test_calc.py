import pytest
from calc import build_report, parse_finite, parse_positive, parse_nonneg, parse_nonneg_int, SHIFT, vacation_days_hu, vacation_hours_hu

# Helper: find table rows for a given month name.
# Table rows start with the month name; headline lines start with ✅ or ⏳.
def _table_lines(report: str, month: str) -> list[str]:
    return [l for l in report.split('\n') if l.strip().startswith(month)]


# ---------------------------------------------------------------------------
# parse_positive
# ---------------------------------------------------------------------------

def test_shift_is_12():
    assert SHIFT == 12.0


def test_parse_positive_valid():
    assert parse_positive("168") == 168.0
    assert parse_positive("168,5") == 168.5
    assert parse_positive("  12.0 ") == 12.0


def test_parse_positive_rejects_zero():
    with pytest.raises(ValueError):
        parse_positive("0")


def test_parse_positive_rejects_negative():
    with pytest.raises(ValueError):
        parse_positive("-5")


def test_parse_positive_rejects_text():
    with pytest.raises(ValueError):
        parse_positive("abc")


def test_parse_positive_rejects_nan():
    with pytest.raises(ValueError):
        parse_positive("nan")


# ---------------------------------------------------------------------------
# parse_nonneg
# ---------------------------------------------------------------------------

def test_parse_nonneg_zero_ok():
    assert parse_nonneg("0") == 0.0


def test_parse_nonneg_positive_ok():
    assert parse_nonneg("6") == 6.0


def test_parse_nonneg_rejects_negative():
    with pytest.raises(ValueError):
        parse_nonneg("-1")


def test_parse_nonneg_rejects_inf():
    with pytest.raises(ValueError):
        parse_nonneg("inf")


# ---------------------------------------------------------------------------
# parse_finite (opening balance — allows negatives)
# ---------------------------------------------------------------------------

def test_parse_finite_positive():
    assert parse_finite("36") == 36.0


def test_parse_finite_zero():
    assert parse_finite("0") == 0.0


def test_parse_finite_negative():
    assert parse_finite("-24") == -24.0


def test_parse_finite_negative_decimal():
    assert parse_finite("-12,5") == -12.5


def test_parse_finite_rejects_nan():
    with pytest.raises(ValueError):
        parse_finite("nan")


def test_parse_finite_rejects_inf():
    with pytest.raises(ValueError):
        parse_finite("inf")


# ---------------------------------------------------------------------------
# build_report — reference case (opening_balance = 0, existing behaviour)
# ---------------------------------------------------------------------------

def test_reference_case_may():
    # Annual formula: total=168h/year, rate=14h/mo, used=6d(72h), Jan-Oct
    # May n=5: accrued=70h, avail=70-72=-2h=-0.2d (still a deficit)
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='uk')
    lines = _table_lines(report, 'Травень')
    assert lines, "May table row missing"
    parts = lines[0].replace(' ←', '').strip().split()
    avail = float(parts[-1])
    assert avail < 0, f"Expected May to still be in deficit (annual formula), got: {avail}"


def test_reference_case_june():
    # June n=6: accrued=84h, avail=84-72=12h=1.0d (annual formula: rate=14h/mo)
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='uk')
    lines = _table_lines(report, 'Червень')
    assert lines, "June table row missing"
    assert '1.0' in lines[0], f"Expected 1.0 in June line, got: {lines[0]}"


def test_reference_case_october():
    # October n=10: accrued=140h, avail=140-72=68h=5.67d (annual formula: rate=14h/mo)
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='uk')
    lines = _table_lines(report, 'Жовтень')
    assert lines, "October table row missing"
    assert '5.7' in lines[0], f"Expected 5.7 in October line, got: {lines[0]}"


def test_early_months_show_deficit():
    # January: accrued=14h, used=72h → avail = 14-72 = -58h = -4.83d (no clamp)
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='uk')
    lines = _table_lines(report, 'Січень')
    assert lines, "January table row missing"
    line_clean = lines[0].replace(' ←', '').strip()
    parts = line_clean.split()
    avail = float(parts[-1])
    assert avail < 0, f"Expected negative available in January, got: {avail}"


def test_cross_year_duration():
    # Nov(11) to Mar(3): (3-11)%12+1 = 5 months
    report = build_report(total=120, used_days=0, start_m=11, end_m=3, lang='uk')
    assert '5' in report


def test_cross_year_wraps_months():
    # Should contain Листопад, Грудень, Січень, Лютий, Березень
    report = build_report(total=120, used_days=0, start_m=11, end_m=3, lang='uk')
    for month in ['Листопад', 'Грудень', 'Січень', 'Лютий', 'Березень']:
        assert month in report, f"{month} missing in cross-year report"


def test_zero_used():
    report = build_report(total=144, used_days=0, start_m=1, end_m=10, lang='uk')
    # total=144 → rate=12h/mo; First month: accrued=12h=1.0d, avail=1.0d
    lines = _table_lines(report, 'Січень')
    assert lines
    line_clean = lines[0].replace(' ←', '').strip()
    parts = line_clean.split()
    assert parts[-1] == '1.0'


def test_all_languages_produce_output():
    for lang in ['uk', 'en', 'hu']:
        report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang=lang)
        assert len(report) > 100, f"Report for lang={lang} too short"


def test_english_month_names():
    report = build_report(total=168, used_days=6, start_m=1, end_m=3, lang='en')
    assert 'January' in report
    assert 'February' in report
    assert 'March' in report


def test_hungarian_month_names():
    report = build_report(total=168, used_days=6, start_m=1, end_m=3, lang='hu')
    assert 'Január' in report


# ---------------------------------------------------------------------------
# build_report — opening balance
# ---------------------------------------------------------------------------

def test_opening_balance_positive_shifts_available():
    # opening_balance=+36h (+3d): May avail = 36 + 70 - 72 = 34h = 2.83d (rate=14h/mo)
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='uk',
                          opening_balance_h=36.0)
    lines = _table_lines(report, 'Травень')
    assert lines, "May table row missing"
    parts = lines[0].replace(' ←', '').strip().split()
    assert float(parts[-1]) == pytest.approx(34 / 12, abs=0.1), f"Expected ~2.8, got: {parts[-1]}"


def test_opening_balance_negative_shows_debt():
    # opening_balance=-24h (-2d): January avail = -24 + 14 - 72 = -82h = -6.83d (rate=14h/mo)
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='uk',
                          opening_balance_h=-24.0)
    lines = _table_lines(report, 'Січень')
    assert lines, "January table row missing"
    parts = lines[0].replace(' ←', '').strip().split()
    avail = float(parts[-1])
    assert avail < -6.0, f"Expected debt < -6.0 in January, got: {avail}"


def test_opening_balance_zero_matches_default():
    # Explicit zero should match the no-balance call
    r1 = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='en')
    r2 = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='en',
                      opening_balance_h=0.0)
    assert r1 == r2


def test_opening_balance_line_shown_when_nonzero():
    report = build_report(total=168, used_days=0, start_m=1, end_m=10, lang='en',
                          opening_balance_h=24.0)
    assert 'Opening balance' in report


def test_opening_balance_line_hidden_when_zero():
    report = build_report(total=168, used_days=0, start_m=1, end_m=10, lang='en',
                          opening_balance_h=0.0)
    assert 'Opening balance' not in report


def test_opening_balance_remaining_includes_balance():
    # With +36h balance: remaining = 36 + 14×10 - 72 = 104h = 8.67d → '8.7' (rate=14h/mo)
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='en',
                          opening_balance_h=36.0)
    assert '8.7' in report


# ---------------------------------------------------------------------------
# build_report — headline (big answer for non-tech users)
# ---------------------------------------------------------------------------

def test_report_headline_shown_full_year_contract():
    # Jan-Dec covers all 12 months → today always in contract range
    report = build_report(total=120, used_days=0, start_m=1, end_m=12, lang='en')
    assert 'Right now' in report  # now_available_pos


def test_report_headline_negative_full_year_overuse():
    # 100 days used (1200h) on 120h contract → deep deficit every month → ⏳ headline
    report = build_report(total=120, used_days=100, start_m=1, end_m=12, lang='en')
    assert '⏳' in report  # now_available_neg


def test_report_headline_appears_before_table():
    # Headline must come before the ``` code block
    report = build_report(total=168, used_days=0, start_m=1, end_m=12, lang='en')
    lines = report.split('\n')
    code_block_start = next(i for i, l in enumerate(lines) if l.strip() == '```')
    for i, line in enumerate(lines):
        if 'Right now' in line or '⏳' in line:
            assert i < code_block_start, "Headline must appear before the table"
            break


def test_report_headline_all_languages():
    # Headline present in all 3 languages for a full-year contract
    for lang, keyword in [('uk', 'Зараз'), ('en', 'Right now'), ('hu', 'Most')]:
        report = build_report(total=120, used_days=0, start_m=1, end_m=12, lang=lang)
        assert keyword in report, f"Headline missing for lang={lang}"


# ---------------------------------------------------------------------------
# vacation_days_hu / vacation_hours_hu — Hungarian Labour Code
# ---------------------------------------------------------------------------

def test_hu_base_young():
    assert vacation_days_hu(20, 0) == 20


def test_hu_age_25():
    assert vacation_days_hu(25, 0) == 21


def test_hu_age_28():
    assert vacation_days_hu(28, 0) == 22


def test_hu_age_35():
    assert vacation_days_hu(35, 0) == 25


def test_hu_age_45():
    assert vacation_days_hu(45, 0) == 30


def test_hu_one_child():
    assert vacation_days_hu(25, 1) == 23  # 21 + 2


def test_hu_two_children():
    assert vacation_days_hu(25, 2) == 25  # 21 + 4


def test_hu_three_children():
    assert vacation_days_hu(25, 3) == 28  # 21 + 7


def test_hu_age_and_children():
    assert vacation_days_hu(35, 2) == 29  # 25 + 4


def test_hu_hours_base():
    assert vacation_hours_hu(20, 0) == 160.0  # 20 × 8


# ---------------------------------------------------------------------------
# parse_nonneg_int
# ---------------------------------------------------------------------------

def test_parse_nonneg_int_ok():
    assert parse_nonneg_int("35") == 35


def test_parse_nonneg_int_zero():
    assert parse_nonneg_int("0") == 0


def test_parse_nonneg_int_neg():
    with pytest.raises(ValueError):
        parse_nonneg_int("-1")
