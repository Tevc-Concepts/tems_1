from __future__ import annotations
import random
import frappe
from frappe.utils import add_days, nowdate
from frappe import _
from .seed_utils import ensure_min_records
from .seed_utils import log_error, write_debug_json, log
def ensure_infrastructure(context):
    """Make sure minimal master data (Warehouse, UOM) exists so subsequent seeding doesn't silently fail."""
    # UOM
    if not frappe.db.exists("UOM", "Litre"):
        try:
            frappe.get_doc({"doctype": "UOM", "uom_name": "Litre"}).insert(ignore_permissions=True)
            frappe.db.commit()
        except Exception as e:  # pragma: no cover - defensive
            frappe.logger().warning(f"[TEMS DEMO] Failed creating UOM Litre: {e}")
            frappe.db.rollback()
    # Warehouse
    if not frappe.get_all("Warehouse", limit=1):
        try:
            wh = frappe.get_doc({
                "doctype": "Warehouse",
                "warehouse_name": "Main",
                "is_group": 0,
                "company": context.get("company"),
            }).insert(ignore_permissions=True)
            frappe.db.commit()
            context["warehouse"] = wh.name
        except Exception as e:
            frappe.logger().warning(f"[TEMS DEMO] Failed creating Warehouse: {e}")
            frappe.db.rollback()



ITEM_NAMES = [
    "Diesel Fuel", "Engine Oil", "Brake Pad Set", "Truck Tyre 22.5", "GPS Tracker",
    "Telematics Sensor", "Hydraulic Hose", "Air Filter", "Clutch Kit", "Gearbox Assembly",
    "Headlamp Unit", "Alternator", "Battery 120Ah", "Wheel Bearing", "Shock Absorber",
    "Exhaust Pipe", "Cabin Filter", "Drive Belt", "Coolant", "Trailer Coupler",
    "Side Mirror", "Windshield Wiper", "Fuel Pump", "Injector", "Radiator"
]


def seed_core_items_suppliers(context, count: int = 20):
    """Ensure at least `count` items & ~count/2 suppliers exist; include pre-existing ones in context."""
    items_ctx = context.setdefault("items", [])
    suppliers_ctx = context.setdefault("suppliers", [])
    # Pull existing first
    existing_items = frappe.get_all("Item", pluck="name", limit=count)
    for nm in existing_items:
        if nm not in items_ctx:
            items_ctx.append(nm)
    # Create missing up to target
    for name in ITEM_NAMES:
        if len(items_ctx) >= count:
            break
        if not frappe.db.exists("Item", name):
            try:
                doc = frappe.get_doc({
                    "doctype": "Item",
                    "item_code": name,
                    "item_name": name,
                    "item_group": "All Item Groups",
                    "is_stock_item": 1
                })
                doc.insert(ignore_permissions=True)
                items_ctx.append(doc.name)
            except Exception as e:
                log_error(context, "Item", e)
                frappe.db.rollback()
    # Suppliers existing
    existing_suppliers = frappe.get_all("Supplier", pluck="name", limit=max(10, count // 2))
    for s in existing_suppliers:
        if s not in suppliers_ctx:
            suppliers_ctx.append(s)
    needed_suppliers = max(10, count // 2)
    idx = 1
    while len(suppliers_ctx) < needed_suppliers and idx < needed_suppliers + 50:
        sup_name = f"Supplier {idx:02d}"
        idx += 1
        if frappe.db.exists("Supplier", sup_name):
            if sup_name not in suppliers_ctx:
                suppliers_ctx.append(sup_name)
            continue
        try:
            sdoc = frappe.get_doc({
                "doctype": "Supplier",
                "supplier_name": sup_name,
                "supplier_group": "All Supplier Groups",
                "tax_id": f"TX{random.randint(1000,9999)}"
            })
            sdoc.insert(ignore_permissions=True)
            suppliers_ctx.append(sdoc.name)
        except Exception as e:
            log_error(context, "Supplier", e)
            frappe.db.rollback()


def seed_purchase_and_stock(context, count: int = 20, stock_target: int | None = None):
    # Debug snapshot before
    try:
        pre = {
            "po_before": frappe.db.count("Purchase Order") if frappe.db.exists("DocType", "Purchase Order") else None,
            "se_before": frappe.db.count("Stock Entry") if frappe.db.exists("DocType", "Stock Entry") else None,
            "target": count,
        }
        write_debug_json("demo_dbg_stock_pre.json", pre)
    except Exception:
        pass
    ensure_infrastructure(context)
    supplier_list = context.get("suppliers", [])
    items = context.get("items", [])
    po_names = []
    existing_po_count = frappe.db.count("Purchase Order") if frappe.db.exists("DocType", "Purchase Order") else 0
    po_create_target = max(0, count - min(existing_po_count, count))
    for _ in range(po_create_target):
        if not supplier_list or not items:
            break
        sup = random.choice(supplier_list)
        item = random.choice(items)
        qty = random.randint(1, 10)
        rate = random.randint(50, 500)
        po = frappe.get_doc({
            "doctype": "Purchase Order",
            "supplier": sup,
            "schedule_date": add_days(nowdate(), 7),
            "items": [{"item_code": item, "qty": qty, "rate": rate}]
        })
        try:
            po.insert(ignore_permissions=True)
            po.submit()
            po_names.append(po.name)
            frappe.db.commit()
        except Exception as e:
            log_error(context, "Purchase Order", e)
            frappe.db.rollback()
    context.setdefault("purchase_orders", []).extend([p for p in po_names if p not in context.get("purchase_orders", [])])

    if stock_target is None:
        try:
            existing_se = frappe.db.count("Stock Entry") if frappe.db.exists("DocType", "Stock Entry") else 0
            stock_target = max(0, 20 - existing_se)
        except Exception:
            stock_target = 0
    se_names = []
    warehouses = frappe.get_all("Warehouse", pluck="name", limit=1)
    target_wh = warehouses[0] if warehouses else None
    if not target_wh:
        try:
            company = context.get("company") or frappe.db.get_value("Company", {}, "name")
            wh = frappe.get_doc({"doctype": "Warehouse", "warehouse_name": "Main", "is_group": 0, "company": company})
            wh.insert(ignore_permissions=True)
            frappe.db.commit()
            target_wh = wh.name
        except Exception as e:
            log_error(context, "Warehouse Provision", e, capture_tb=True)
            frappe.db.rollback()
            return
    candidate_pos = frappe.get_all("Purchase Order", pluck="name", limit=count)
    if not candidate_pos:
        log_error(context, "Stock Entry", Exception("No candidate Purchase Orders found"))
    company = context.get("company") or frappe.db.get_value("Company", {}, "name")
    for itm in items:
        try:
            if frappe.db.has_column("Item", "stock_uom") and not frappe.db.get_value("Item", itm, "stock_uom"):
                frappe.db.set_value("Item", itm, "stock_uom", "Nos")
        except Exception:
            frappe.db.rollback()
    attempts = 0
    for po in candidate_pos:
        if len(se_names) >= (stock_target or 0):
            break
        try:
            attempts += 1
            po_doc = frappe.get_doc("Purchase Order", po)
            po_items = po_doc.get("items") or []
            if not po_items:
                continue
            itm = po_items[0]
            qty = itm.qty or 1
            se = frappe.get_doc({
                "doctype": "Stock Entry",
                "stock_entry_type": "Material Receipt",
                "company": company,
                "posting_date": nowdate(),
                "items": [{
                    "item_code": itm.item_code,
                    "qty": qty,
                    "t_warehouse": target_wh,
                    "basic_rate": random.randint(50, 500),
                }]
            })
            se.insert(ignore_permissions=True)
            se.submit()
            se_names.append(se.name)
            frappe.db.commit()
        except Exception as e:
            log_error(context, "Stock Entry", e, capture_tb=True)
            frappe.db.rollback()
            continue
    fallback_attempts = 0
    while len(se_names) < (stock_target or 0) and items:
        itm_code = random.choice(items)
        try:
            fallback_attempts += 1
            se = frappe.get_doc({
                "doctype": "Stock Entry",
                "stock_entry_type": "Material Receipt",
                "company": company,
                "posting_date": nowdate(),
                "items": [{
                    "item_code": itm_code,
                    "qty": random.randint(1, 5),
                    "t_warehouse": target_wh,
                    "basic_rate": random.randint(50, 500),
                    "valuation_rate": random.randint(50, 500)
                }]
            })
            se.insert(ignore_permissions=True)
            se.submit()
            se_names.append(se.name)
            frappe.db.commit()
        except Exception as e:
            log_error(context, "Stock Entry (Direct)", e, capture_tb=True)
            frappe.db.rollback()
            continue
    context.setdefault("stock_entries", []).extend([s for s in se_names if s not in context.get("stock_entries", [])])
    try:
        post = {
            "po_after": frappe.db.count("Purchase Order") if frappe.db.exists("DocType", "Purchase Order") else None,
            "se_after": frappe.db.count("Stock Entry") if frappe.db.exists("DocType", "Stock Entry") else None,
            "created": len(se_names),
            "attempts": attempts,
            "fallback_attempts": fallback_attempts,
            "stock_target": stock_target,
        }
        write_debug_json("demo_dbg_stock_post.json", post)
        log(context, f"StockEntry top-up attempts={attempts} fallback_attempts={fallback_attempts} created={len(se_names)} target={stock_target}")
    except Exception:
        pass


def seed_assets(context, count: int = 20):
    """Create non-depreciating Assets; in A1 diagnostic mode raise on first failure."""
    frappe.logger().info(f"[TEMS DEMO][ASSETS] seed_assets start target={count}")
    items = context.get("items", []) or frappe.get_all("Item", pluck="name", limit=count)
    company = context.get("company") or frappe.db.get_value("Company", {}, "name")
    # Locate/create category
    categories = frappe.get_all("Asset Category", pluck="name")
    if categories:
        category = categories[0]
    else:
        try:
            # Attempt to pick a minimal fixed asset account (only mandatory for our non-depreciable category)
            fixed_asset_acc = frappe.get_all(
                "Account",
                filters={"account_type": "Fixed Asset", "is_group": 0, "company": company},
                pluck="name",
                limit=1,
            )
            fixed_asset_acc = fixed_asset_acc[0] if fixed_asset_acc else None
            # Build document with at least one accounts child row (required by DocType)
            cat_payload = {
                "doctype": "Asset Category",
                "asset_category_name": "Fleet Parts",
                "is_group": 0,
                "non_depreciable_category": 1,
                "enable_cwip_accounting": 0,
                "accounts": []
            }
            # (Removed accidental nested definition of seed_purchase_and_stock introduced by patch merge)
            if fixed_asset_acc:
                cat_payload["accounts"].append({
                    "company_name": company,
                    "fixed_asset_account": fixed_asset_acc,
                })
            cat_doc = frappe.get_doc(cat_payload)
            cat_doc.insert(ignore_permissions=True)
            frappe.db.commit()
            category = cat_doc.name
        except Exception as e:
            log_error(context, "Asset Category", e)
            frappe.db.rollback()
            return
    # Ensure Asset Category has at least one accounts child row (required by validation)
    try:
        if not category:
            return
        cat_doc = frappe.get_doc("Asset Category", category)
        # Child table parentfield is 'accounts' (error message earlier confirmed)
        frappe.logger().info(f"[TEMS DEMO][ASSETS] Pre-accounts child count={len(getattr(cat_doc, 'accounts', []))}")
        if not getattr(cat_doc, "accounts", []):
            def pick(account_type: str) -> str | None:
                acc = frappe.get_all(
                    "Account",
                    filters={"account_type": account_type, "company": company, "is_group": 0},
                    pluck="name",
                    limit=1,
                )
                return acc[0] if acc else None
            fixed = pick("Fixed Asset")
            accum = pick("Accumulated Depreciation")
            dexp = pick("Depreciation")
            cwip = pick("Capital Work in Progress") or pick("Fixed Asset")
            # Fallbacks: choose any leaf account if specific types not found
            if not (fixed and accum and dexp):
                leaf_any = frappe.get_all("Account", filters={"company": company, "is_group":0}, pluck="name", limit=3)
                while len(leaf_any) < 3:
                    leaf_any.append(leaf_any[0] if leaf_any else None)
                fixed = fixed or (leaf_any[0] if leaf_any else None)
                accum = accum or (leaf_any[1] if len(leaf_any) > 1 else fixed)
                dexp = dexp or (leaf_any[2] if len(leaf_any) > 2 else fixed)
                cwip = cwip or fixed
            if fixed and accum and dexp:
                cat_doc.append("accounts", {
                    "company_name": company,
                    "fixed_asset_account": fixed,
                    "accumulated_depreciation_account": accum,
                    "depreciation_expense_account": dexp,
                    "capital_work_in_progress_account": cwip,
                })
                cat_doc.save(ignore_permissions=True)
                frappe.db.commit()
                frappe.logger().info("[TEMS DEMO][ASSETS] Added accounts child row for Asset Category")
            else:
                log_error(context, "Asset Category Account Setup", Exception("Could not resolve necessary accounts for Asset Category"))
    except Exception as e:
        log_error(context, "Asset Category Account Child Setup", e)
        frappe.db.rollback()

    # Link items to asset category if field exists and empty
    try:
        if frappe.db.has_column("Item", "asset_category"):
            for itm in items:
                if not frappe.db.get_value("Item", itm, "asset_category"):
                    frappe.db.set_value("Item", itm, "asset_category", category)
            frappe.db.commit()
    except Exception as e:
        log_error(context, "Bulk Item Asset Category", e)
        frappe.db.rollback()

    assets_ctx = context.setdefault("assets", [])
    existing = frappe.get_all("Asset", pluck="name", limit=count)
    for nm in existing:
        if nm not in assets_ctx:
            assets_ctx.append(nm)
    seq = 0
    for code in items:
        if len(assets_ctx) >= count:
            break
        seq += 1
        # Re-fetch category doc each iteration to ensure accounts child persisted
        try:
            _cat_child_ct = frappe.db.count("Asset Category Account", {"parent": category})
            if not _cat_child_ct:
                context.setdefault("_errors", []).append("Asset Category still missing child accounts row before asset creation")
        except Exception:
            pass
        # We'll let the framework assign the name (avoid naming collisions)
        asset_name = None
        # Ensure a Location
        loc_name = None
        try:
            loc = frappe.get_all("Location", pluck="name", limit=1)
            if loc:
                loc_name = loc[0]
            else:
                loc_doc = frappe.get_doc({"doctype": "Location", "location_name": "Main Yard", "is_group": 0})
                loc_doc.insert(ignore_permissions=True)
                frappe.db.commit()
                loc_name = loc_doc.name
        except Exception as e:
            log_error(context, "Location", e)
            frappe.db.rollback()
        if not loc_name:
            raise Exception("Failed to provision Location for Asset debug")
        base_fields = {
            "doctype": "Asset",
            "item_code": code,
            "asset_category": category,
            "purchase_date": nowdate(),
            "gross_purchase_amount": random.randint(500, 5000),
            "company": company,
            "is_existing_asset": 1,
            "location": loc_name,
            "calculate_depreciation": 0,
            "opening_accumulated_depreciation": 0,
            "asset_quantity": 1,
        }
        try:
            doc = frappe.get_doc(base_fields)
            doc.insert(ignore_permissions=True, ignore_mandatory=True)
            frappe.db.commit()
            assets_ctx.append(doc.name)
        except Exception as e:
            # Fallback attempt using new_doc workflow ignoring validation
            frappe.db.rollback()
            try:
                alt = frappe.new_doc("Asset")
                for k, v in base_fields.items():
                    if k != "doctype":
                        setattr(alt, k, v)
                alt.flags.ignore_validate = True
                alt.flags.ignore_mandatory = True
                alt.insert(ignore_permissions=True)
                frappe.db.commit()
                assets_ctx.append(alt.name)
            except Exception as e2:
                import traceback
                tb = traceback.format_exc(limit=8)
                context.setdefault("_errors", []).append(
                    f"Asset DEBUG FAILURE FINAL item={code} primary={e} secondary={e2} tail={tb.splitlines()[-1]}"
                )
                frappe.db.rollback()
                raise
    if len(assets_ctx) == 0:
        raise Exception("ASSET DEBUG ASSERT: No assets created after attempt")


def debug_seed_assets():
    """Diagnostic helper to run asset seeding in isolation and return internal info."""
    import inspect
    info = {}
    info["seed_assets_file"] = seed_assets.__code__.co_filename
    info["seed_assets_head"] = inspect.getsource(seed_assets).splitlines()[:12]
    context = {}
    # Prepare minimal context
    comps = frappe.get_all("Company", pluck="name", limit=1)
    if comps:
        context["company"] = comps[0]
    context["items"] = frappe.get_all("Item", pluck="name", limit=25)
    # Pre-capture existing asset categories and account child counts
    cats_state = []
    for cat in frappe.get_all("Asset Category", pluck="name"):
        acc_rows = frappe.get_all("Asset Category Account", filters={"parent": cat}, fields=["company_name","fixed_asset_account","accumulated_depreciation_account","depreciation_expense_account","capital_work_in_progress_account"])
        cats_state.append({"category": cat, "accounts_rows": acc_rows, "row_count": len(acc_rows)})
    info["pre_categories_state"] = cats_state
    try:
        seed_assets(context, count=3)
    except Exception as e:
        info["exception"] = str(e)
    info["asset_count_db"] = frappe.db.count("Asset") if frappe.db.exists("DocType", "Asset") else None
    info["context_assets_len"] = len(context.get("assets", []))
    info["errors_tail"] = (context.get("_errors", []) or [])[-5:]
    # Post-run capture
    cats_state_post = []
    for cat in frappe.get_all("Asset Category", pluck="name"):
        acc_rows = frappe.get_all("Asset Category Account", filters={"parent": cat}, fields=["company_name","fixed_asset_account","accumulated_depreciation_account","depreciation_expense_account","capital_work_in_progress_account"])
        cats_state_post.append({"category": cat, "accounts_rows": acc_rows, "row_count": len(acc_rows)})
    info["post_categories_state"] = cats_state_post
    return info

