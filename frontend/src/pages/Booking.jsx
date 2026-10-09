
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";

function Booking() {
  const navigate = useNavigate();

  const [meals, setMeals] = useState([]);
  const [bookedMeals, setBookedMeals] = useState({});
  const [loading, setLoading] = useState(true);

  // LOAD MEALS
  useEffect(() => {
    fetch("http://127.0.0.1:8000/meals")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to load meals");
        }
        return response.json();
      })
      .then((data) => {
        setMeals(data);
      })
      .catch((error) => {
        console.error("Error fetching meals:", error);
        alert("Unable to load meals. Please check your backend.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  // LOAD EXISTING BOOKINGS
  useEffect(() => {
    const student = JSON.parse(localStorage.getItem("student"));

    if (!student) {
      setBookedMeals({});
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
        const existingBookings = {};

        data.forEach((booking) => {
          if (booking.status !== "BOOKED") {
            return;
          }

          const matchingMeal = meals.find(
            (meal) =>
              meal.meal_name === booking.meal_name &&
              meal.meal_type === booking.meal_type &&
              meal.meal_date === booking.meal_date &&
              meal.meal_time === booking.meal_time
          );

          if (matchingMeal) {
            existingBookings[matchingMeal.meal_id] =
              booking.booking_id;
          }
        });

        setBookedMeals(existingBookings);
      })
      .catch((error) => {
        console.error("Error fetching existing bookings:", error);
      });
  }, [meals]);

  // BOOK OR CANCEL A MEAL
  const handleBooking = (mealId) => {
    const student = JSON.parse(localStorage.getItem("student"));

    if (!student) {
      alert("Please login first");
      navigate("/login");
      return;
    }

    // CANCEL BOOKING
    if (bookedMeals[mealId]) {
      const bookingId = bookedMeals[mealId];

      fetch(
        `http://127.0.0.1:8000/bookings/${bookingId}/cancel`,
        {
          method: "PUT",
        }
      )
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            setBookedMeals((previous) => {
              const updated = { ...previous };
              delete updated[mealId];
              return updated;
            });

            alert("Booking cancelled successfully!");
          } else {
            alert(data.message || "Booking not found");
          }
        })
        .catch((error) => {
          console.error("Cancel error:", error);
          alert("Failed to cancel booking");
        });

      return;
    }

    // CREATE NEW BOOKING
    fetch("http://127.0.0.1:8000/bookings", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        student_id: student.student_id,
        meal_id: mealId,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          setBookedMeals((previous) => ({
            ...previous,
            [mealId]: data.booking_id,
          }));

          alert("Meal booked successfully!");
        } else {
          alert(data.message || "Unable to book this meal");
        }
      })
      .catch((error) => {
        console.error("Booking error:", error);
        alert("Failed to book meal");
      });
  };

  // PAGE UI
  return (
    <div className="dashboard">
      <div className="booking-header">
        <div>
          <h1>Meal Booking</h1>
          <p>Select the meals you want to book.</p>
        </div>

        <div className="booking-navigation">
          <button onClick={() => navigate("/")}>
            Back to Dashboard
          </button>

          <button onClick={() => navigate("/my-bookings")}>
            My Bookings
          </button>
        </div>
      </div>

      {loading ? (
        <p>Loading meals...</p>
      ) : meals.length === 0 ? (
        <p>No meals are currently available.</p>
      ) : (
        <div className="meal-container">
          {meals.map((meal) => (
            <div className="meal-card" key={meal.meal_id}>
              <h2>
                {meal.meal_type === "Breakfast"
                  ? "🌅"
                  : meal.meal_type === "Lunch"
                  ? "☀️"
                  : meal.meal_type === "Snacks"
                  ? "🍪"
                  : meal.meal_type === "Dinner"
                  ? "🌙"
                  : "🍽️"}{" "}
                {meal.meal_type}
              </h2>

              <p>{meal.meal_name}</p>

              <p>Time: {meal.meal_time}</p>

              {meal.meal_date && (
                <p>Date: {meal.meal_date}</p>
              )}

              <button onClick={() => handleBooking(meal.meal_id)}>
                {bookedMeals[meal.meal_id]
                  ? "Cancel Booking"
                  : "Book Meal"}
              </button>
            </div>
          ))}
        </div>
      )}

      <h2>
        Total Meals Booked: {Object.keys(bookedMeals).length}
      </h2>
    </div>
  );
}

export default Booking;

