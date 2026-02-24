const API_BASE = import.meta.env.VITE_API_BASE || "";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options);
  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    if (payload && typeof payload === "object") {
      const first = Object.values(payload)[0];
      const detail = Array.isArray(first) ? first[0] : first;
      throw new Error(detail || `Request failed: ${response.status}`);
    }
    throw new Error(payload || `Request failed: ${response.status}`);
  }

  return payload || null;
}

export function getProducts() {
  return request("/api/products/");
}

export function getCategories() {
  return request("/api/categories/");
}

export function getProductById(id) {
  return request(`/api/products/${id}/`);
}

export function login(username, password) {
  return request("/api/users/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });
}

export function loginCustomer(username, password) {
  return request("/api/users/customer-login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });
}

export function registerCustomer(payload) {
  return request("/api/users/register/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export function getCurrentUser(token) {
  return request("/api/users/me/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export function createCategory(name, token) {
  return request("/api/categories/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ name }),
  });
}

export function createProduct(payload, token) {
  const formData = new FormData();
  formData.append("name", payload.name);
  formData.append("description", payload.description);
  formData.append("price", payload.price);
  formData.append("stock", payload.stock);
  formData.append("category", payload.category);
  if (payload.image) {
    formData.append("image", payload.image);
  }

  return request("/api/products/", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });
}

export function updateProduct(productId, payload, token) {
  const formData = new FormData();
  if (payload.name !== undefined) formData.append("name", payload.name);
  if (payload.description !== undefined) formData.append("description", payload.description);
  if (payload.price !== undefined) formData.append("price", payload.price);
  if (payload.stock !== undefined) formData.append("stock", payload.stock);
  if (payload.category !== undefined) formData.append("category", payload.category);
  if (payload.image instanceof File) {
    formData.append("image", payload.image);
  }

  return request(`/api/products/${productId}/`, {
    method: "PATCH",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });
}
