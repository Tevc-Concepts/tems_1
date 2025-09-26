import frappe


def _table(doctype: str) -> str:
    return f"tab{doctype}"


def _add_col_if_missing(doctype: str, col: str, ddl: str):
    if not frappe.db.has_column(doctype, col):
        frappe.db.sql(f"ALTER TABLE `{_table(doctype)}` ADD COLUMN `{col}` {ddl}")


def _copy_if_exists(doctype: str, src: str, dest: str):
    if frappe.db.has_column(doctype, src):
        _add_col_if_missing(doctype, dest, "varchar(140)")
        frappe.db.sql(
            f"""
            UPDATE `{_table(doctype)}`
            SET `{dest}` = `{src}`
            WHERE (`{dest}` IS NULL OR `{dest}` = '') AND `{src}` IS NOT NULL AND `{src}` != ''
            """
        )


def execute():
    # Emissions Log: move from asset -> vehicle
    _copy_if_exists("Emissions Log", "asset", "vehicle")

    # Maintenance Work Order: ensure vehicle column exists and copy from asset if present
    _copy_if_exists("Maintenance Work Order", "asset", "vehicle")
