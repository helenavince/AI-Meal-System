

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";

function MyBookings() {
  const navigate = useNavigate();
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const student = JSON.parse(localStorage.getItem("student"));

    if (!student) {
      setLoading(false);
      navigate("/login");
      return;
    }

    fetch(`http://127.0.0.1:8000/bookings/${student.student_id}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to load bookings");
        }
        return response.json();
      })
      .then((data) => {
        setBookings(data);
      })
      .catch((error) => {
        console.error("Error fetching bookings:", error);
        alert("Unable to load bookings. Please try again.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [navigate]);

  return (
    <div className="dashboard">
      <div className="booking-header">
        <div>
          <h1>My Bookings</h1>
          <p>View your meal booking history.</p>
        </div>

        <div className="booking-navigation">
          <button onClick={() => navigate("/")}>
            Dashboard
          </button>

          <button onClick={() => navigate("/booking")}>
            Book Meals
          </button>
        </div>
      </div>

      {loading ? (
        <p>Loading your bookings...</p>
      ) : bookings.length === 0 ? (
        <div className="meal-card">
          <h2>No bookings yet</h2>
          <p>You haven't made any meal bookings yet.</p>
          <button onClick={() => navigate("/booking")}>
            Book a Meal
          </button>
        </div>
      ) : (
        <div className="meal-container">
          {bookings.map((booking) => (
            <div className="meal-card" key={booking.booking_id}>
              <h2>🍽️ {booking.meal_type}</h2>

              <p>
                <strong>Meal:</strong> {booking.meal_name}
              </p>

              <p>
                <strong>Date:</strong>{" "}
                {booking.meal_date || "Not available"}
              </p>

              <p>
                <strong>Time:</strong>{" "}
                {booking.meal_time || "Not available"}
              </p>

              <p>
                <strong>Status:</strong>{" "}
                {booking.status || "Unknown"}
              </p>

              <p>
                <strong>Booking ID:</strong> {booking.booking_id}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default MyBookings;

