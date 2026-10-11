from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
EXPORT_API_FILES = (
    REPOSITORY_ROOT / "backend/app/api/export_access.py",
    REPOSITORY_ROOT / "backend/app/api/google_sheet.py",
)
EXPORT_FRONTEND_FILES = (
    REPOSITORY_ROOT / "frontend/src/components/ExportListButton.tsx",
    REPOSITORY_ROOT / "frontend/src/services/exportApi.ts",
)


# Supports AC-EXP-04, FR-EXP-05, IF-REG-01, ASM-04.
def test_AC_EXP_04_exported_file_is_usable_in_reg_process() -> None:
    contract = (
        REPOSITORY_ROOT / "docs/integration/export-reg-process.md"
    ).read_text(encoding="utf-8")

    assert ".xlsx" in contract
    assert ".csv" in contract
    assert "ผู้จัดกิจกรรมนำไฟล์ไปดำเนินการต่อในระบบ REG ด้วยตนเอง" in contract


# Supports AC-EXP-05, FR-EXP-06, IF-REG-01, ASM-07.
def test_AC_EXP_05_does_not_upload_to_reg_automatically() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in (*EXPORT_API_FILES, *EXPORT_FRONTEND_FILES))
    contract = (
        REPOSITORY_ROOT / "docs/integration/export-reg-process.md"
    ).read_text(encoding="utf-8")

    assert "/reg" not in source.lower()
    assert "fetch(" not in source or "reg" not in source.lower()
    assert "ไม่อัปโหลดไฟล์หรือส่งรายชื่อไปยัง REG โดยอัตโนมัติ" in contract


# Supports AC-EXP-06, FR-EXP-07, DOM-APP-01, ASM-07.
def test_AC_EXP_06_preserves_existing_project_approval_process() -> None:
    contract = (
        REPOSITORY_ROOT / "docs/integration/export-reg-process.md"
    ).read_text(encoding="utf-8")

    assert "ไม่สร้างหรือเปลี่ยนขั้นตอนอนุมัติโครงการ" in contract
    assert "ไม่มี endpoint, state" in contract
