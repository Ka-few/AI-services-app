import React, { useEffect, useState } from "react";
import { getBulls } from "../services/api";
import BullCard from "./BullCard";
import axios from "axios";
import "../styles/BullList.css"

export default function BullList() {
   const [bulls, setBulls] = useState([]);
  const [loading, setLoading] = useState(true); 
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/bulls") 
      .then((res) => {
        setBulls(res.data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading bulls...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: "1rem" }}>
      {bulls.map((bull) => (
        <div
          key={bull.id}
          style={{
            border: "1px solid #ccc",
            padding: "1rem",
            width: "200px",
            borderRadius: "8px",
          }}
        >
          <h3>{bull.name}</h3>
          <p>Breed: {bull.breed}</p>
          <p>Age: {bull.age}</p>
          <p>Qty: {bull.semen_quantity}</p>
          <p>Price: ${bull.price}</p>
        </div>
      ))}
    </div>
  );
}
