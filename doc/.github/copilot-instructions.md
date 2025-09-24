# AI Coding Agent Instructions

Concise, project-specific guidance for this Frappe Bench mono-environment containing multiple Frappe apps: `frappe` (framework), `erpnext`, `hrms`, and custom app `tems`.

## 1. Big Picture Architecture
- This workspace is a Bench root (`frappe-bench/`) hosting multiple Frappe apps under `frappe-bench/apps/` and multi-site data under `frappe-bench/sites/`.
- Core framework: `frappe` (Python + MariaDB + Redis + Node realtime). Business domain layers: `erpnext`, `hrms`. Custom domain extension: `tems` (transport platform).
- Sites (tenants) live in `sites/<site_name>/`; active default site from `sites/common_site_config.json` (`default_site`: `tems.local`).
- Realtime events: Node Socket.IO server (`apps/frappe/socketio.js`, `apps/frappe/realtime/*`) bridges Redis pub/sub channels (defined in `common_site_config.json`) to browser namespaces (one namespace per site).
- Background + async: RQ workers launched via Bench Procfile entry `worker: bench worker`; scheduled jobs via `schedule: bench schedule`; asset rebuild / file watching via `watch: bench watch`.

## 2. Key Configuration Files
- `frappe-bench/Procfile` – process model for local dev (web, socketio, watch, schedule, worker).
- `sites/common_site_config.json` – global bench + site defaults (ports, redis endpoints, dev mode, default site).
- `sites/apps.json` – installed apps & versions/resolution metadata.
- Each app `pyproject.toml` – Python deps & Ruff lint config; framework app (`frappe`) has extensive pinned versions (avoid loosening) and custom gunicorn git ref.
- App integration & lifecycle hooks: `apps/<app>/<app>/hooks.py` (e.g., `apps/tems/tems/hooks.py`). Only enable sections you actually need—leave commented templates intact for future discoverability.

## 3. Conventions & Patterns
- Tabs are acceptable (framework tolerates mixed indentation); Ruff ignores E101/W191 in config—do not “fix” globally.
- Broad `from module import *` patterns exist intentionally in Frappe; Ruff ignores F401/F403/F405 for this reason—avoid removing seemingly unused imports embedded in dynamic registration.
- Use Bench CLI for all site/app operations; do NOT run framework Python scripts directly with raw `python`.
- Multitenancy: treat site name as Socket.IO namespace (`/<site>`). When emitting from Python, publish via Redis channel consumed in `realtime/index.js`—follow existing message schema: `{namespace, room?, event, message}`.

## 4. Typical Developer Workflows
- Start full dev stack (web + workers + realtime + watchers): `bench start` (equivalent to Procfile processes).
- Install an app into a site: `bench --site tems.local install-app tems` (already done; see `bench.log`).
- Database migrations & patches after code changes: `bench --site tems.local migrate`.
- Asset rebuild (JS/CSS) during heavy front-end changes: `bench watch` (normally auto-run under `bench start`).
- Manual rebuild (full): `bench --site tems.local rebuild` (logged as `--rebuild` variants in `logs/bench.log`).
- Backup (on-demand): `bench --site tems.local backup`.
- Adding new site (pattern from HRMS README): `bench new-site <newsite>` then install apps per need.

## 5. Adding Features to Custom App `tems`
- Define DocTypes/UI via Frappe generators inside `apps/tems/tems/` (follow Frappe app scaffolding). Update `hooks.py` when introducing: scheduled tasks (`scheduler_events`), document events (`doc_events`), whitelisted methods (`override_whitelisted_methods`), or client assets (`app_include_js`). Uncomment and minimally edit only needed blocks.
- For scheduled jobs: add dotted path in `scheduler_events` mapping; ensure idempotency (jobs may retry).
- For realtime: publish from Python using Frappe's event emitting utilities (ensure namespace = site). Node side already relays messages; don't modify `realtime/index.js` unless altering protocol.

### 5.1 Creating & Wiring a New DocType (TEMS)
1. Generate: `bench --site tems.local new-doctype "Vehicle" --module TEMS` (or use Desk UI). This creates files under `apps/tems/tems/tems/doctype/vehicle/`.
2. Add fields via Desk (saves JSON + updates model). Keep server logic in `vehicle.py` (class `Vehicle(Document)`). Use `before_save`, `validate`, etc.
3. If you need client logic, add `vehicle.js` in the same folder; Frappe auto loads it for that DocType.
4. Permissions: manage via Role Permission Manager; avoid hardcoding unless dynamic checks are essential (then use `has_permission` hook in `hooks.py`).
5. Add list/kanban settings via the DocType UI; these persist in the DocType JSON—do not hand edit JSON unless scripted migration.
6. After adding / changing DocTypes, run `bench --site tems.local migrate` to apply schema.
7. For fixtures (exporting customizations), add their names to `hooks.py` (`fixtures = ["Custom Field", ...]`) then `bench export-fixtures`.

Minimal server pattern (`vehicle.py`):
```python
import frappe
from frappe.model.document import Document

class Vehicle(Document):
	def validate(self):
		if self.capacity and self.capacity <= 0:
			frappe.throw("Capacity must be positive")
```

### 5.2 Publishing Realtime Events from Python
The Node service (`apps/frappe/realtime/index.js`) listens on Redis channel `events` and re-emits to Socket.IO namespaces matching site names. Message shape it expects: `{namespace, room?, event, message}`.

Use Frappe's redis publisher (pattern):
```python
import frappe, json

def publish_vehicle_status(vehicle_name: str, status: str):
	site = frappe.local.site  # current site = namespace
	payload = {
		"namespace": site,          # becomes "/<site>" namespace
		"event": "vehicle_status", # client listens for this
		"message": {"vehicle": vehicle_name, "status": status},
	}
	r = frappe.utils.redis_queue.get_redis_conn()  # or frappe.redis_conn
	r.publish("events", json.dumps(payload))
```

Optionally target a room (e.g., a group of subscribers) by adding `"room": "fleet:<id>"` to the payload.

Client (browser) example after login (pseudo):
```javascript
const socket = io(`http://localhost:9000/tems.local`, { withCredentials: true });
socket.on('vehicle_status', (data) => { /* update UI */ });
```

Prefer small, explicit payloads; keep event names snake_case; avoid sending large serialized Doc objects—fetch details via REST after notification if needed.

## 6. Dependency & Lint Notes
- Respect pinned versions in `frappe/pyproject.toml` (e.g., `PyMySQL==1.1.1`, custom gunicorn commit). Don’t upgrade casually—framework expects specific APIs.
- New Python libs for `tems` go into `apps/tems/pyproject.toml` under `[project] dependencies`; run `bench pip install -e apps/tems` (bench handles env). Keep `frappe` dependency commented (managed by bench).
- JS realtime/service code uses Node 18+ (see socketio path in Procfile); avoid introducing ESM-only modules without confirming build chain.

## 7. Safe Editing Guidelines
- Never hardcode ports; read from config (`node_utils.get_conf()` on Node side; `frappe.conf` in Python context).
- Maintain commented templates in `hooks.py`—they are living documentation for future hooks.
- Avoid aggressive dead-code cleanup in framework apps; dynamic import & reflection patterns are common.

## 8. Where to Look First For Examples
- Realtime pattern: `apps/frappe/realtime/handlers/frappe_handlers.js` (and middlewares) for socket events & auth shape.
- Bench process orchestration: `Procfile` + corresponding commands seen in `logs/bench.log`.
- Redis + config resolution: `apps/frappe/node_utils.js`.
- Hook scaffolding: `apps/tems/tems/hooks.py` (pristine template to extend).

## 9. When Unsure
- Prefer adding a small hook or scheduled task over modifying framework internals.
- Surface new capability via `hooks.py` + DocType customization; escalate to framework changes only if cross-app reuse needed.

---
Provide feedback if you need deeper specifics (e.g., emitting events from Python, adding DocTypes, or test strategy) so we can extend this document.
