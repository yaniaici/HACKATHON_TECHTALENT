// API central para todos los recursos del backend
const API_BASE = "http://localhost:5000";

// Función helper para manejo de respuestas
const handleResponse = async (response: Response) => {
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  const data = await response.json();
  return data;
};

// Función helper para manejo de errores
const handleError = (error: any) => {
  console.error('API Error:', error);
  return { success: false, message: error.message || 'Error en la comunicación con el servidor' };
};

// --- USUARIOS ---
export async function getUsuarios() {
  try {
    const res = await fetch(`${API_BASE}/usuario`);
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function createUsuario(data: any) {
  try {
    const res = await fetch(`${API_BASE}/usuario`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function updateUsuario(usuario_id: number, data: any) {
  try {
    const res = await fetch(`${API_BASE}/usuario/${usuario_id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function deleteUsuario(usuario_id: number) {
  try {
    const res = await fetch(`${API_BASE}/usuario/${usuario_id}`, { method: 'DELETE' });
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

// --- PRODUCTOS ---
export async function getProductos() {
  try {
    const res = await fetch(`${API_BASE}/producto`);
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function createProducto(data: any) {
  try {
    const res = await fetch(`${API_BASE}/producto`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function updateProducto(producto_id: number, data: any) {
  try {
    const res = await fetch(`${API_BASE}/producto/${producto_id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function deleteProducto(producto_id: number) {
  try {
    const res = await fetch(`${API_BASE}/producto/${producto_id}`, { method: 'DELETE' });
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

// --- PEDIDOS ---
export async function getPedidos() {
  try {
    const res = await fetch(`${API_BASE}/pedido`);
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function createPedido(data: any) {
  try {
    const res = await fetch(`${API_BASE}/pedido`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function getPedidoById(pedido_id: number) {
  try {
    const res = await fetch(`${API_BASE}/pedido/${pedido_id}`);
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function updatePedido(pedido_id: number, data: any) {
  try {
    const res = await fetch(`${API_BASE}/pedido/${pedido_id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function deletePedido(pedido_id: number) {
  try {
    const res = await fetch(`${API_BASE}/pedido/${pedido_id}`, { method: 'DELETE' });
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

// --- AUTH ---
export async function login(data: any) {
  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

// --- CHATBOT ---
export async function chatbotQuery(data: any) {
  try {
    const res = await fetch(`${API_BASE}/chatbot/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function chatbotSearch(q: string) {
  try {
    const res = await fetch(`${API_BASE}/chatbot/search?q=${encodeURIComponent(q)}`);
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function chatbotCreateOrder(data: any) {
  try {
    const res = await fetch(`${API_BASE}/chatbot/create-order`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function chatbotGetProductsByType(product_type: string) {
  try {
    const res = await fetch(`${API_BASE}/chatbot/products/${product_type}`);
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function chatbotGetProductsByOrigin(origin: string) {
  try {
    const res = await fetch(`${API_BASE}/chatbot/products/origin/${origin}`);
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function chatbotGetProductsNoAllergens() {
  try {
    const res = await fetch(`${API_BASE}/chatbot/products/no-allergens`);
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function chatbotGetOrdersByStatus(status: string) {
  try {
    const res = await fetch(`${API_BASE}/chatbot/orders/${status}`);
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function chatbotGetStats() {
  try {
    const res = await fetch(`${API_BASE}/chatbot/stats`);
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function chatbotTestConnection() {
  try {
    const res = await fetch(`${API_BASE}/chatbot/test-connection`);
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

// --- STOCK ---
export async function getProductoStock(producto_id: number) {
  try {
    const res = await fetch(`${API_BASE}/stock/producto/${producto_id}`);
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function updateProductoStock(producto_id: number, data: any) {
  try {
    const res = await fetch(`${API_BASE}/stock/producto/${producto_id}/ajuste`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function getProductosStockBajo() {
  try {
    const res = await fetch(`${API_BASE}/stock/productos/stock-bajo`);
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function getMovimientosStock() {
  try {
    const res = await fetch(`${API_BASE}/stock/movimientos`);
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
}

export async function verificarStockDisponible(producto_id: number) {
  try {
    const res = await fetch(`${API_BASE}/stock/verificar/${producto_id}`);
    return await handleResponse(res);
  } catch (error) {
    return handleError(error);
  }
} 