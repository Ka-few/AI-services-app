// BullList.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import "../index.css"

export default function BullList() {
  const [bulls, setBulls] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    id: null,
    name: "",
    breed: "",
    age: "",
    description: "",
    image_url: "",
    semen_quantity: 0,
    price: 0,
  });

  const API_URL = "http://localhost:5000/bulls";

  // Fetch bulls
  const fetchBulls = async () => {
    try {
      const res = await axios.get(API_URL);
      setBulls(res.data);
    } catch (err) {
      setError("Failed to fetch bulls");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBulls();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
    const payload = {
      ...formData,
      age: formData.age ? parseInt(formData.age) : null,
      semen_quantity: parseInt(formData.semen_quantity),
      price: parseFloat(formData.price),
    };

    if (formData.id) {
      await axios.put(`${API_URL}/${formData.id}`, payload);
    } else {
      await axios.post(API_URL, payload);
    }

      setShowForm(false);
      setFormData({
        id: null,
        name: "",
        breed: "",
        age: "",
        description: "",
        image_url: "",
        semen_quantity: 0,
        price: 0,
      });
      fetchBulls();
    } catch (err) {
      console.error(err);
      alert("Error saving bull");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this bull?")) return;
    try {
      await axios.delete(`${API_URL}/${id}`);
      fetchBulls();
    } catch (err) {
      console.error(err);
      alert("Error deleting bull");
    }
  };

  const handleEdit = (bull) => {
    setFormData(bull);
    setShowForm(true);
  };

  if (loading) return <p>Loading bulls...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div style={{ padding: "1rem" }}>
      <h2>Bulls Catalog</h2>
      <button onClick={() => setShowForm(true)}>Add Bull</button>

      {showForm && (
        <form
          onSubmit={handleSubmit}
          style={{
            margin: "1rem 0",
            border: "1px solid #ccc",
            padding: "1rem",
            borderRadius: "8px",
          }}
        >
          <h3>{formData.id ? "Edit Bull" : "Add Bull"}</h3>
          <input
            type="text"
            name="name"
            placeholder="Name"
            value={formData.name}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="breed"
            placeholder="Breed"
            value={formData.breed}
            onChange={handleChange}
            required
          />
          <input
            type="number"
            name="age"
            placeholder="Age"
            value={formData.age}
            onChange={handleChange}
          />
          <input
            type="text"
            name="description"
            placeholder="Description"
            value={formData.description}
            onChange={handleChange}
          />
          <input
            type="text"
            name="image_url"
            placeholder="Image URL"
            value={formData.image_url}
            onChange={handleChange}
          />
          <input
            type="number"
            name="semen_quantity"
            placeholder="Semen Quantity"
            value={formData.semen_quantity}
            onChange={handleChange}
          />
          <input
            type="number"
            name="price"
            placeholder="Price"
            value={formData.price}
            onChange={handleChange}
          />
          <button type="submit">{formData.id ? "Update" : "Add"}</button>
          <button type="button" onClick={() => setShowForm(false)}>
            Cancel
          </button>
        </form>
      )}

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "1rem",
          marginTop: "1rem",
        }}
      >
        {bulls.map((bull) => (
          <div
            key={bull.id}
            style={{
              border: "1px solid #ccc",
              padding: "1rem",
              borderRadius: "8px",
              width: "200px",
            }}
          >
            <h4>{bull.name}</h4>
            <p>
              <strong>Breed:</strong> {bull.breed}
            </p>
            <p>
              <strong>Age:</strong> {bull.age}
            </p>
            <p>
              <strong>Quantity:</strong> {bull.semen_quantity}
            </p>
            <p>
              <strong>Price:</strong> Kshs:{bull.price}
            </p>
            {bull.image_url && (
              <img
                src={bull.image_url}
                alt={bull.name}
                style={{ width: "100%", height: "100px", objectFit: "cover" }}
              />
            )}
            <button onClick={() => handleEdit(bull)}>Edit</button>
            <button onClick={() => handleDelete(bull.id)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
}
