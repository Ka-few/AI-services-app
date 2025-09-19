import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav style={{ padding: "1rem", background: "#f5f5f5" }}>
      <Link to="/" style={{ marginRight: "1rem" }}>Home</Link>
      <Link to="/bulls" style={{ marginRight: "1rem" }}>Bulls</Link>
      <Link to="/vets">Vets</Link>
    </nav>
  );
}
