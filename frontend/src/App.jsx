import { useEffect, useMemo, useState } from "react";
import { Link, Route, Routes, useNavigate, useParams } from "react-router-dom";
import {
  createProduct,
  clearAdminRecentActions,
  getAdminRecentActions,
  getCurrentUser,
  getCategories,
  getProductById,
  getProducts,
  login,
  loginCustomer,
  registerCustomer,
  updateProduct,
} from "./api";
import { addItem, clearCart, loadCart, removeItem, saveCart } from "./cart";

function Layout({ cartCount, isLoggedIn, isAdmin, onLogout, username, children }) {
  const [menuOpen, setMenuOpen] = useState(false);

  function closeMenu() {
    setMenuOpen(false);
  }

  return (
    <div className="app">
      <header className={`header ${isAdmin ? "header-admin" : ""}`}>
        <div className="container nav">
          <Link to="/" className="brand">
            E-Shop
          </Link>
          <button
            className="menu-toggle"
            type="button"
            onClick={() => setMenuOpen((prev) => !prev)}
            aria-label="Toggle navigation menu"
          >
            Menu
          </button>
          <nav className={`menu ${menuOpen ? "open" : ""}`}>
            {isAdmin ? (
              <>
                <Link to="/" onClick={closeMenu}>
                  Dashboard
                </Link>
                <Link to="/products" onClick={closeMenu}>
                  Catalog
                </Link>
                <span className="status admin-badge">
                  Admin: {username || "user"}
                </span>
                <button
                  className="nav-link-button"
                  type="button"
                  onClick={() => {
                    onLogout();
                    closeMenu();
                  }}
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/" onClick={closeMenu}>
                  Home
                </Link>
                <Link to="/products" onClick={closeMenu}>
                  Products
                </Link>
                <Link to="/cart" onClick={closeMenu}>
                  Cart ({cartCount})
                </Link>
                <Link to="/login" onClick={closeMenu}>
                  Login
                </Link>
                <span className="status">{isLoggedIn ? "Logged In" : "Guest"}</span>
              </>
            )}
          </nav>
        </div>
      </header>
      <main className="container">{children}</main>
    </div>
  );
}

function HomePage() {
  return (
    <section className="home">
      <div className="home-hero">
        <p className="home-kicker">React Storefront</p>
        <h1>Welcome to E-Shop</h1>
        <p className="home-text">
          Browse products, manage your cart, and use the admin page to add
          categories and products.
        </p>
        <div className="actions">
          <Link className="btn" to="/products">
            Shop Now
          </Link>
          <Link className="btn secondary" to="/login">
            Login
          </Link>
        </div>
      </div>
    </section>
  );
}

function ProductListPage({ onAddToCart }) {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [categoryId, setCategoryId] = useState("all");

  useEffect(() => {
    async function loadData() {
      try {
        const [productsData, categoriesData] = await Promise.all([
          getProducts(),
          getCategories(),
        ]);
        setProducts(productsData);
        setCategories(categoriesData);
      } catch (err) {
        setError(err.message || "Failed to load products");
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const filtered = useMemo(() => {
    return products.filter((product) => {
      const matchesQuery =
        product.name.toLowerCase().includes(query.toLowerCase()) ||
        product.description.toLowerCase().includes(query.toLowerCase());
      const matchesCategory =
        categoryId === "all" || String(product.category) === categoryId;
      return matchesQuery && matchesCategory;
    });
  }, [products, query, categoryId]);

  if (loading) return <p className="state">Loading products...</p>;
  if (error) return <p className="state error">{error}</p>;

  return (
    <section>
      <h1>Products</h1>

      <div className="filters">
        <input
          type="text"
          placeholder="Search products..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        <select
          value={categoryId}
          onChange={(e) => setCategoryId(e.target.value)}
        >
          <option value="all">All categories</option>
          {categories.map((category) => (
            <option key={category.id} value={String(category.id)}>
              {category.name}
            </option>
          ))}
        </select>
      </div>

      <div className="grid">
        {filtered.map((product) => (
          <article className="card" key={product.id}>
            <Link to={`/product/${product.id}`} className="card-image-wrap">
              {product.image ? (
                <img src={product.image} alt={product.name} className="card-image" />
              ) : (
                <div className="card-image placeholder">No Image</div>
              )}
            </Link>
            <h2>{product.name}</h2>
            <p>{product.description}</p>
            <p className="price">${Number(product.price).toFixed(2)}</p>
            <div className="actions">
              <Link className="btn secondary" to={`/product/${product.id}`}>
                Details
              </Link>
              <button className="btn" onClick={() => onAddToCart(product)}>
                Add to cart
              </button>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function ProductDetailPage({ onAddToCart }) {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getProductById(id);
        setProduct(data);
      } catch (err) {
        setError(err.message || "Failed to load product");
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [id]);

  if (loading) return <p className="state">Loading product...</p>;
  if (error) return <p className="state error">{error}</p>;
  if (!product) return <p className="state">Product not found.</p>;

  return (
    <section className="detail">
      {product.image ? (
        <img src={product.image} alt={product.name} className="detail-image" />
      ) : (
        <div className="detail-image placeholder">No Image</div>
      )}
      <div>
        <h1>{product.name}</h1>
        <p className="detail-desc">{product.description}</p>
        <p className="price">${Number(product.price).toFixed(2)}</p>
        <p>Stock: {product.stock}</p>
        <button className="btn" onClick={() => onAddToCart(product)}>
          Add to cart
        </button>
      </div>
    </section>
  );
}

function CartPage({ cartItems, onRemoveItem, onCheckout }) {
  const total = cartItems.reduce(
    (sum, item) => sum + Number(item.price) * Number(item.quantity),
    0
  );

  return (
    <section>
      <h1>Your Cart</h1>

      {cartItems.length === 0 ? (
        <p className="state">Your cart is empty.</p>
      ) : (
        <>
          <div className="cart-list">
            {cartItems.map((item) => (
              <article className="cart-item" key={item.id}>
                <div>
                  <h2>{item.name}</h2>
                  <p>
                    {item.quantity} x ${Number(item.price).toFixed(2)}
                  </p>
                </div>
                <button className="btn danger" onClick={() => onRemoveItem(item.id)}>
                  Remove
                </button>
              </article>
            ))}
          </div>
          <p className="cart-total">Total: ${total.toFixed(2)}</p>
          <button className="btn" onClick={onCheckout}>
            Checkout
          </button>
        </>
      )}
    </section>
  );
}

function LoginPage({ onLoginSuccess, onLogout, isLoggedIn, isAdmin }) {
  const navigate = useNavigate();
  const [role, setRole] = useState("customer");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function handleLogin(event) {
    event.preventDefault();
    setMessage("");
    setError("");
    try {
      const result =
        role === "admin"
          ? await login(username, password)
          : await loginCustomer(username, password);
      const user = await getCurrentUser(result.access);
      const userIsAdmin = Boolean(user.is_admin || user.is_staff);

      if (role === "admin") {
        if (!userIsAdmin) {
          setError("This account is not admin. Use Customer Login.");
          return;
        }
        onLoginSuccess(result.access, user);
        setPassword("");
        setMessage("Admin login successful.");
        navigate("/");
      } else {
        onLoginSuccess(result.access, user);
        setPassword("");
        setMessage("Customer login successful.");
        navigate("/products");
      }
    } catch (err) {
      setError(err.message || "Login failed. Check username/password.");
    }
  }

  return (
    <section>
      <h1>Login</h1>
      <p className="state">
        Choose login type first. Admin users can access admin tools after login.
      </p>
      {message ? <p className="state">{message}</p> : null}
      {error ? <p className="state error">{error}</p> : null}

      <div className="manage-grid single">
        <form className="panel" onSubmit={handleLogin}>
          <h2>{role === "admin" ? "Admin Login" : "Customer Login"}</h2>
          <div className="role-toggle">
            <button
              type="button"
              className={`btn ${role === "admin" ? "" : "secondary"}`}
              onClick={() => setRole("admin")}
            >
              Admin Login
            </button>
            <button
              type="button"
              className={`btn ${role === "customer" ? "" : "secondary"}`}
              onClick={() => setRole("customer")}
            >
              Customer Login
            </button>
          </div>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <div className="actions">
            <button className="btn" type="submit">
              Login
            </button>
            <button
              className="btn secondary"
              type="button"
              onClick={() => navigate("/customer-signup")}
            >
              Sign Up
            </button>
            <button className="btn secondary" type="button" onClick={onLogout}>
              Logout
            </button>
          </div>
          <p className="muted">
            Status:{" "}
            {isLoggedIn ? (isAdmin ? "Logged in as admin" : "Logged in as customer") : "Not logged in"}
          </p>
        </form>
      </div>
    </section>
  );
}

function CustomerSignupPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function handleSignup(event) {
    event.preventDefault();
    setMessage("");
    setError("");
    try {
      await registerCustomer({ username, email, password });
      setMessage("Account created successfully. You can now login.");
      setUsername("");
      setEmail("");
      setPassword("");
    } catch (err) {
      setError(err.message || "Could not create account. Try a different username/email.");
    }
  }

  return (
    <section>
      <h1>Customer Sign Up</h1>
      {message ? <p className="state">{message}</p> : null}
      {error ? <p className="state error">{error}</p> : null}
      <div className="manage-grid single">
        <form className="panel" onSubmit={handleSignup}>
          <h2>Create Account</h2>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <div className="actions">
            <button className="btn" type="submit">
              Create Account
            </button>
            <button
              className="btn secondary"
              type="button"
              onClick={() => navigate("/login")}
            >
              Back to Login
            </button>
          </div>
        </form>
      </div>
    </section>
  );
}

function AdminToolsPage({ token, isAdmin }) {
  const [categories, setCategories] = useState([]);
  const [products, setProducts] = useState([]);
  const [productForm, setProductForm] = useState({
    name: "",
    description: "",
    price: "",
    stock: "",
    category: "",
    image: null,
  });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [savingProductId, setSavingProductId] = useState(null);
  const [recentActions, setRecentActions] = useState([]);
  const [clearingActions, setClearingActions] = useState(false);

  useEffect(() => {
    async function loadData() {
      try {
        const [categoriesData, productsData] = await Promise.all([
          getCategories(),
          getProducts(),
        ]);
        setCategories(categoriesData);
        setProducts(
          productsData.map((product) => ({
            id: product.id,
            name: product.name,
            description: product.description,
            price: String(product.price),
            stock: String(product.stock),
            category: String(product.category),
            image: product.image || "",
            newImage: null,
          }))
        );
        setProductForm((prev) =>
          prev.category || categoriesData.length === 0
            ? prev
            : { ...prev, category: String(categoriesData[0].id) }
        );
        const actionsData = await getAdminRecentActions(token);
        setRecentActions(actionsData);
      } catch (err) {
        setCategories([]);
        setProducts([]);
        setError(err.message || "Could not load categories.");
      }
    }
    if (isAdmin && token) {
      loadData();
    }
  }, [isAdmin, token]);

  async function handleAddProduct(event) {
    event.preventDefault();
    setMessage("");
    setError("");
    if (!token || !isAdmin) {
      setError("Only admin users can modify store data.");
      return;
    }
    try {
      const created = await createProduct(productForm, token);
      setMessage("Product added.");
      setProductForm({
        name: "",
        description: "",
        price: "",
        stock: "",
        category: categories.length ? String(categories[0].id) : "",
        image: null,
      });
      setProducts((prev) => [
        ...prev,
        {
          id: created.id,
          name: created.name,
          description: created.description,
          price: String(created.price),
          stock: String(created.stock),
          category: String(created.category),
          image: created.image || "",
          newImage: null,
        },
      ]);
    } catch {
      setError("Could not add product.");
    }
  }

  function handleEditChange(productId, field, value) {
    setProducts((prev) =>
      prev.map((product) =>
        product.id === productId ? { ...product, [field]: value } : product
      )
    );
  }

  async function handleSaveStock(productId) {
    setMessage("");
    setError("");
    if (!token || !isAdmin) {
      setError("Only admin users can modify store data.");
      return;
    }

    const target = products.find((product) => product.id === productId);
    if (!target) return;

    setSavingProductId(productId);
    try {
      const updated = await updateProduct(
        productId,
        {
          stock: target.stock,
        },
        token
      );
      setProducts((prev) =>
        prev.map((product) =>
          product.id === productId
            ? {
                ...product,
                stock: String(updated.stock),
              }
            : product
        )
      );
      setMessage(`Stock updated for product #${productId}.`);
    } catch {
      setError(`Could not update stock for product #${productId}.`);
    } finally {
      setSavingProductId(null);
    }
  }

  async function handleClearActions() {
    if (!token || !isAdmin) return;
    setClearingActions(true);
    setMessage("");
    setError("");
    try {
      const result = await clearAdminRecentActions(token);
      setRecentActions([]);
      setMessage(`Cleared ${result.cleared} recent action(s).`);
    } catch (err) {
      setError(err.message || "Could not clear actions.");
    } finally {
      setClearingActions(false);
    }
  }

  return (
    <section>
      <h1>Admin Dashboard</h1>
      {!isAdmin ? <p className="state error">Access denied. Login as admin from the Login page.</p> : null}
      {message ? <p className="state">{message}</p> : null}
      {error ? <p className="state error">{error}</p> : null}

      <div className="manage-grid">
        <form className="panel" onSubmit={handleAddProduct}>
          <h2>Product</h2>
          <input
            type="text"
            placeholder="Product name"
            value={productForm.name}
            onChange={(e) => setProductForm((prev) => ({ ...prev, name: e.target.value }))}
            required
          />
          <textarea
            placeholder="Description"
            value={productForm.description}
            onChange={(e) =>
              setProductForm((prev) => ({ ...prev, description: e.target.value }))
            }
            rows={3}
            required
          />
          <input
            type="number"
            placeholder="Price"
            step="0.01"
            value={productForm.price}
            onChange={(e) => setProductForm((prev) => ({ ...prev, price: e.target.value }))}
            required
          />
          <input
            type="number"
            placeholder="Stock"
            value={productForm.stock}
            onChange={(e) => setProductForm((prev) => ({ ...prev, stock: e.target.value }))}
            required
          />
          <select
            value={productForm.category}
            onChange={(e) => setProductForm((prev) => ({ ...prev, category: e.target.value }))}
            required
          >
            <option value="" disabled>
              Select category
            </option>
            {categories.map((category) => (
              <option key={category.id} value={String(category.id)}>
                {category.name}
              </option>
            ))}
          </select>
          <input
            type="file"
            accept="image/*"
            onChange={(e) =>
              setProductForm((prev) => ({ ...prev, image: e.target.files?.[0] || null }))
            }
          />
          <button className="btn" type="submit" disabled={!isAdmin}>
            Add Product
          </button>
        </form>
      </div>

      <section className="admin-products" id="inventory">
        <h2>Stock</h2>
        <p className="muted">Stock management only.</p>
        <div className="manage-grid">
          {products.map((product) => (
            <article className="panel" key={product.id}>
              <h3>
                #{product.id} {product.name}
              </h3>
              <p className="muted">Current Stock</p>
              <input
                type="number"
                value={product.stock}
                onChange={(e) => handleEditChange(product.id, "stock", e.target.value)}
                disabled={!isAdmin}
              />
              <button
                className="btn"
                type="button"
                onClick={() => handleSaveStock(product.id)}
                disabled={!isAdmin || savingProductId === product.id}
              >
                {savingProductId === product.id ? "Saving..." : "Save Stock"}
              </button>
            </article>
          ))}
        </div>
      </section>

      <section className="admin-products">
        <div className="admin-actions-head">
          <h2>Recent Actions</h2>
          <button
            className="btn secondary"
            type="button"
            onClick={handleClearActions}
            disabled={!isAdmin || clearingActions}
          >
            {clearingActions ? "Clearing..." : "Clear Activity"}
          </button>
        </div>
        {recentActions.length === 0 ? (
          <p className="state">No recent actions found.</p>
        ) : (
          <div className="manage-grid">
            {recentActions.map((action) => (
              <article className="panel" key={action.id}>
                <h3>{action.object_repr}</h3>
                <p className="muted">
                  {action.app_label}.{action.model}
                </p>
                <p>{action.change_message}</p>
                <p className="muted">{new Date(action.action_time).toLocaleString()}</p>
              </article>
            ))}
          </div>
        )}
      </section>
    </section>
  );
}

export default function App() {
  const [cartItems, setCartItems] = useState(loadCart);
  const [authToken, setAuthToken] = useState(() => localStorage.getItem("auth_token") || "");
  const [authUser, setAuthUser] = useState(() => {
    const raw = localStorage.getItem("auth_user");
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch {
      return null;
    }
  });

  useEffect(() => {
    saveCart(cartItems);
  }, [cartItems]);

  useEffect(() => {
    if (authToken) {
      localStorage.setItem("auth_token", authToken);
    } else {
      localStorage.removeItem("auth_token");
    }
  }, [authToken]);

  useEffect(() => {
    if (authUser) {
      localStorage.setItem("auth_user", JSON.stringify(authUser));
    } else {
      localStorage.removeItem("auth_user");
    }
  }, [authUser]);

  function handleLoginSuccess(token, user) {
    setAuthToken(token);
    setAuthUser(user);
  }

  function handleLogout() {
    setAuthToken("");
    setAuthUser(null);
  }

  function handleAddToCart(product) {
    setCartItems((prev) => addItem(prev, product));
  }

  function handleRemoveItem(productId) {
    setCartItems((prev) => removeItem(prev, productId));
  }

  function handleCheckout() {
    clearCart();
    setCartItems([]);
  }

  const cartCount = cartItems.reduce((sum, item) => sum + item.quantity, 0);
  const isAdmin = Boolean(authUser && (authUser.is_admin || authUser.is_staff));

  return (
    <Layout
      cartCount={cartCount}
      isLoggedIn={Boolean(authToken)}
      isAdmin={isAdmin}
      onLogout={handleLogout}
      username={authUser?.username}
    >
      <Routes>
        <Route
          path="/"
          element={
            isAdmin ? (
              <AdminToolsPage token={authToken} isAdmin={isAdmin} />
            ) : (
              <HomePage />
            )
          }
        />
        <Route
          path="/products"
          element={<ProductListPage onAddToCart={handleAddToCart} />}
        />
        <Route
          path="/product/:id"
          element={<ProductDetailPage onAddToCart={handleAddToCart} />}
        />
        <Route
          path="/cart"
          element={
            <CartPage
              cartItems={cartItems}
              onRemoveItem={handleRemoveItem}
              onCheckout={handleCheckout}
            />
          }
        />
        <Route
          path="/login"
          element={
            <LoginPage
              onLoginSuccess={handleLoginSuccess}
              onLogout={handleLogout}
              isLoggedIn={Boolean(authToken)}
              isAdmin={isAdmin}
            />
          }
        />
        <Route path="/customer-signup" element={<CustomerSignupPage />} />
        <Route
          path="/admin-tools"
          element={
            <AdminToolsPage
              token={authToken}
              isAdmin={isAdmin}
            />
          }
        />
        <Route
          path="/admin-page"
          element={
            <LoginPage
              onLoginSuccess={handleLoginSuccess}
              onLogout={handleLogout}
              isLoggedIn={Boolean(authToken)}
              isAdmin={isAdmin}
            />
          }
        />
        <Route
          path="/manage"
          element={
            <LoginPage
              onLoginSuccess={handleLoginSuccess}
              onLogout={handleLogout}
              isLoggedIn={Boolean(authToken)}
              isAdmin={isAdmin}
            />
          }
        />
      </Routes>
    </Layout>
  );
}
