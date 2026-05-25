import pytest
from calc import build_report, parse_finite, parse_positive, parse_nonneg, SHIFT


def test_shift_is_12():
    assert SHIFT == 12.0


# ---------------------------------------------------------------------------
# parse_positive
# ---------------------------------------------------------------------------

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
    # total=168h, used=6d(72h), Jan-Oct; May n=5: accrued=84h, avail=12h=1.0d
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='uk')
    lines = [l for l in report.split('\n') if 'Травень' in l]
    assert lines, "May line missing"
    assert '1.0' in lines[0], f"Expected 1.0 in May line, got: {lines[0]}"


def test_reference_case_june():
    # June n=6: accrued=100.8h, avail=28.8h=2.4d
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='uk')
    lines = [l for l in report.split('\n') if 'Червень' in l]
    assert lines, "June line missing"
    assert '2.4' in lines[0], f"Expected 2.4 in June line, got: {lines[0]}"


def test_reference_case_october():
    # October n=10: accrued=168h, avail=96h=8.0d
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='uk')
    lines = [l for l in report.split('\n') if 'Жовтень' in l]
    assert lines, "October line missing"
    assert '8.0' in lines[0], f"Expected 8.0 in October line, got: {lines[0]}"


def test_early_months_show_deficit():
    # January: accrued=16.8h, used=72h → avail = 16.8-72 = -55.2h = -4.6d (no clamp)
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='uk')
    lines = [l for l in report.split('\n') if 'Січень' in l]
    assert lines, "January line missing"
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
    report = build_report(total=120, used_days=0, start_m=1, end_m=10, lang='uk')
    # First month: accrued=12h=1.0d, avail=1.0d
    lines = [l for l in report.split('\n') if 'Січень' in l]
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
    # opening_balance=+36h (+3d): May avail = 36 + 84 - 72 = 48h = 4.0d
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='uk',
                          opening_balance_h=36.0)
    lines = [l for l in report.split('\n') if 'Травень' in l]
    assert lines, "May line missing"
    parts = lines[0].replace(' ←', '').strip().split()
    assert float(parts[-1]) == pytest.approx(4.0), f"Expected 4.0, got: {parts[-1]}"


def test_opening_balance_negative_shows_debt():
    # opening_balance=-24h (-2d): January avail = -24 + 16.8 - 72 = -79.2h = -6.6d
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='uk',
                          opening_balance_h=-24.0)
    lines = [l for l in report.split('\n') if 'Січень' in l]
    assert lines, "January line missing"
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
    # With +36h balance: remaining = 36 + 168 - 72 = 132h = 11.0d
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='en',
                          opening_balance_h=36.0)
    assert '11.0' in report
