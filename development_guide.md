# E-Commerce Development Guide

> [!CAUTION]
> **STRICT RESTRICTION: NO GIT / GITHUB INTERACTIONS**
> 1. **Do NOT run `git push`, `git pull`, `git clone`, or `gh` commands**.
> 2. **Avoid `git` commands** entirely if possible to prevent accidental remote interactions.
> 3. **LOCAL ONLY**: This project is strictly local.

## Project Structure

### Core Apps
- `e_commerce/`: Main project configuration (`settings.py`, `urls.py`).
- `products/`: Product catalog, categories, and inventory management.
- `cart/`: Shopping cart functionality (session-based).
- `orders/`: Order processing and history.
- `users/`: User authentication and profiles.

### Static and Templates
- `static/css/`
  - `style.css`: Main storefront styles (theme system, product rows, responsive layout).
  - `admin_custom.css`: Admin-only overrides for theme parity and responsive dashboard layout.
- `templates/`
  - `base.html`: Main storefront layout (navbar, footer, theme toggle logic).
  - `admin/base_site.html`: Admin navbar override and admin theme toggle.
  - `products/product_list.html`: Home page product list in row format.
  - `products/product_detail.html`: Product detail page.
  - `cart/cart_detail.html`: Cart view.

---

## Theme System

### Global Theme Tokens (`static/css/style.css`)
The storefront uses CSS variables with light mode as default:
- `:root` = light palette.
- `[data-theme="dark"]` = dark overrides.

Use variables for all new colors:
- Backgrounds: `--bg-primary`, `--bg-card`, `--bg-navbar`
- Text: `--text-primary`, `--text-secondary`, `--text-muted`
- Brand: `--accent-primary`, `--accent-secondary`, `--accent-gradient`
- Borders/effects: `--border-color`, `--border-subtle`, `--shadow-card`
- **Layout**: `--page-width` (Default: 1250px) - Controls max-width of main containers in both Storefront and Admin.

### Theme Toggle
- Storefront toggle is in `templates/base.html`.
- Admin toggle is in `templates/admin/base_site.html`.
- Both toggles persist to `localStorage['eshop-theme']` and set `data-theme` on `<html>`.

### Adding New Theme Variables
1. Define in `:root` (light value).
2. Define matching override in `[data-theme="dark"]`.
3. Use `var(--token-name)` in styles.
4. Mirror needed admin tokens in `static/css/admin_custom.css`.

---

## 💎 Component Analysis: Header (Navbar)

The Home Page header (`templates/base.html`) features a premium, clean design using **Glassmorphism**.

### Structure
- **Container**: `<nav class="navbar">` (Flexbox container).
- **Brand**: `.navbar-brand` (Gradient text, left-aligned).
- **Links**: `.navbar-nav` (Center/Right-aligned links).
- **Toggle**: `.theme-toggle` (Day/Night switch).

### Styling (`style.css`)
- **Glassmorphism**: `backdrop-filter: blur(20px)` + Semi-transparent background (`var(--bg-navbar)`).
- **Sticky**: `position: sticky; top: 0` ensures navigation is always available.
- **Dimensions**: Fixed height (`70px`).
- **Z-Index**: `1000` (Stays on top).

---

## Home Page Layout

### Product Row Format (`templates/products/product_list.html`)
The home page now renders products as horizontal rows instead of a centered card/grid:
- Left: image/placeholder.
- Middle: category, title, description.
- Right: price and actions (`Add to Cart`, `View Details`).

Related CSS lives in `static/css/style.css`:
- `.products-row-list`
- `.product-row`
- `.product-row-media`
- `.product-row-main`
- `.product-row-right`
- `.product-row-actions`

Responsive behavior:
- Desktop: 3-column row structure.
- Tablet: media + content with actions moved below.
- Mobile: stacked single-column rows.

---

## Admin UI Enhancements

### Responsive and Attractive Dashboard (`static/css/admin_custom.css`)
Admin dashboard improvements include:
- Two-column dashboard structure on desktop (`#content-main` + `#content-related`).
- Sticky recent-actions panel on larger screens.
- Better module/table spacing, hover states, and card feel.
- Mobile breakpoints for navbar, toggle, and compact table spacing.

Key selectors:
- `.dashboard #content`
- `.dashboard #content-main`
- `.dashboard #content-related`
- `#recent-actions-module .actionlist li`

---

## Development Workflow

1. Build UI in templates first, then style via global tokens.
2. Avoid hard-coded colors when theme variables can be used.
3. Ensure both storefront and admin remain responsive at `1100px`, `900px`, and `640px` breakpoints.
4. Update this guide whenever component structure or theme behavior changes.

## Commit Protocol

- `git add .`
- `git commit -m "feat: description"`
- Never run `git push`.
