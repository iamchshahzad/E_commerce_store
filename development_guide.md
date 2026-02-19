# E-Commerce Development Guide

> [!CAUTION]
> **STRICT RESTRICTION: LOCAL WORK ONLY**
> 1. Do not run `git push`, `git pull`, `git clone`, or `gh` commands.
> 2. Avoid unnecessary `git` commands unless explicitly requested.
> 3. Keep all code changes local.

## Project Structure

### Core Apps
- `e_commerce/`: Project configuration (`settings.py`, `urls.py`).
- `products/`: Product catalog and categories.
- `cart/`: Session-based cart logic.
- `orders/`: Purchase/order handling.
- `users/`: User/auth models and admin.

### Static and Templates
- `static/css/style.css`: Storefront theme and components.
- `static/css/admin_custom.css`: Admin theme overrides and dashboard layout.
- `templates/base.html`: Shared storefront shell (navbar, theme toggle, footer).
- `templates/admin/base_site.html`: Admin header override with home-style navbar structure.
- `templates/products/product_list.html`: Home product row layout.

---

## Theme Rules

### Storefront Theme
- Light mode is default in `:root`.
- Dark mode overrides live in `[data-theme="dark"]`.
- All new UI colors should use CSS variables.

### Admin Theme
- Admin reuses the same theme toggle model as storefront.
- `data-theme` on `<html>` controls both admin and storefront appearance.

### Required Variable Pattern
1. Add token in `:root`.
2. Add matching token in `[data-theme="dark"]`.
3. Use `var(--token)` in component styles.

---

## Header Consistency

- Admin must use the same navbar structure pattern as home:
  - Left: brand
  - Center: nav links
  - Right: theme toggle
- Only link text/targets change for admin context.

---

## Home Layout

### Product Rows
Home page products are horizontal rows:
- Left: image/placeholder
- Middle: category, title, description
- Right: price and actions

Primary selectors:
- `.products-row-list`
- `.product-row`
- `.product-row-media`
- `.product-row-main`
- `.product-row-right`

Responsive behavior:
- Desktop: three-part row.
- Tablet: actions move below content.
- Mobile: stacked rows.

---

## Admin Dashboard Layout

### Two-Column Mapping (Required)
- Left column: app modules (`Authentication and Authorization`, `Products`, etc).
- Right column: `Recent Actions` panel.
- Admin content uses full-page width (no centered/narrow container on desktop).

Primary selectors:
- `body.dashboard #content`
- `.dashboard #content-main`
- `.dashboard #content-related`
- `#recent-actions-module .actionlist li`

Behavior:
- Desktop: two columns with sticky recent-actions panel.
- <=1100px: single column stack.
- Column balance favors readability: wider left app-list column and stable right recent-actions column.
- Recent Actions uses card-style entries with action-type visual markers (`add`, `change`, `delete`) via CSS classes:
  - `#recent-actions-module .actionlist li.addlink`
  - `#recent-actions-module .actionlist li.changelink`
  - `#recent-actions-module .actionlist li.deletelink`
- Recent Actions visual theme is isolated to that module only (accent borders/shadows/markers are applied inside `#recent-actions-module`).
- Desktop layout offsets the Recent Actions column slightly right for clearer visual separation from the left modules column.
- Recent Actions includes a `Clear Activity` control in the module toolbar.
  - UI insertion: `templates/admin/base_site.html` (`.recent-actions-toolbar`, `.recent-actions-clear-btn`).
  - Endpoint: `POST /admin/clear-recent-actions/`.
  - Scope: clears only the current admin user's entries from `django.contrib.admin.models.LogEntry`.
- Product changelist action dropdown uses only Django's default delete action (no custom duplicate delete action entry).
- Admin theme toggle script is bound once via `data-bound` guards in `templates/admin/base_site.html` to prevent double-click toggling issues.
- Admin theme initialization includes a global one-time guard (`window.__ESHOP_ADMIN_THEME_INIT__`) and normalized head boot theme (`dark|light`) to avoid duplicate bindings and stale theme values.
- Admin toggle uses isolated selectors (`#admin-theme-toggle`, `.admin-theme-toggle*`) to avoid collisions with any built-in admin/frontend theme scripts.
- Admin object-tools row (`Add product`) is force-aligned with `.object-tools` flex rules to prevent right-side clipping/overflow on narrow layouts.
- Admin changelist width is controlled with grid layout:
  - `#changelist` uses `minmax(0, 1fr)` for results + fixed filter column aligned to the right.
  - results area allows horizontal scroll (`.results { overflow-x: auto; }`) instead of breaking page width.
  - below `1100px`, changelist collapses to a single-column stack.
- Changelist action bar uses increased vertical space (`.actions` min-height and padding) for clearer control readability.
- Changelist action controls are explicitly balanced:
  - `.actions` uses flex alignment for label, dropdown, and `Run` button.
  - action dropdown keeps a readable minimum width and visible selected text.
  - action dropdown height is slightly increased for clarity.
  - `Run` button width is intentionally compact.
- Filter column is pushed further right with a wider fixed column and right self-alignment.
- Changelist product rows should be visible without horizontal page scrolling:
  - table uses auto layout with constrained inline input widths
  - results container avoids forcing horizontal overflow
- Changelist target snapshot alignment:
  - action dropdown width is reduced and height increased for clearer selected value visibility
  - `Run` button size matches action control height and label readability
  - changelist grid uses a narrower, right-aligned filter column (`300px`) at page end
  - results table uses auto column layout to keep product rows fully visible without bottom horizontal scroll

---

## Workflow

1. Build template structure first.
2. Style with theme variables only.
3. Verify responsive behavior at `1100px`, `900px`, and `640px`.
4. **Update this `development_guide.md` after every prompt that changes UI/behavior.**

## Commit Protocol

- `git add .`
- `git commit -m "feat: description"`
- Never run `git push`.




- Snapshot lock for products changelist:
  - high-specificity body.change-list rules enforce one-line action controls and stable right filter placement
  - fixed result-table column sizing keeps photo/name/category/price/stock/status readable at desktop width
  - paginator area is aligned to left count + right save button to match the target layout
- Latest prompt update (exact screenshot sizing):
  - search bar, action row, table rows, and paginator/save button use fixed desktop heights to match target proportions
  - changelist form container uses a single rounded card wrapper with consistent border spacing
  - filter column remains fixed at the right with unchanged width while left product area scales cleanly
- Latest prompt update (width + visual polish):
  - changelist now uses a wider desktop frame with `main area + fixed 320px filter` and reduced inter-column gap
  - product area card has stronger depth and cleaner top-section separation (search/actions)
  - table header and row-hover visuals were refined for better readability and a more polished admin appearance
- Latest prompt update (product table fit):
  - product image sizing and row height are fixed for consistent visual rhythm
  - results table uses separate borders with defined spacing to mirror the target screenshot
