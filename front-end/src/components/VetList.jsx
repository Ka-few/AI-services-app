// VetList.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import "../index.css"

export default function VetList() {
  const [vets, setVets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    id: null,
    name: "",
    phone: "",
    email: "",
    location: "",
  });

  const API_URL = "http://localhost:5000/vets";

  // Fetch vets
  const fetchVets = async () => {
    try {
      const res = await axios.get(API_URL);
      setVets(res.data);
    } catch (err) {
      setError("Failed to fetch vets");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchVets();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (formData.id) {
        // Update vet
        await axios.put(`${API_URL}/${formData.id}`, formData);
      } else {
        // Add new vet
        await axios.post(API_URL, formData);
      }
      setShowForm(false);
      setFormData({
        id: null,
        name: "",
        phone: "",
        email: "",
        location: "",
      });
      fetchVets();
    } catch (err) {
      console.error(err);
      alert("Error saving vet");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this vet?")) return;
    try {
      await axios.delete(`${API_URL}/${id}`);
      fetchVets();
    } catch (err) {
      console.error(err);
      alert("Error deleting vet");
    }
  };

  const handleEdit = (vet) => {
    setFormData(vet);
    setShowForm(true);
  };

  if (loading) return <p>Loading vets...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div style={{ padding: "1rem" }}>
      <h2>Veterinary Officers</h2>
      <button onClick={() => setShowForm(true)}>Add Vet</button>

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
          <h3>{formData.id ? "Edit Vet" : "Add Vet"}</h3>
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
            name="phone"
            placeholder="Phone"
            value={formData.phone}
            onChange={handleChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
          />
          <input
            type="text"
            name="location"
            placeholder="Location"
            value={formData.location}
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
        {vets.map((vet) => (
          <div
            key={vet.id}
            style={{
              border: "1px solid #ccc",
              padding: "1rem",
              borderRadius: "8px",
              width: "220px",
            }}
          >
            <h4>{vet.name}</h4>
            <p>
              <strong>Phone:</strong> {vet.phone}
            </p>
            <p>
              <strong>Email:</strong> {vet.email}
            </p>
            <p>
              <strong>Location:</strong> {vet.location}
            </p>
            <button onClick={() => handleEdit(vet)}>Edit</button>
            <button onClick={() => handleDelete(vet.id)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
}
