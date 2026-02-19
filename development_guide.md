# E-Commerce Development Guide

> [!CAUTION]
> **STRICT RULE: NO PUSH TO GITHUB**
> Do not push any code to GitHub repositories. All commits must remain local.

## 📂 Project Structure

### Core Apps
- **`e_commerce/`**: Main project configuration (`settings.py`, `urls.py`).
- **`products/`**: Product catalog, categories, and inventory management.
- **`cart/`**: Shopping cart functionality (session-based).
- **`orders/`**: Order processing and history.
- **`users/`**: User authentication and profiles.

### Static & Templates
- **`static/css/`**:
  - `style.css`: Main frontend styles (Responsive, CSS Variables).
  - `admin_custom.css`: Django Admin overrides (matches main theme).
- **`templates/`**:
  - `base.html`: Main layout (Navbar, Footer, Theme Logic).
  - `admin/base_site.html`: Admin dashboard override (Theme Toggle).
  - `products/`: Product list and detail templates.
  - `cart/`: Cart templates.

---

## 🎨 Theme & Components

### 1. Global Theme System (`style.css`)
The site uses a native CSS variable system for theming.
- **Light Mode (Default)**: Defined in `:root`. Uses Lavender/White palette with Purple accents.
- **Dark Mode**: Defined in `[data-theme="dark"]`. Uses Deep Blue/Purple palette.
- **CSS Variables**: Use `var(--color-name)` for all styling.
  - Backgrounds: `--bg-primary`, `--bg-card`, `--bg-navbar`
  - Text: `--text-primary`, `--text-secondary`
  - Accents: `--accent-primary`, `--accent-gradient`

### 2. Theme Toggle Component
Located in `templates/base.html` (Navbar).
- **HTML**: `<button class="theme-toggle">...</button>`
- **Logic**:
  - Inline script in `<head>` reads `localStorage['eshop-theme']` to prevent flash.
  - Toggles `data-theme` attribute on `<html>` tag.
  - Persists preference to `localStorage`.

### 3. Admin Panel Customization
Located in `templates/admin/base_site.html` & `static/css/admin_custom.css`.
- **Goal**: Match the main site aesthetics without external packages.
- **Features**:
  - **Toggle**: Added to the admin header (User Tools section).
  - **Variables**: `admin_custom.css` maps the main site's CSS variables to Django admin selectors.
  - **No Jazzmin**: Pure Django template overrides for stability.

---

## 🛠️ Development Workflow

1.  **Adding New Components**:
    -   Create HTML structure in `templates/`.
    -   Style using **CSS Variables** from `style.css` (do not hardcode colors).
    -   **Update this guide** with the new component's details.

2.  **Modifying Theme**:
    -   Update `:root` for Light Mode changes.
    -   Update `[data-theme="dark"]` for Dark Mode changes.

3.  **Commit Protocol**:
    -   `git add .`
    -   `git commit -m "feat: description"`
    -   **NEVER RUN `git push`**.
