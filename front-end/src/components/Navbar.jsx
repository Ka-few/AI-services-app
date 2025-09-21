import React from "react";
import { Link } from "react-router-dom";
import "../index.css"

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="brand">🐂 Bull Catalog</div>
      <div className="navbar-links">
        <Link to="/">Home</Link>
        <Link to="/bulls">Bulls</Link>
        <Link to="/vets">Vets</Link>
        <Link to="/orders">Orders</Link>
      </div>
    </nav>
  );
}
