import { useEffect, useState } from "react";
import "./AdminDashboard.css";
function AdminDashboard() {

  const [totalBookings, setTotalBookings] = useState(0);
  const [mealCounts, setMealCounts] = useState([]);
  const [meals, setMeals] = useState([]);
  const [todayMeals, setTodayMeals] = useState([]);

  const [wasteSummary, setWasteSummary] = useState({
    total_prepared: 0,
    total_consumed: 0,
    total_waste: 0,
    waste_percentage: 0
  });

  const [predictions, setPredictions] = useState([]);

  const [mealName, setMealName] = useState("");
  const [mealType, setMealType] = useState("Breakfast");
  const [mealDate, setMealDate] = useState("");
  const [mealTime, setMealTime] = useState("");

  const [wasteMealId, setWasteMealId] = useState("");
  const [preparedQuantity, setPreparedQuantity] = useState("");
  const [consumedQuantity, setConsumedQuantity] = useState("");


  // =====================================================
  // LOAD DASHBOARD DATA
  // =====================================================

  const loadDashboard = () => {

    fetch("http://127.0.0.1:8000/admin/booking-count")
      .then(response => response.json())
      .then(data => {
        setTotalBookings(data.total_bookings);
      })
      .catch(error => {
        console.error("Booking count error:", error);
      });


    fetch("http://127.0.0.1:8000/admin/meal-counts")
      .then(response => response.json())
      .then(data => {
        setMealCounts(data);
      })
      .catch(error => {
        console.error("Meal count error:", error);
      });


    fetch("http://127.0.0.1:8000/meals")
      .then(response => response.json())
      .then(data => {
        setMeals(data);
      })
      .catch(error => {
        console.error("Meals error:", error);
      });


    // =================================================
    // TODAY'S MEALS
    // =================================================

    fetch("http://127.0.0.1:8000/admin/today-meals")
      .then(response => response.json())
      .then(data => {
        setTodayMeals(data);
      })
      .catch(error => {
        console.error("Today's meals error:", error);
      });


    fetch("http://127.0.0.1:8000/admin/food-waste-summary")
      .then(response => response.json())
      .then(data => {
        setWasteSummary(data);
      })
      .catch(error => {
        console.error("Waste summary error:", error);
      });


    fetch("http://127.0.0.1:8000/admin/meal-prediction")
      .then(response => response.json())
      .then(data => {
        setPredictions(data);
      })
      .catch(error => {
        console.error("Prediction error:", error);
      });

  };


  useEffect(() => {

    loadDashboard();

  }, []);


  // =====================================================
  // ADD MEAL
  // =====================================================

  const addMeal = () => {

    if (!mealName || !mealDate || !mealTime) {

      alert("Please fill all meal details");

      return;

    }


    fetch("http://127.0.0.1:8000/admin/meals", {

      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({

        meal_name: mealName,

        meal_type: mealType,

        meal_date: mealDate,

        meal_time: mealTime

      })

    })

      .then(response => response.json())

      .then(data => {

        if (data.success) {

          alert("Meal added successfully!");

          setMealName("");

          setMealType("Breakfast");

          setMealDate("");

          setMealTime("");

          loadDashboard();

        } else {

          alert("Failed to add meal");

        }

      })

      .catch(error => {

        console.error("Add meal error:", error);

        alert("Unable to connect to server");

      });

  };


  // =====================================================
  // RECORD FOOD WASTE
  // =====================================================

  const recordWaste = () => {

    if (
      !wasteMealId ||
      !preparedQuantity ||
      !consumedQuantity
    ) {

      alert("Please fill all food waste fields");

      return;

    }


    if (Number(preparedQuantity) <= 0) {

      alert(
        "Prepared quantity must be greater than 0"
      );

      return;

    }


    if (Number(consumedQuantity) < 0) {

      alert(
        "Consumed quantity cannot be negative"
      );

      return;

    }


    if (
      Number(consumedQuantity) >
      Number(preparedQuantity)
    ) {

      alert(
        "Consumed quantity cannot be greater than prepared quantity"
      );

      return;

    }


    fetch(
      "http://127.0.0.1:8000/admin/food-waste",
      {

        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({

          meal_id: Number(wasteMealId),

          prepared_quantity:
            Number(preparedQuantity),

          consumed_quantity:
            Number(consumedQuantity)

        })

      }
    )

      .then(response => response.json())

      .then(data => {

        if (data.success) {

          alert(
            "Food waste recorded successfully!\n\nWaste Quantity: "
            + data.waste_quantity
          );

          setWasteMealId("");

          setPreparedQuantity("");

          setConsumedQuantity("");

          loadDashboard();

        } else {

          alert(
            data.message ||
            "Failed to record food waste"
          );

        }

      })

      .catch(error => {

        console.error(
          "Food waste error:",
          error
        );

        alert(
          "Unable to connect to server"
        );

      });

  };


  // =====================================================
  // COMPLETE MEAL
  // =====================================================

  const completeMeal = (mealId, mealName) => {

    const confirmComplete = window.confirm(
      `Are you sure you want to complete "${mealName}"?\n\n` +
      `All active bookings for this meal will be marked as COMPLETED.`
    );

    if (!confirmComplete) {
      return;
    }


    fetch(
      `http://127.0.0.1:8000/admin/meals/${mealId}/complete`,
      {
        method: "PUT"
      }
    )

      .then(response => response.json())

      .then(data => {

        if (data.success) {

          alert(
            "Meal completed successfully!\n\n" +
            "Completed bookings: " +
            data.completed_bookings
          );

          loadDashboard();

        } else {

          alert(
            data.message ||
            "Failed to complete meal"
          );

        }

      })

      .catch(error => {

        console.error(
          "Complete meal error:",
          error
        );

        alert(
          "Unable to connect to server"
        );

      });

  };


  // =====================================================
  // MEAL ICON
  // =====================================================

  const getMealIcon = (type) => {

    if (type === "Breakfast")
      return "🌅";

    if (type === "Lunch")
      return "🍛";

    if (type === "Snacks")
      return "☕";

    if (type === "Dinner")
      return "🌙";

    return "🍽️";

  };


  // =====================================================
  // AI STATUS
  // =====================================================

  const getPredictionStatus = (
    current,
    recommended,
    waste
  ) => {

    if (current >= recommended) {

      return {
        text: "Demand reached",
        className: "high-demand"
      };

    }


    if (waste >= 20) {

      return {
        text: "Waste adjusted",
        className: "prepare"
      };

    }


    if (recommended - current >= 8) {

      return {
        text: "Prepare more",
        className: "prepare"
      };

    }


    return {
      text: "Balanced",
      className: "balanced"
    };

  };


  // =====================================================
  // AI EXPLANATION
  // =====================================================

  const getPredictionExplanation = (
    prediction
  ) => {

    const waste =
      prediction.waste_percentage || 0;

    const historical =
      prediction.historical_average || 0;

    if (waste >= 20) {

      return (
        "High historical waste detected. " +
        "The recommendation has been reduced."
      );

    }


    if (historical > 0) {

      return (
        "Based on historical demand, " +
        "current bookings and ML analysis."
      );

    }


    return (
      "Based on current bookings and AI analysis."
    );

  };


  // =====================================================
  // RENDER
  // =====================================================

  return (

    <div className="admin-page">


      {/* =================================================
          SIDEBAR
      ================================================= */}

      <aside className="admin-sidebar">

        <div className="sidebar-logo">

          <div className="logo-icon">
            🍽️
          </div>

          <div>

            <h2>
              Smart Mess
            </h2>

            <span>
              Admin Panel
            </span>

          </div>

        </div>


        <nav className="sidebar-nav">

          <a
            href="#overview"
            className="active"
          >
            📊
            <span>
              Overview
            </span>
          </a>


          <a href="#today-meals">

            🕐

            <span>
              Today's Meals
            </span>

          </a>


          <a href="#meals">

            🍽️

            <span>
              Meals
            </span>

          </a>


          <a href="#prediction">

            🤖

            <span>
              AI Prediction
            </span>

          </a>


          <a href="#waste">

            ♻️

            <span>
              Food Waste
            </span>

          </a>

        </nav>


        <div className="sidebar-footer">

          <div className="admin-profile">

            <div className="profile-avatar">
              A
            </div>

            <div>

              <strong>
                Administrator
              </strong>

              <span>
                Mess Manager
              </span>

            </div>

          </div>

        </div>

      </aside>


      {/* =================================================
          MAIN CONTENT
      ================================================= */}

      <main className="admin-main">


        {/* =================================================
            HEADER
        ================================================= */}

        <header className="admin-header">

          <div>

            <p className="header-small">
              SMART MESS MANAGEMENT
            </p>

            <h1>
              Dashboard
            </h1>

            <p className="header-description">
              Monitor meal bookings, food consumption
              and AI demand predictions.
            </p>

          </div>


         <div className="header-actions">
  <div className="header-status">
    <span className="status-dot"></span>
    System Online
  </div>

  <button
    className="refresh-button"
    onClick={loadDashboard}
  >
    ↻ Refresh Data
  </button>
</div>




        </header>


        {/* =================================================
            OVERVIEW
        ================================================= */}

        <section id="overview">

          <div className="section-title">

            <div>

              <h2>
                Overview
              </h2>

              <p>
                Today's mess activity at a glance
              </p>

            </div>

          </div>


          <div className="stats-grid">


            {/* ACTIVE BOOKINGS */}

            <div className="stat-card">

              <div className="stat-icon blue">
                📋
              </div>

              <div>

                <span className="stat-label">
                  Active Bookings
                </span>

                <strong className="stat-value">
                  {totalBookings}
                </strong>

                <span className="stat-description">
                  Current meal reservations
                </span>

              </div>

            </div>


            {/* PREPARED */}

            <div className="stat-card">

              <div className="stat-icon purple">
                🍱
              </div>

              <div>

                <span className="stat-label">
                  Meals Prepared
                </span>

                <strong className="stat-value">
                  {wasteSummary.total_prepared}
                </strong>

                <span className="stat-description">
                  Total meals prepared
                </span>

              </div>

            </div>


            {/* CONSUMED */}

            <div className="stat-card">

              <div className="stat-icon green">
                ✅
              </div>

              <div>

                <span className="stat-label">
                  Meals Consumed
                </span>

                <strong className="stat-value">
                  {wasteSummary.total_consumed}
                </strong>

                <span className="stat-description">
                  Successfully consumed
                </span>

              </div>

            </div>


            {/* WASTE */}

            <div className="stat-card">

              <div className="stat-icon orange">
                ♻️
              </div>

              <div>

                <span className="stat-label">
                  Food Waste
                </span>

                <strong className="stat-value">
                  {wasteSummary.waste_percentage}%
                </strong>

                <span className="stat-description">
                  Current waste rate
                </span>

              </div>

            </div>

          </div>

        </section>


        {/* =================================================
            TODAY'S MEAL MANAGEMENT
        ================================================= */}

        <section id="today-meals">

          <div className="section-title">

            <div>

              <div className="section-heading-row">

                <h2>
                  Today's Meal Management
                </h2>

                <span className="today-badge">
                  📅 TODAY
                </span>

              </div>

              <p>
                Monitor today's meals and complete
                meals after serving.
              </p>

            </div>

          </div>


          <div className="today-meals-grid">

            {todayMeals.length === 0 ? (

              <div className="empty-card">

                <span>
                  🍽️
                </span>

                <p>
                  No meals scheduled for today.
                </p>

              </div>

            ) : (

              todayMeals.map(meal => (

                <div
                  className="today-meal-card"
                  key={meal.meal_id}
                >

                  {/* MEAL HEADER */}

                  <div className="today-meal-header">

                    <div>

                      <span className="today-meal-type">

                        {getMealIcon(
                          meal.meal_type
                        )}

                        {meal.meal_type}

                      </span>

                      <h3>
                        {meal.meal_name}
                      </h3>

                    </div>

                    <div className="today-meal-icon">
                      🍽️
                    </div>

                  </div>


                  {/* MEAL TIME */}

                  <div className="today-meal-time">

                    🕐

                    <strong>
                      {meal.meal_time
  ? String(meal.meal_time).slice(0, 5)
  : "Time unavailable"}
                    </strong>

                  </div>


                  {/* BOOKING INFORMATION */}

                  <div className="today-meal-stats">

                    <div>

                      <span>
                        Active Bookings
                      </span>

                      <strong>
                        {meal.active_bookings}
                      </strong>

                    </div>


                    <div>

                      <span>
                        Completed
                      </span>

                      <strong>
                        {meal.completed_bookings}
                      </strong>

                    </div>

                  </div>


                  {/* STATUS */}

                  <div className="today-meal-status">

                    {meal.completed_bookings > 0 &&
                    meal.active_bookings === 0 ? (

                      <span className="meal-completed-status">

                        ✓ Meal Completed

                      </span>

                    ) : (

                      <span className="meal-pending-status">

                        ● Meal Pending

                      </span>

                    )}

                  </div>


                  {/* COMPLETE BUTTON */}

                  {!(
                    meal.completed_bookings > 0 &&
                    meal.active_bookings === 0
                  ) && (

                    <button
                      className="complete-meal-button"
                      onClick={() =>
                        completeMeal(
                          meal.meal_id,
                          meal.meal_name
                        )
                      }
                    >

                      ✓ Complete Meal

                    </button>

                  )}

                </div>

              ))

            )}

          </div>

        </section>


        {/* =================================================
            MEAL BOOKINGS
        ================================================= */}

        <section id="meals">

          <div className="section-title">

            <div>

              <h2>
                Meal Bookings
              </h2>

              <p>
                Active bookings by meal type
              </p>

            </div>

          </div>


          <div className="meal-stats-grid">

            {mealCounts.length === 0 ? (

              <div className="empty-card">

                <span>
                  📊
                </span>

                <p>
                  No booking data available.
                </p>

              </div>

            ) : (

              mealCounts.map(meal => (

                <div
                  className="meal-stat-card"
                  key={meal.meal_type}
                >

                  <div className="meal-stat-top">

                    <div className="meal-type-icon">

                      {getMealIcon(
                        meal.meal_type
                      )}

                    </div>

                    <span className="meal-type">

                      {meal.meal_type}

                    </span>

                  </div>


                  <strong>
                    {meal.booking_count}
                  </strong>


                  <span>
                    active bookings
                  </span>

                </div>

              ))

            )}

          </div>

        </section>


        {/* =================================================
            AI PREDICTION
        ================================================= */}

        <section id="prediction">

          <div className="section-title">

            <div>

              <div className="section-heading-row">

                <h2>
                  AI Meal Demand Prediction
                </h2>

                <span className="ai-badge">
                  ✨ AI POWERED
                </span>

              </div>

              <p>
                AI combines historical demand,
                current bookings, ML prediction
                and food-waste patterns.
              </p>

            </div>

          </div>


          <div className="prediction-grid">


            {predictions.length === 0 ? (

              <div className="empty-card">

                <span>
                  🤖
                </span>

                <p>
                  No predictions available.
                </p>

              </div>

            ) : (

              predictions.map(prediction => {

                const bookings =
                  prediction.current_bookings || 0;


                const recommended =
                  prediction.predicted_quantity || 0;


                const historical =
                  prediction.historical_average || 0;


                const mlPrediction =
                  prediction.ml_prediction || 0;


                const waste =
                  prediction.waste_percentage || 0;


                const additional =
                  Math.max(
                    0,
                    recommended - bookings
                  );


                const status =
                  getPredictionStatus(
                    bookings,
                    recommended,
                    waste
                  );


                return (

                  <div
                    className="prediction-card"
                    key={prediction.meal_id}
                  >


                    {/* CARD HEADER */}

                    <div className="prediction-header">

                      <div>

                        <span className="prediction-type">

                          {getMealIcon(
                            prediction.meal_type
                          )}

                          {prediction.meal_type}

                        </span>


                        <h3>
                          {prediction.meal_name}
                        </h3>


                        <p>
                          📅 {prediction.meal_date}
                        </p>

                      </div>


                      <div className="prediction-ai-icon">
                        🤖
                      </div>

                    </div>


                    {/* RECOMMENDATION HERO */}

                    <div className="ai-recommendation">

                      <span>
                        AI RECOMMENDS
                      </span>

                      <strong>
                        {recommended}
                      </strong>

                      <small>
                        portions to prepare
                      </small>

                    </div>


                    {/* AI DATA */}

                    <div className="prediction-content">


                      <div className="prediction-item">

                        <span>
                          Current Bookings
                        </span>

                        <strong>
                          {bookings}
                        </strong>

                      </div>


                      <div className="prediction-item">

                        <span>
                          Historical Avg.
                        </span>

                        <strong>
                          {historical}
                        </strong>

                      </div>


                      <div className="prediction-item">

                        <span>
                          ML Prediction
                        </span>

                        <strong>
                          {mlPrediction}
                        </strong>

                      </div>


                      <div className="prediction-item">

                        <span>
                          Food Waste
                        </span>

                        <strong>
                          {waste}%
                        </strong>

                      </div>

                    </div>


                    {/* ADDITIONAL MEALS */}

                    <div className="prediction-footer">

                      <span>

                        Additional portions:

                        {" "}

                        <strong>
                          {additional}
                        </strong>

                      </span>


                      <span
                        className={
                          `prediction-status ${
                            status.className
                          }`
                        }
                      >

                        {status.text}

                      </span>

                    </div>


                    {/* EXPLANATION */}

                    <div className="ai-explanation">

                      🤖

                      <span>

                        {getPredictionExplanation(
                          prediction
                        )}

                      </span>

                    </div>


                    {/* COMPLETE MEAL BUTTON */}

                    <button
                      className="complete-meal-button"
                      onClick={() =>
                        completeMeal(
                          prediction.meal_id,
                          prediction.meal_name
                        )
                      }
                    >

                      ✓ Complete Meal

                    </button>

                  </div>

                );

              })

            )}

          </div>

        </section>


        {/* =================================================
            FOOD WASTE
        ================================================= */}

        <section id="waste">

          <div className="section-title">

            <div>

              <h2>
                Food Waste Analytics
              </h2>

              <p>
                Track preparation, consumption
                and food waste.
              </p>

            </div>

          </div>










       <div className="waste-grid">


            <div className="waste-card">

              <span className="waste-label">
                Prepared
              </span>

              <strong>
                {wasteSummary.total_prepared}
              </strong>

              <span>
                meals
              </span>

            </div>


            <div className="waste-card">

              <span className="waste-label">
                Consumed
              </span>

              <strong>
                {wasteSummary.total_consumed}
              </strong>

              <span>
                meals
              </span>

            </div>







            
<div className="waste-breakdown">
  <h3>Food Consumption Breakdown</h3>

  <p>
    {wasteSummary.total_consumed} portions consumed out of{" "}
    {wasteSummary.total_prepared} portions prepared.
  </p>

  <div className="waste-progress">
    <div
      className="consumed-progress"
      style={{
        width:
          wasteSummary.total_prepared > 0
            ? `${(wasteSummary.total_consumed / wasteSummary.total_prepared) * 100}%`
            : "0%"
      }}
    />
  </div>

  <div className="waste-legend">
    <span>
      <span className="legend-dot consumed-dot" />
      Consumed: {wasteSummary.total_consumed}
    </span>

    <span>
      <span className="legend-dot wasted-dot" />
      Wasted: {wasteSummary.total_waste}
    </span>
  </div>
</div>






            <div className="waste-card">

              <span className="waste-label">
                Wasted
              </span>

              <strong>
                {wasteSummary.total_waste}
              </strong>

              <span>
                meals
              </span>

            </div>


            <div className="waste-card highlight">

              <span className="waste-label">
                Waste Rate
              </span>

              <strong>
                {wasteSummary.waste_percentage}%
              </strong>

              <span>
                of prepared food
              </span>

            </div>

          </div>

        </section>


        {/* =================================================
            ACTION AREA
        ================================================= */}

        <section className="action-grid">


          {/* ADD MEAL */}

          <div className="form-card">

            <div className="form-header">

              <div className="form-icon">
                🍽️
              </div>

              <div>

                <h2>
                  Add New Meal
                </h2>

                <p>
                  Create a new meal schedule
                </p>

              </div>

            </div>


            <div className="form-group">

              <label>
                Meal Name
              </label>

              <input
                type="text"
                placeholder="Example: Rice, Sambar & Poriyal"
                value={mealName}
                onChange={e =>
                  setMealName(
                    e.target.value
                  )
                }
              />

            </div>


            <div className="form-row">


              <div className="form-group">

                <label>
                  Meal Type
                </label>

                <select
                  value={mealType}
                  onChange={e =>
                    setMealType(
                      e.target.value
                    )
                  }
                >

                  <option value="Breakfast">
                    Breakfast
                  </option>

                  <option value="Lunch">
                    Lunch
                  </option>

                  <option value="Snacks">
                    Snacks
                  </option>

                  <option value="Dinner">
                    Dinner
                  </option>

                </select>

              </div>


              <div className="form-group">

                <label>
                  Date
                </label>

                <input
                  type="date"
                  value={mealDate}
                  onChange={e =>
                    setMealDate(
                      e.target.value
                    )
                  }
                />

              </div>

            </div>


            <div className="form-group">

              <label>
                Meal Time
              </label>

              <input
                type="time"
                value={mealTime}
                onChange={e =>
                  setMealTime(
                    e.target.value
                  )
                }
              />

            </div>


            <button
              className="primary-button"
              onClick={addMeal}
            >

              + Add Meal

            </button>

          </div>


          {/* RECORD WASTE */}

          <div className="form-card">

            <div className="form-header">

              <div className="form-icon waste-icon">
                ♻️
              </div>

              <div>

                <h2>
                  Record Food Consumption
                </h2>

                <p>
                  Track prepared and consumed quantities
                </p>

              </div>

            </div>


            <div className="form-group">

              <label>
                Select Meal
              </label>

              <select
                value={wasteMealId}
                onChange={e =>
                  setWasteMealId(
                    e.target.value
                  )
                }
              >

                <option value="">
                  Select a meal
                </option>


                {meals.map(meal => (

                  <option
                    key={meal.meal_id}
                    value={meal.meal_id}
                  >

                    {meal.meal_type}
                    {" - "}
                    {meal.meal_name}

                  </option>

                ))}

              </select>

            </div>


            <div className="form-row">


              <div className="form-group">

                <label>
                  Prepared Quantity
                </label>

                <input
                  type="number"
                  min="1"
                  placeholder="Example: 100"
                  value={preparedQuantity}
                  onChange={e =>
                    setPreparedQuantity(
                      e.target.value
                    )
                  }
                />

              </div>


              <div className="form-group">

                <label>
                  Consumed Quantity
                </label>

                <input
                  type="number"
                  min="0"
                  placeholder="Example: 90"
                  value={consumedQuantity}
                  onChange={e =>
                    setConsumedQuantity(
                      e.target.value
                    )
                  }
                />

              </div>

            </div>


            <div className="waste-preview">

              <span>
                Estimated Waste
              </span>

              <strong>

                {preparedQuantity &&
                consumedQuantity

                  ? Math.max(

                      0,

                      Number(
                        preparedQuantity
                      )
                      -
                      Number(
                        consumedQuantity
                      )

                    )

                  : 0}

              </strong>

              <span>
                meals
              </span>

            </div>


            <button
              className="secondary-button"
              onClick={recordWaste}
            >

              ♻ Record Consumption

            </button>

          </div>

        </section>


        {/* =================================================
            FOOTER
        ================================================= */}

        <footer className="admin-footer">

          <span>
            Smart Mess Management System
          </span>

          <span>
            AI-driven food waste reduction
          </span>

        </footer>

      </main>

    </div>

  );

}

export default AdminDashboard;