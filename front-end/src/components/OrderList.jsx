import React, { useState, useEffect } from "react";
import axios from "axios";

export default function OrderList() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch all orders
  const fetchOrders = async () => {
    try {
      const response = await axios.get("http://localhost:5000/orders");
      setOrders(response.data);
    } catch (err) {
      console.error(err);
      setError("Failed to load orders");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  // Delete an order
  const handleDelete = async (orderId) => {
    if (!window.confirm("Are you sure you want to delete this order?")) return;

    try {
      await axios.delete(`http://localhost:5000/orders/${orderId}`);
      // Remove from frontend state
      setOrders(orders.filter((o) => o.id !== orderId));
    } catch (err) {
      console.error(err);
      alert("Failed to delete order");
    }
  };

  // Confirm an order
  const handleConfirm = async (orderId) => {
    try {
      const order = orders.find((o) => o.id === orderId);
      const updated = { ...order, status: "confirmed" };
      await axios.put(`http://localhost:5000/orders/${orderId}`, updated);
      fetchOrders(); // Refresh list
    } catch (err) {
      console.error(err);
      alert("Failed to confirm order");
    }
  };

  // Complete an order
  const handleComplete = async (orderId) => {
    try {
      const order = orders.find((o) => o.id === orderId);
      const updated = { ...order, status: "completed" };
      await axios.put(`http://localhost:5000/orders/${orderId}`, updated);
      fetchOrders();
    } catch (err) {
      console.error(err);
      alert("Failed to complete order");
    }
  };

  if (loading) return <p>Loading orders...</p>;
  if (error) return <p>{error}</p>;
  if (orders.length === 0) return <p>No orders found.</p>;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      {orders.map((order) => (
        <div
          key={order.id}
          style={{ border: "1px solid #ccc", borderRadius: "8px", padding: "1rem" }}
        >
          <h3>Order #{order.id}</h3>
          <p><strong>Customer:</strong> {order.customer_name}</p>
          <p><strong>Phone:</strong> {order.customer_phone || "N/A"}</p>
          <p><strong>Status:</strong> {order.status}</p>
          <p><strong>Order Date:</strong> {new Date(order.order_date).toLocaleString()}</p>

          <h4>Bulls in Order:</h4>
          {order.order_items && order.order_items.length > 0 ? (
            order.order_items.map((item) => (
              <div
                key={item.bull?.id || item.id}
                style={{ border: "1px solid #ddd", padding: "0.5rem", marginBottom: "0.5rem" }}
              >
                <p>Bull: {item.bull?.name || "Unknown Bull"}</p>
                <p>Quantity: {item.quantity}</p>
                <p>Price: ${item.price_at_order}</p>
              </div>
            ))
          ) : (
            <p>No bulls in this order</p>
          )}

          {/* CRUD Buttons */}
          <div style={{ marginTop: "0.5rem", display: "flex", gap: "0.5rem" }}>
            <button onClick={() => handleConfirm(order.id)}>Confirm</button>
            <button onClick={() => handleComplete(order.id)}>Complete</button>
            <button onClick={() => handleDelete(order.id)} style={{ color: "red" }}>Delete</button>
          </div>
        </div>
      ))}
    </div>
  );
}
