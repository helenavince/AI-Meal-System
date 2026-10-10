
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";

function Dashboard() {
  const navigate = useNavigate();

  const meals = [
    {
      name: "Breakfast",
      emoji: "🌅",
      menu: "Idli, Sambar, Chutney",
    },
    {
      name: "Lunch",
      emoji: "☀️",
      menu: "Rice, Sambar, Poriyal",
    },
    {
      name: "Snacks",
      emoji: "🍪",
      menu: "Tea and Biscuits",
    },
    {
      name: "Dinner",
      emoji: "🌙",
      menu: "Chapati, Kurma",
    },
  ];

  return (
    <div className="dashboard">
      <h1>Smart Mess</h1>
      <p>AI-Driven Meal Prebooking System</p>

      <div className="meal-container">
        {meals.map((meal) => (
          <div className="meal-card" key={meal.name}>
            <h2>
              {meal.emoji} {meal.name}
            </h2>

            <p>{meal.menu}</p>

            <button onClick={() => navigate("/booking")}>
              Book Meal
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;

