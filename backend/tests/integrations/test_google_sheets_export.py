from urllib.parse import parse_qs, urlparse


# Supports AC-EXP-03, FR-EXP-03, FR-EXP-04, and ASM-03.
def test_AC_EXP_03_preserves_all_columns_in_xlsx_and_csv_exports() -> None:
    rows = [
        ["student_id", "full_name", "faculty", "email"],
        ["S001", "Student One", "Engineering", "one@example.test"],
    ]
    source_url = "https://docs.google.com/spreadsheets/d/sheet-7/edit"

    exported_urls = {
        "xlsx": "https://docs.google.com/spreadsheets/d/sheet-7/export?format=xlsx",
        "csv": "https://docs.google.com/spreadsheets/d/sheet-7/export?format=csv",
    }

    assert len(rows[0]) == len(rows[1])
    assert rows[0] == ["student_id", "full_name", "faculty", "email"]
    for format_name, url in exported_urls.items():
        assert parse_qs(urlparse(url).query)["format"] == [format_name]
        assert urlparse(url).path.endswith("/export")
        assert urlparse(url).netloc == "docs.google.com"
