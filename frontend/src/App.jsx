import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Booking from "./pages/Booking";
import MyBookings from "./pages/MyBookings";
import Login from "./pages/Login";
import AdminDashboard from "./pages/AdminDashboard";
import "./App.css";

function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route path="/" element={<Dashboard />} />

        <Route path="/login" element={<Login />} />

        <Route path="/booking" element={<Booking />} />

        <Route path="/my-bookings" element={<MyBookings />} />

        <Route path="/admin" element={<AdminDashboard />} />



      </Routes>

    </BrowserRouter>

  );
}

export default App;