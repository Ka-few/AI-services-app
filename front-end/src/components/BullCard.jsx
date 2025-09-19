import React from "react";

export default function BullCard({ bull }) {
  return (
    <div style={{
      border: "1px solid #ccc",
      borderRadius: "8px",
      padding: "1rem",
      width: "200px",
      textAlign: "center"
    }}>
      <img src={bull.image_url || "https://via.placeholder.com/150"} alt={bull.name} width="150" />
      <h3>{bull.name}</h3>
      <p>Breed: {bull.breed}</p>
      <p>Quantity: {bull.semen_quantity}</p>
      <p>Price: ${bull.price}</p>
    </div>
  );
}
