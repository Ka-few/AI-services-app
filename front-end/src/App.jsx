import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import BullsPage from "./pages/BullsPage";
import VetsPage from "./pages/VetsPage";
import Home from "./pages/Home";
import OrdersPage from "./pages/OrdersPage";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/bulls" element={<BullsPage />} />
        <Route path="/vets" element={<VetsPage />} />
        <Route path="/orders" element={<OrdersPage />} />
      </Routes>
    </Router>
  );
}

export default App;
