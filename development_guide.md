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

### Frontend (React)
- `frontend/`: Vite + React storefront app.
- `frontend/src/App.jsx`: Main routes and page shells.
- `frontend/src/api.js`: Calls Django API endpoints.
- `frontend/src/cart.js`: LocalStorage cart state helpers.
- `frontend/src/styles.css`: React storefront styles.

### Static and Templates
- Django templates are now legacy/fallback pages.
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

## React Storefront Rules

- React app is the default storefront runtime.
- Data source for products/categories is Django REST API:
  - `GET /api/products/`
  - `GET /api/products/<id>/`
  - `GET /api/categories/`
- React dev server proxies `/api` and `/media` to Django (`127.0.0.1:8000`).
- Production/local attached mode: build React and let Django serve `frontend/dist/index.html`.
- Backend route split:
  - API endpoints are under `/api/`
  - Non-API frontend routes are resolved by Django catch-all to React entrypoint
- Cart is client-side (`localStorage`) until backend cart APIs are introduced.
- Store management actions in React:
  - `POST /api/users/login/` for JWT access token
  - `POST /api/users/customer-login/` for customer-only JWT access token
  - `POST /api/users/register/` for customer account creation
  - `POST /api/categories/` for category creation (auth required)
  - `POST /api/products/` for product creation (auth required)
- Keep components focused and avoid embedding API calls directly in deeply nested UI elements.
- Frontend route map:
  - `/` Home page
  - `/products` Product listing
  - `/product/:id` Product detail
  - `/cart` Cart
  - `/login` unified login page (choose Admin Login or Customer Login)
  - `/customer-signup` customer account creation page
  - `/admin-tools` Admin-only management page for category/product creation
- Navbar behavior:
  - Guest/customer navbar shows `Home`, `Products`, `Cart`, `Login`
  - Admin navbar uses a different visual theme and shows `Dashboard`, `Catalog`, `Admin Tools`, `Logout`
  - Navbar is responsive with a mobile menu toggle

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

1. Build React page/component structure first.
2. Keep API access in `frontend/src/api.js`.
3. Keep cart state operations in `frontend/src/cart.js`.
4. Style in `frontend/src/styles.css`.
5. Verify responsive behavior at `1100px`, `900px`, and `640px`.
6. **Update this `development_guide.md` after every prompt that changes UI/behavior.**

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
- Latest prompt update (React migration):
  - added `frontend/` Vite + React storefront with routes for products, product detail, and cart
  - wired React data layer to existing Django API (`/api/products`, `/api/categories`)
  - moved storefront cart behavior to LocalStorage via `frontend/src/cart.js`
- Latest prompt update (React attached to backend):
  - removed Django storefront template routes from `products/urls.py`
  - moved products/categories endpoints to backend API namespace (`/api/...`)
  - added Django catch-all route to serve React build for non-API paths
- Latest prompt update (React manage actions):
  - added `/manage` page with login form and token persistence in LocalStorage
  - added Add Category and Add Product forms in React (optional product image upload)
  - wired creation flow to protected DRF endpoints using Bearer token
- Latest prompt update (Home + Admin page naming):
  - added explicit Home page at `/`
  - moved product listing to `/products`
  - added explicit Admin page route `/admin-page` (kept `/manage` alias)
- Latest prompt update (admin-only management flow):
  - removed add category/product forms from `/admin-page` and kept login-only there
  - created separate `/admin-tools` page with add category and add product forms
  - added role check (`is_admin`/`is_staff`) after login and restricted write APIs to admins only
- Latest prompt update (login UX refinement):
  - navbar now shows only `Login` (no direct Admin/Admin Tools links)
  - `/login` now displays role choice: `Admin Login` and `Customer Login`
  - admin path requires admin account then redirects to `/admin-tools`; customer path redirects to `/products`
- Latest prompt update (admin navbar theme + responsive):
  - added a separate admin-themed navbar after admin login
  - added responsive mobile navigation toggle behavior
  - integrated quick logout action in admin navbar
- Latest prompt update (admin product dashboard editing):
  - admin tools now load all existing products in editable cards
  - admin can update product name, description, stock, price, category, and image
  - each product has per-item save action powered by `PATCH /api/products/<id>/`
- Latest prompt update (dashboard shift):
  - admin management tools are now shifted to admin dashboard route (`/`) after admin login
  - removed admin tools entry from navbar; admin navbar now focuses on dashboard and catalog
- Latest prompt update (full admin panel redesign):
  - rebuilt admin dashboard layout with left sidebar + overview topbar + metric cards + analytics panel
  - applied a mint/teal themed visual system inspired by provided reference screenshot
  - kept full admin capabilities for add/edit product/category inside redesigned sections
- Latest prompt update (products vs inventory separation):
  - Products section is now dedicated to adding category and adding product only
  - Inventory section is now dedicated to stock management only
  - stock updates are saved via product PATCH with stock field only
- Latest prompt update (basic admin panel):
  - simplified admin dashboard to two basic areas only: `Product` and `Stock`
  - removed extra analytics/overview widgets from admin tools UI
  - kept stock update workflow as single-field stock save per product
- Latest prompt update (customer auth + login audit):
  - added customer signup option on login page using `/api/users/register/`
  - added dedicated customer JWT endpoint `/api/users/customer-login/`
  - added DB model `CustomerLoginActivity` to store customer login audit entries
- Latest prompt update (login/signup page split):
  - login page is now login-only
  - added single `Sign Up` button on login page that routes to customer signup page
  - moved customer account creation form to `/customer-signup`
- Latest prompt update (template cleanup):
  - removed frontend template usage from active app flow
  - kept minimal Django `TEMPLATES` config only for Django admin compatibility
  - converted legacy cart template response to JSON to avoid template dependency
- Latest prompt update (admin recent actions):
  - added admin-only API endpoints for recent actions list and clear actions
  - added Recent Actions section in admin dashboard with optional `Clear Activity` control
  - actions are scoped to current admin user log entries
- Latest prompt update (API action activity logging):
  - added `AdminActivity` model to store API-driven admin operations
  - product/category create, update, delete and stock updates are now logged as admin recent activity
  - recent actions endpoint now reads from `AdminActivity` for accurate dashboard actions history
- Latest prompt update (category option restore):
  - restored Add Category option in basic admin panel
  - admin panel now includes both Add Category and Add Product plus Stock management
