import frappe


def execute():
    """Ensure unique seat per trip at DB level (trip, seat_no).

    Idempotent: checks existing indexes and creates one if missing.
    """
    doctype = "Passenger Booking"
    # raw table name is `tab<DocType>`; DocType has space, backticks will be used in SQL
    table = f"tab{doctype}"

    index_name = "uniq_passenger_booking_trip_seat"
    exists, is_unique = _index_status(table, index_name)
    if exists and is_unique:
        return
    if exists and not is_unique:
        # drop non-unique index so we can add unique
        frappe.db.sql(f"ALTER TABLE `{table}` DROP INDEX `{index_name}`")
    # ensure columns exist (no-op if already there)
    frappe.db.add_index(doctype, ["trip", "seat_no"], index_name=index_name)
    # convert to UNIQUE if still not unique
    _, is_unique = _index_status(table, index_name)
    if not is_unique:
        _make_unique(table, index_name)


def _index_status(table: str, index_name: str) -> tuple[bool, bool]:
    # returns (exists, is_unique)
    rows = frappe.db.sql(
        """
        SELECT NON_UNIQUE
        FROM information_schema.statistics
        WHERE table_schema = DATABASE()
          AND table_name = %s
          AND index_name = %s
        LIMIT 1
        """,
        (table, index_name),
    )
    if not rows:
        return False, False
    # rows[0] is a tuple like (NON_UNIQUE,)
    non_unique = int(rows[0][0])
    return True, non_unique == 0


def _make_unique(table: str, index_name: str) -> None:
    # Try altering index to be UNIQUE if not already
    # Recreate as UNIQUE
    try:
        frappe.db.sql(
            f"ALTER TABLE `{table}` ADD UNIQUE INDEX `{index_name}` (`trip`, `seat_no`)")
    except Exception:
        # If index exists (possibly non-unique), drop and recreate uniquely
        frappe.db.sql(f"ALTER TABLE `{table}` DROP INDEX `{index_name}`")
        frappe.db.sql(
            f"ALTER TABLE `{table}` ADD UNIQUE INDEX `{index_name}` (`trip`, `seat_no`)")

