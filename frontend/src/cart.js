const STORAGE_KEY = "ecommerce_cart_v1";

export function loadCart() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

export function saveCart(cartItems) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(cartItems));
}

export function addItem(cartItems, product) {
  const existing = cartItems.find((item) => item.id === product.id);
  if (existing) {
    return cartItems.map((item) =>
      item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
    );
  }

  return [
    ...cartItems,
    {
      id: product.id,
      name: product.name,
      price: Number(product.price),
      image: product.image || "",
      quantity: 1,
    },
  ];
}

export function removeItem(cartItems, productId) {
  return cartItems.filter((item) => item.id !== productId);
}

export function clearCart() {
  localStorage.removeItem(STORAGE_KEY);
}
