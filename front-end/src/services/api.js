import axios from "axios";

const API_BASE = "http://localhost:5000"; // backend url

export const api = axios.create({
  baseURL: API_BASE,
});

// Bulls
export const getBulls = () => api.get("/bulls");
export const getBull = (id) => api.get(`/bulls/${id}`);
export const createBull = (data) => api.post("/bulls", data);
export const updateBull = (id, data) => api.put(`/bulls/${id}`, data);
export const deleteBull = (id) => api.delete(`/bulls/${id}`);

// Vets
export const getVets = () => api.get("/vets");
export const getVet = (id) => api.get(`/vets/${id}`);
export const createVet = (data) => api.post("/vets", data);
export const updateVet = (id, data) => api.put(`/vets/${id}`, data);
export const deleteVet = (id) => api.delete(`/vets/${id}`);
