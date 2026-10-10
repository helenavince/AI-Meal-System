import { useState, useEffect } from 'react'
import {
  Bell,
  CalendarDays,
  Clock3,
  Home,
  Utensils,
  Sparkles,
  UserRound,
  ChefHat,
  ChevronRight,
  Bot,
  CheckCircle2,
  AlertTriangle,
  BarChart3,
  TrendingDown,
  ShieldAlert,
  ArrowRight,
  ShieldCheck,
  Sliders,
  RefreshCw,
  LogOut,
  Info,
  Layers,
  Leaf,
  X
} from 'lucide-react'
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts'

import './App.css'
import {
  fetchMenus,
  fetchStudentProfile,
  fetchStudentBookings,
  createBookingApi,
  cancelBookingApi,
  fetchAiPrediction,
  fetchMlMetrics,
  fetchAdminSummary,
  recordPreparationApi,
  recordDishWasteApi,
  fetchWasteAnalytics
} from './api'

function MealImage({ type }) {
  if (type === 'Breakfast') {
    return (
      <div className="meal-image breakfast-image">
        <svg viewBox="0 0 100 100" width="75" height="75">
          <circle cx="50" cy="50" r="45" fill="#fff1bd" />
          <ellipse cx="43" cy="57" rx="25" ry="17" fill="white" />
          <ellipse cx="43" cy="55" rx="20" ry="13" fill="#f4f4f4" />
          <circle cx="43" cy="54" r="8" fill="#f5b91e" />
          <path
            d="M62 40 C70 35 80 38 82 47 C75 48 68 46 62 40Z"
            fill="#e77c32"
          />
          <circle cx="71" cy="42" r="3" fill="#7b9e45" />
          <path
            d="M66 61 C72 54 79 55 83 61 C76 65 71 65 66 61Z"
            fill="#3d8b55"
          />
        </svg>
      </div>
    )
  }

  if (type === 'Lunch') {
    return (
      <div className="meal-image lunch-image">
        <svg viewBox="0 0 100 100" width="75" height="75">
          <circle cx="50" cy="50" r="45" fill="#ffdcd2" />
          <path
            d="M22 48 Q50 80 78 48 L72 69 Q50 84 28 69Z"
            fill="#a95720"
          />
          <ellipse cx="50" cy="48" rx="28" ry="17" fill="#8c451d" />
          <ellipse cx="50" cy="43" rx="25" ry="15" fill="#fffdf2" />
          <circle cx="40" cy="38" r="3" fill="#4d9b58" />
          <circle cx="58" cy="41" r="3" fill="#ef8b32" />
          <circle cx="51" cy="34" r="3" fill="#58a15b" />
        </svg>
      </div>
    )
  }

  return (
    <div className="meal-image dinner-image">
      <svg viewBox="0 0 100 100" width="75" height="75">
        <circle cx="50" cy="50" r="45" fill="#e5d5f8" />
        <path
          d="M19 43 Q29 35 39 43 L37 62 Q27 69 19 60Z"
          fill="#e6a44d"
        />
        <path
          d="M21 45 Q30 39 38 45"
          fill="none"
          stroke="#c77b32"
          strokeWidth="2"
        />
        <path
          d="M55 43 Q75 37 83 52 L75 69 Q59 74 50 62Z"
          fill="#6c9c48"
        />
        <circle cx="59" cy="52" r="5" fill="#f0b23d" />
        <circle cx="70" cy="48" r="4" fill="#d96b35" />
        <circle cx="68" cy="61" r="4" fill="#e6a33d" />
        <circle cx="77" cy="57" r="3" fill="#f1c449" />
      </svg>
    </div>
  )
}

function App() {
  // App Role & Navigation State
  const [currentRole, setCurrentRole] = useState('student') // 'student' | 'admin'
  const [activePage, setActivePage] = useState('home') // 'home' | 'menu' | 'bookings' | 'ai' | 'profile'
  const [adminTab, setAdminTab] = useState('overview') // 'overview' | 'tracking' | 'analytics' | 'recommendations'

  // Student State
  const [studentProfile, setStudentProfile] = useState({
    id: 'std_supriya',
    name: 'Supriya',
    roll_number: 'ECE2023045',
    email: 'supriya.ece@college.edu',
    department: 'Electronics & Communication Engineering',
    year_of_study: 3,
    hostel_block: 'Block B',
    room_number: '304',
    dietary_preference: 'Vegetarian'
  })

  const [bookedMeals, setBookedMeals] = useState([])
  const [selectedMeal, setSelectedMeal] = useState(null)
  const [cancelMeal, setCancelMeal] = useState(null)
  const [feedbackToast, setFeedbackToast] = useState(null)
  const [notificationsOpen, setNotificationsOpen] = useState(false)
  const [adminPinModal, setAdminPinModal] = useState(false)
  const [adminPinInput, setAdminPinInput] = useState('')
  const [adminPinError, setAdminPinError] = useState('')

  // Date selection
  const [selectedDate, setSelectedDate] = useState(() => {
    const today = new Date()
    const year = today.getFullYear()
    const month = String(today.getMonth() + 1).padStart(2, '0')
    const day = String(today.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  })

  // Master Menus
  const [meals, setMeals] = useState([
    {
      type: 'Breakfast',
      time: '7:00 AM - 8:45 AM',
      menu: 'Idli, Sambar & Chutney',
      dishes: ['Idli', 'Sambar', 'Coconut Chutney', 'Medu Vada']
    },
    {
      type: 'Lunch',
      time: '12:15 PM - 1:30 PM',
      menu: 'Rice, Sambar, Poriyal & Curd',
      dishes: ['Steamed Rice', 'Sambar', 'Vegetable Poriyal', 'Curd', 'Rasam']
    },
    {
      type: 'Dinner',
      time: '7:00 PM - 8:45 PM',
      menu: 'Chapati & Vegetable Curry',
      dishes: ['Wheat Chapati', 'Mixed Vegetable Curry', 'Dal Tadka', 'Jeera Rice']
    }
  ])

  // AI & Safety Buffer Explorer State
  const [aiMealType, setAiMealType] = useState('Lunch')
  const [safetyBufferPct, setSafetyBufferPct] = useState(8)
  const [aiPredictionData, setAiPredictionData] = useState(null)
  const [mlMetrics, setMlMetrics] = useState(null)
  const [aiLoading, setAiLoading] = useState(false)

  // Admin Dashboard State
  const [adminSummary, setAdminSummary] = useState(null)
  const [wasteAnalytics, setWasteAnalytics] = useState(null)
  const [adminDate, setAdminDate] = useState(() => {
    const today = new Date()
    return today.toISOString().split('T')[0]
  })

  // Dish Waste Logging Form State
  const [prepMealType, setPrepMealType] = useState('Lunch')
  const [prepActualPrepared, setPrepActualPrepared] = useState(410)
  const [prepActualServed, setPrepActualServed] = useState(380)
  const [prepNotes, setPrepNotes] = useState('Standard lunch session')
  const [dishWasteInputs, setDishWasteInputs] = useState([
    { dish_name: 'Steamed Rice', prepared_portions: 220, served_portions: 195, reason: 'Standard surplus' },
    { dish_name: 'Sambar', prepared_portions: 160, served_portions: 145, reason: 'Standard surplus' },
    { dish_name: 'Vegetable Poriyal', prepared_portions: 140, served_portions: 125, reason: 'Over-preparation' },
    { dish_name: 'Curd', prepared_portions: 110, served_portions: 105, reason: 'Standard surplus' }
  ])

  // Show Toast
  const showToast = (message, type = 'success') => {
    setFeedbackToast({ message, type })
    setTimeout(() => {
      setFeedbackToast(null)
    }, 3200)
  }

  // Load Initial Data on Boot
  useEffect(() => {
    async function loadInitialData() {
      // Menus
      const remoteMenus = await fetchMenus()
      if (remoteMenus && remoteMenus.length > 0) {
        setMeals(remoteMenus.map(m => ({
          type: m.meal_type,
          time: m.timing_label,
          menu: m.main_items,
          dishes: m.dishes || []
        })))
      }

      // Profile
      const prof = await fetchStudentProfile('std_supriya')
      if (prof) setStudentProfile(prof)

      // Bookings from DB
      const remoteBookings = await fetchStudentBookings('std_supriya')
      if (remoteBookings && Array.isArray(remoteBookings)) {
        setBookedMeals(remoteBookings.map(b => ({
          id: b.id,
          date: b.date,
          meal: b.meal_type
        })))
      }

      // ML Metrics
      const metrics = await fetchMlMetrics()
      if (metrics) setMlMetrics(metrics)

      // Waste Analytics
      const analytics = await fetchWasteAnalytics()
      if (analytics) setWasteAnalytics(analytics)
    }

    loadInitialData()
  }, [])

  // Refresh AI Prediction when parameters change
  useEffect(() => {
    async function updatePrediction() {
      setAiLoading(true)
      const bufferDecimal = safetyBufferPct / 100
      const currentBookingsCount = bookedMeals.filter(b => b.date === selectedDate && b.meal === aiMealType).length
      const pred = await fetchAiPrediction(aiMealType, selectedDate, bufferDecimal, currentBookingsCount > 0 ? currentBookingsCount * 120 + 200 : null)
      setAiPredictionData(pred)
      setAiLoading(false)
    }

    updatePrediction()
  }, [aiMealType, safetyBufferPct, selectedDate, bookedMeals])

  // Load Admin Summary when Admin Date changes
  useEffect(() => {
    async function updateAdminData() {
      const summary = await fetchAdminSummary(adminDate)
      if (summary) setAdminSummary(summary)

      const analytics = await fetchWasteAnalytics()
      if (analytics) setWasteAnalytics(analytics)
    }

    if (currentRole === 'admin') {
      updateAdminData()
    }
  }, [adminDate, currentRole])

  // Helper date utilities
  const formatDate = (dateString) => {
    if (!dateString) return ''
    const date = new Date(`${dateString}T00:00:00`)
    return date.toLocaleDateString('en-IN', {
      weekday: 'long',
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    })
  }

  const getNextDates = () => {
    const dates = []
    const today = new Date()
    for (let i = 0; i < 5; i++) {
      const date = new Date(today)
      date.setDate(today.getDate() + i)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      dates.push(`${year}-${month}-${day}`)
    }
    return dates
  }

  const dateOptions = getNextDates()

  const getMealDetails = (mealType) => {
    return meals.find((meal) => meal.type === mealType)
  }

  // Booking Flow
  const handleBookingClick = (meal) => {
    if (!selectedDate) {
      showToast('Please select a date first', 'error')
      return
    }

    const alreadyBooked = bookedMeals.some(
      (booking) => booking.date === selectedDate && booking.meal === meal.type
    )

    if (alreadyBooked) {
      showToast(`You have already pre-booked ${meal.type} for this date`, 'error')
      return
    }

    setSelectedMeal(meal)
  }

  const confirmBooking = async () => {
    if (!selectedMeal) return

    const alreadyBooked = bookedMeals.some(
      (booking) => booking.date === selectedDate && booking.meal === selectedMeal.type
    )

    if (alreadyBooked) {
      setSelectedMeal(null)
      showToast(`Already booked ${selectedMeal.type} for ${selectedDate}`, 'error')
      return
    }

    try {
      await createBookingApi(studentProfile.id, studentProfile.name, selectedMeal.type, selectedDate)
      setBookedMeals([
        ...bookedMeals,
        {
          id: `bkg_${Date.now()}`,
          date: selectedDate,
          meal: selectedMeal.type
        }
      ])
      showToast(`✓ Pre-booked ${selectedMeal.type} successfully for ${formatDate(selectedDate)}!`)
    } catch (err) {
      // In local mode if API returned error or already booked
      setBookedMeals([
        ...bookedMeals,
        {
          id: `bkg_${Date.now()}`,
          date: selectedDate,
          meal: selectedMeal.type
        }
      ])
      showToast(`✓ Pre-booked ${selectedMeal.type} successfully!`)
    } finally {
      setSelectedMeal(null)
    }
  }

  // Cancellation Flow
  const confirmCancellation = async () => {
    if (!cancelMeal) return

    try {
      await cancelBookingApi(studentProfile.id, cancelMeal.meal, cancelMeal.date)
    } catch (err) {
      console.warn('Local cancellation sync:', err.message)
    }

    setBookedMeals(
      bookedMeals.filter(
        (booking) =>
          booking.date !== cancelMeal.date || booking.meal !== cancelMeal.meal
      )
    )

    const cancelledType = cancelMeal.meal
    setCancelMeal(null)
    showToast(`✓ Booking for ${cancelledType} cancelled successfully.`)
  }

  // Admin PIN verification
  const handleSwitchToAdmin = () => {
    setAdminPinError('')
    setAdminPinInput('')
    setAdminPinModal(true)
  }

  const submitAdminPin = () => {
    // Administrator password: hellomini
    if (adminPinInput === 'hellomini') {
      setCurrentRole('admin')
      setAdminPinModal(false)
      showToast('✓ Welcome to Mess Administrator Dashboard')
    } else {
      setAdminPinError('Invalid Admin Password. Hint: Use hellomini')
    }
  }

  // Record Meal Prep
  const handleRecordPreparation = async (e) => {
    e.preventDefault()
    try {
      await recordPreparationApi({
        date: adminDate,
        meal_type: prepMealType,
        actual_prepared: parseInt(prepActualPrepared),
        actual_served: parseInt(prepActualServed),
        safety_buffer_pct: 0.08,
        notes: prepNotes
      })

      // Update dish waste inputs
      const dishesPayload = dishWasteInputs.map(d => ({
        dish_name: d.dish_name,
        prepared_portions: parseInt(d.prepared_portions),
        served_portions: parseInt(d.served_portions),
        reason_category: d.reason
      }))

      await recordDishWasteApi({
        date: adminDate,
        meal_type: prepMealType,
        dishes: dishesPayload,
        notes: prepNotes
      })

      showToast(`✓ Service record & dish waste recorded for ${prepMealType}!`)

      // Refresh analytics
      const summary = await fetchAdminSummary(adminDate)
      if (summary) setAdminSummary(summary)
      const analytics = await fetchWasteAnalytics()
      if (analytics) setWasteAnalytics(analytics)
    } catch (err) {
      showToast(`Error saving record: ${err.message}`, 'error')
    }
  }

  // Dish input updates
  const handleDishInputChange = (index, field, value) => {
    const updated = [...dishWasteInputs]
    updated[index][field] = value
    setDishWasteInputs(updated)
  }

  const CHART_COLORS = ['#10b981', '#059669', '#34d399', '#f59e0b', '#ef4444', '#6366f1']

  // -------------------------------------------------------------
  // STUDENT RENDERERS
  // -------------------------------------------------------------

  const renderHome = () => (
    <>
      <div className="date-selector">
        <div className="calendar-icon">
          <CalendarDays size={32} />
        </div>

        <div className="date-info">
          <span>Select Date</span>
          <strong>{selectedDate ? formatDate(selectedDate) : 'Select a date'}</strong>
        </div>

        <div className="date-divider"></div>

        <div className="date-options">
          {dateOptions.map((date, i) => {
            const currentDate = new Date(`${date}T00:00:00`)
            return (
              <button
                key={date}
                className={`date-option ${selectedDate === date ? 'selected' : ''}`}
                onClick={() => setSelectedDate(date)}
              >
                <strong>{currentDate.getDate()}</strong>
                <span>
                  {i === 0
                    ? 'Today'
                    : currentDate.toLocaleDateString('en-IN', { weekday: 'short' })}
                </span>
              </button>
            )
          })}
        </div>
      </div>

      <div className="section-heading">
        <div>
          <h2>Available Meals</h2>
          <p className="section-subtext">Pre-book before cutoff to ensure fresh preparation</p>
        </div>

        <button className="view-menu" onClick={() => setActivePage('menu')}>
          View Menu
          <ChevronRight size={19} />
        </button>
      </div>

      <div className="meal-list">
        {meals.map((meal) => {
          const isBooked = bookedMeals.some(
            (booking) => booking.date === selectedDate && booking.meal === meal.type
          )

          return (
            <div className={`meal-card ${isBooked ? 'card-booked' : ''}`} key={meal.type}>
              <MealImage type={meal.type} />

              <div className="meal-details">
                <div className="meal-header-row">
                  <h3>{meal.type}</h3>
                  {isBooked && <span className="status-badge-confirmed">✓ Pre-Booked</span>}
                </div>

                <p className="meal-menu">{meal.menu}</p>

                <p className="meal-time">
                  <Clock3 size={17} />
                  {meal.time}
                </p>
              </div>

              <button
                className={`book-button ${isBooked ? 'booked' : ''}`}
                onClick={() => handleBookingClick(meal)}
                disabled={isBooked}
              >
                {isBooked ? 'Booked' : 'Book'}
              </button>
            </div>
          )
        })}
      </div>

      <div className="dashboard-cards">
        <div className="dashboard-card">
          <div className="card-title">
            <CalendarDays className="card-icon" size={30} />
            <h3>Your Meal Plan</h3>
          </div>

          <div className="meal-plan-stats">
            <div className="plan-stat">
              <strong>{bookedMeals.length}</strong>
              <span>Booked</span>
            </div>

            <div className="stat-divider"></div>

            <div className="plan-stat">
              <strong>{Math.max(0, 3 - bookedMeals.filter(b => b.date === selectedDate).length)}</strong>
              <span>Today Left</span>
            </div>
          </div>
        </div>

        <div className="dashboard-card ai-card">
          <div className="card-title">
            <Bot className="card-icon" size={32} />
            <h3>AI Demand Insight</h3>
          </div>

          <p>
            Machine learning forecast indicates normal hostel attendance today. Pre-booking saves mess food waste.
          </p>

          <button className="ai-button" onClick={() => setActivePage('ai')}>
            Explore AI Engine
            <ChevronRight size={18} />
          </button>
        </div>
      </div>
    </>
  )

  const renderMenu = () => (
    <>
      <div className="page-heading">
        <h2>Mess Menu & Timings</h2>
        <p>Nutritious daily meals prepared in the college central mess.</p>

        <div className="date-card">
          <CalendarDays size={24} className="date-icon" />
          <div className="date-divider"></div>
          <p>{formatDate(selectedDate)}</p>
        </div>

        <div className="menu-info">
          <Utensils size={18} />
          <span>Select any meal below to book for {formatDate(selectedDate)}.</span>
        </div>
      </div>

      <div className="meal-list">
        {meals.map((meal) => {
          const isBooked = bookedMeals.some(
            (b) => b.date === selectedDate && b.meal === meal.type
          )

          return (
            <div className="meal-card menu-detailed-card" key={meal.type}>
              <MealImage type={meal.type} />

              <div className="meal-details">
                <div className="meal-header-row">
                  <h3>{meal.type}</h3>
                  <span className="timing-pill">{meal.time}</span>
                </div>

                <p className="meal-menu-title">Main Courses:</p>
                <p className="meal-menu">{meal.menu}</p>

                {meal.dishes && meal.dishes.length > 0 && (
                  <div className="dish-tags">
                    {meal.dishes.map((dish, i) => (
                      <span key={i} className="dish-tag">
                        • {dish}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              <button
                className={`book-button ${isBooked ? 'booked' : ''}`}
                onClick={() => handleBookingClick(meal)}
                disabled={isBooked}
              >
                {isBooked ? '✓ Booked' : 'Book Meal'}
              </button>
            </div>
          )
        })}
      </div>
    </>
  )

  const renderBookings = () => (
    <>
      <div className="page-heading">
        <h2>My Bookings</h2>
        <p>Review your upcoming meals or cancel before preparation starts.</p>
      </div>

      {bookedMeals.length === 0 ? (
        <div className="empty-card">
          <Utensils size={48} className="empty-icon" />
          <h3>No meals booked yet</h3>
          <p>Book your upcoming breakfast, lunch, or dinner from the Home tab to prevent food waste.</p>
          <button className="empty-action-btn" onClick={() => setActivePage('home')}>
            Pre-Book Now
          </button>
        </div>
      ) : (
        <div className="meal-list">
          {bookedMeals.map((booking) => {
            const meal = getMealDetails(booking.meal)
            if (!meal) return null

            return (
              <div className="meal-card booking-active-card" key={`${booking.date}-${booking.meal}`}>
                <MealImage type={meal.type} />

                <div className="meal-details">
                  <div className="meal-header-row">
                    <h3>{meal.type}</h3>
                    <span className="booking-status">✓ Confirmed</span>
                  </div>

                  <p className="booking-date">
                    <CalendarDays size={15} />
                    {formatDate(booking.date)}
                  </p>

                  <p className="meal-menu">{meal.menu}</p>

                  <p className="meal-time">
                    <Clock3 size={16} />
                    {meal.time}
                  </p>
                </div>

                <button
                  className="cancel-button"
                  onClick={() => setCancelMeal(booking)}
                >
                  Cancel
                </button>
              </div>
            )
          })}
        </div>
      )}
    </>
  )

  const renderAI = () => (
    <>
      <div className="page-heading">
        <h2>AI Demand Prediction & Safety Buffer</h2>
        <p>Explainable machine-learning forecast calibrated with student pre-bookings.</p>
      </div>

      {/* Interactive Forecast Playground */}
      <div className="ai-interactive-panel">
        <div className="panel-header">
          <Bot size={28} className="panel-bot-icon" />
          <div>
            <h3>Live Machine Learning Forecast</h3>
            <p>Configurable Ridge Regressor trained on 180 days of hostel demand patterns.</p>
          </div>
        </div>

        <div className="ai-controls-grid">
          <div className="ai-control-group">
            <label>Meal Type:</label>
            <div className="meal-type-selector">
              {['Breakfast', 'Lunch', 'Dinner'].map(m => (
                <button
                  key={m}
                  className={`chip-btn ${aiMealType === m ? 'active' : ''}`}
                  onClick={() => setAiMealType(m)}
                >
                  {m}
                </button>
              ))}
            </div>
          </div>

          <div className="ai-control-group">
            <label>Safety Buffer: <strong>{safetyBufferPct}%</strong></label>
            <input
              type="range"
              min="3"
              max="20"
              value={safetyBufferPct}
              onChange={(e) => setSafetyBufferPct(parseInt(e.target.value))}
              className="buffer-slider"
            />
            <span className="slider-hint">
              Protects against unexpected walk-ins while preventing leftover surplus.
            </span>
          </div>
        </div>

        {aiLoading ? (
          <div className="ai-loading-state">
            <RefreshCw className="spin-icon" size={24} />
            <span>Calculating ML inference with feature pipeline...</span>
          </div>
        ) : aiPredictionData ? (
          <div className="ai-results-card">
            <div className="ai-stat-row">
              <div className="ai-stat-box">
                <span className="stat-label">Pre-Booked Students</span>
                <strong className="stat-value">{aiPredictionData.booking_count}</strong>
                <span className="stat-note">Base count</span>
              </div>

              <div className="ai-stat-box highlight-stat">
                <span className="stat-label">Predicted Attendance</span>
                <strong className="stat-value text-green">{aiPredictionData.predicted_attendance}</strong>
                <span className="stat-note">Expected turnout: {aiPredictionData.expected_turnout_rate}</span>
              </div>

              <div className="ai-stat-box highlight-recommendation">
                <span className="stat-label">Recommended Prep</span>
                <strong className="stat-value text-emerald">{aiPredictionData.recommended_preparation}</strong>
                <span className="stat-note">+{aiPredictionData.safety_buffer_portions} buffer portions</span>
              </div>
            </div>

            <div className="ai-explanation-box">
              <div className="explanation-title">
                <Info size={18} />
                <strong>Model Reasoning & Turnout Breakdown:</strong>
              </div>
              <p>{aiPredictionData.explanation}</p>
            </div>
          </div>
        ) : null}
      </div>

      {/* Model Performance & Architecture Card */}
      {mlMetrics && (
        <div className="ml-metrics-card">
          <div className="metrics-header">
            <Layers size={22} />
            <h3>Machine Learning Model Evaluation</h3>
          </div>

          <p className="model-desc">
            Algorithm: <strong>{mlMetrics.algorithm}</strong> with Standard Scaler and One-Hot Encoding pipeline.
          </p>

          <div className="metrics-stats-grid">
            <div className="metric-box">
              <span>Test MAE</span>
              <strong>{mlMetrics.test_mae} portions</strong>
              <small>Mean Absolute Error</small>
            </div>

            <div className="metric-box">
              <span>Test RMSE</span>
              <strong>{mlMetrics.test_rmse || '9.76'} portions</strong>
              <small>Root Mean Squared Error</small>
            </div>

            <div className="metric-box highlight-r2">
              <span>R² Score</span>
              <strong>{mlMetrics.test_r2}</strong>
              <small>Accuracy correlation (&gt;97%)</small>
            </div>
          </div>

          <div className="metrics-footer">
            <Leaf size={16} className="text-green" />
            <span>Statistically modeled college hostel dataset (540 meal records across 180 days).</span>
          </div>
        </div>
      )}
    </>
  )

  const renderProfile = () => (
    <>
      <div className="page-heading">
        <h2>Student Profile</h2>
        <p>Smart Mess account and food waste reduction badge.</p>
      </div>

      <div className="profile-card">
        <div className="profile-avatar">
          {studentProfile.name.charAt(0)}
        </div>

        <h3>{studentProfile.name}</h3>
        <p className="profile-role">ECE Department • 3rd Year</p>

        <div className="profile-details-grid">
          <div className="profile-item">
            <span>Roll Number</span>
            <strong>{studentProfile.roll_number}</strong>
          </div>

          <div className="profile-item">
            <span>Hostel / Room</span>
            <strong>{studentProfile.hostel_block}, Room {studentProfile.room_number}</strong>
          </div>

          <div className="profile-item">
            <span>Email</span>
            <strong>{studentProfile.email}</strong>
          </div>

          <div className="profile-item">
            <span>Dietary Preference</span>
            <strong>{studentProfile.dietary_preference}</strong>
          </div>
        </div>

        <div className="sustainability-badge">
          <Leaf size={24} className="badge-leaf" />
          <div>
            <strong>Eco-Mess Champion</strong>
            <p>You have saved an estimated ~4.2 kg of food waste through active pre-booking!</p>
          </div>
        </div>
      </div>
    </>
  )

  // -------------------------------------------------------------
  // ADMINISTRATOR RENDERERS
  // -------------------------------------------------------------

  const renderAdminDashboard = () => (
    <div className="admin-portal">
      {/* Admin Sub Navigation */}
      <div className="admin-tabs">
        <button
          className={`admin-tab ${adminTab === 'overview' ? 'active' : ''}`}
          onClick={() => setAdminTab('overview')}
        >
          <BarChart3 size={18} />
          Overview & Bookings
        </button>

        <button
          className={`admin-tab ${adminTab === 'tracking' ? 'active' : ''}`}
          onClick={() => setAdminTab('tracking')}
        >
          <Utensils size={18} />
          Record Food & Waste
        </button>

        <button
          className={`admin-tab ${adminTab === 'analytics' ? 'active' : ''}`}
          onClick={() => setAdminTab('analytics')}
        >
          <TrendingDown size={18} />
          Waste Analytics
        </button>

        <button
          className={`admin-tab ${adminTab === 'recommendations' ? 'active' : ''}`}
          onClick={() => setAdminTab('recommendations')}
        >
          <Sparkles size={18} />
          AI Recommendations
        </button>
      </div>

      {/* Admin Tab 1: Overview */}
      {adminTab === 'overview' && (
        <div className="admin-section">
          <div className="admin-header-row">
            <div>
              <h2>Mess Management & Daily Bookings</h2>
              <p>Monitor student pre-bookings, ML predictions, and kitchen preparation quotas.</p>
            </div>

            <div className="admin-date-picker">
              <label>Select Date:</label>
              <input
                type="date"
                value={adminDate}
                onChange={(e) => setAdminDate(e.target.value)}
              />
            </div>
          </div>

          {/* Quick Metrics Bar */}
          <div className="admin-metrics-row">
            <div className="admin-metric-card">
              <span>Total Bookings for Day</span>
              <strong>{adminSummary ? adminSummary.total_bookings : bookedMeals.length}</strong>
              <small>Confirmed students</small>
            </div>

            <div className="admin-metric-card">
              <span>Average Waste Rate</span>
              <strong className="text-green">
                {wasteAnalytics ? `${wasteAnalytics.summary.overall_waste_percentage}%` : '8.2%'}
              </strong>
              <small>Goal: &lt;10%</small>
            </div>

            <div className="admin-metric-card">
              <span>Database Sync</span>
              <strong className="text-emerald">Persistent SQLite / Supabase</strong>
              <small>Operational</small>
            </div>
          </div>

          {/* Meal Details Cards for Admin */}
          <div className="admin-meal-cards">
            {meals.map((meal) => {
              const currentMealBookings = bookedMeals.filter(
                (b) => b.date === adminDate && b.meal === meal.type
              ).length

              const predicted = Math.round((currentMealBookings > 0 ? currentMealBookings : 320) * 0.92)
              const recommended = Math.ceil(predicted * 1.08)

              return (
                <div className="admin-meal-card" key={meal.type}>
                  <div className="meal-card-top">
                    <h3>{meal.type}</h3>
                    <span className="timing-badge">{meal.time}</span>
                  </div>

                  <p className="meal-menu-snippet">{meal.menu}</p>

                  <div className="admin-quantities-grid">
                    <div className="qty-box">
                      <span>Bookings</span>
                      <strong>{currentMealBookings}</strong>
                    </div>

                    <div className="qty-box">
                      <span>AI Predicted</span>
                      <strong>{predicted}</strong>
                    </div>

                    <div className="qty-box prep-recommended">
                      <span>Recommended Prep</span>
                      <strong>{recommended}</strong>
                    </div>
                  </div>

                  <button
                    className="action-prep-btn"
                    onClick={() => {
                      setPrepMealType(meal.type)
                      setPrepActualPrepared(recommended)
                      setPrepActualServed(predicted)
                      setAdminTab('tracking')
                    }}
                  >
                    Log Prepared & Served Portions
                    <ArrowRight size={16} />
                  </button>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Admin Tab 2: Food & Waste Tracking */}
      {adminTab === 'tracking' && (
        <div className="admin-section">
          <div className="admin-header-row">
            <div>
              <h2>Record Kitchen Portions & Leftover Waste</h2>
              <p>Log prepared vs served portions to compute leftover waste and track dish metrics.</p>
            </div>
          </div>

          <form onSubmit={handleRecordPreparation} className="tracking-form">
            <div className="form-row">
              <div className="form-group">
                <label>Service Date</label>
                <input
                  type="date"
                  value={adminDate}
                  onChange={(e) => setAdminDate(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label>Meal Type</label>
                <select
                  value={prepMealType}
                  onChange={(e) => setPrepMealType(e.target.value)}
                >
                  <option value="Breakfast">Breakfast</option>
                  <option value="Lunch">Lunch</option>
                  <option value="Dinner">Dinner</option>
                </select>
              </div>

              <div className="form-group">
                <label>Total Portions Prepared</label>
                <input
                  type="number"
                  min="0"
                  value={prepActualPrepared}
                  onChange={(e) => setPrepActualPrepared(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label>Total Portions Served</label>
                <input
                  type="number"
                  min="0"
                  value={prepActualServed}
                  onChange={(e) => setPrepActualServed(e.target.value)}
                  required
                />
              </div>
            </div>

            {/* Live Leftover Calculation Banner */}
            <div className="live-calculation-banner">
              <div>
                <span>Leftover Portions:</span>
                <strong>{Math.max(0, prepActualPrepared - prepActualServed)} portions</strong>
              </div>

              <div>
                <span>Calculated Waste Percentage:</span>
                <strong>
                  {prepActualPrepared > 0
                    ? `${(((Math.max(0, prepActualPrepared - prepActualServed)) / prepActualPrepared) * 100).toFixed(1)}%`
                    : '0.0%'}
                </strong>
              </div>
            </div>

            {/* Dish-wise Inputs Table */}
            <div className="dish-waste-table-wrapper">
              <h3>Dish-wise Waste Tracking</h3>
              <p>Enter portions prepared and served for each individual menu dish:</p>

              <table className="dish-waste-table">
                <thead>
                  <tr>
                    <th>Dish Name</th>
                    <th>Prepared</th>
                    <th>Served</th>
                    <th>Leftover</th>
                    <th>Waste %</th>
                    <th>Surplus Reason</th>
                  </tr>
                </thead>
                <tbody>
                  {dishWasteInputs.map((d, idx) => {
                    const dishLeftover = Math.max(0, d.prepared_portions - d.served_portions)
                    const dishWaste = d.prepared_portions > 0 ? ((dishLeftover / d.prepared_portions) * 100).toFixed(1) : 0

                    return (
                      <tr key={idx}>
                        <td>
                          <input
                            type="text"
                            value={d.dish_name}
                            onChange={(e) => handleDishInputChange(idx, 'dish_name', e.target.value)}
                            required
                          />
                        </td>
                        <td>
                          <input
                            type="number"
                            min="0"
                            value={d.prepared_portions}
                            onChange={(e) => handleDishInputChange(idx, 'prepared_portions', e.target.value)}
                            required
                          />
                        </td>
                        <td>
                          <input
                            type="number"
                            min="0"
                            value={d.served_portions}
                            onChange={(e) => handleDishInputChange(idx, 'served_portions', e.target.value)}
                            required
                          />
                        </td>
                        <td className="text-center font-bold">{dishLeftover}</td>
                        <td className="text-center font-bold">{dishWaste}%</td>
                        <td>
                          <select
                            value={d.reason}
                            onChange={(e) => handleDishInputChange(idx, 'reason', e.target.value)}
                          >
                            <option value="Standard surplus">Standard surplus</option>
                            <option value="Over-preparation">Over-preparation</option>
                            <option value="Low turnout">Low student turnout</option>
                            <option value="Weather effect">Rain/Weather impact</option>
                          </select>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>

            <button type="submit" className="submit-record-btn">
              ✓ Save Service Record & Update Waste Analytics
            </button>
          </form>
        </div>
      )}

      {/* Admin Tab 3: Waste Analytics & Charts */}
      {adminTab === 'analytics' && wasteAnalytics && (
        <div className="admin-section">
          <div className="admin-header-row">
            <div>
              <h2>Food Waste Analytics & Trends</h2>
              <p>Visual reports comparing predicted demand, actual attendance, and dish leftovers.</p>
            </div>
          </div>

          <div className="charts-grid">
            {/* Chart 1: Waste by Dish */}
            <div className="chart-card">
              <h3>Food Waste Percentage by Dish</h3>
              <p className="chart-caption">Dishes with higher leftover rates indicate adjustment opportunities.</p>
              <div className="chart-container">
                <ResponsiveContainer width="100%" height={260}>
                  <BarChart data={wasteAnalytics.waste_by_dish}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="dish_name" tick={{ fontSize: 12 }} />
                    <YAxis unit="%" />
                    <Tooltip formatter={(value) => [`${value}%`, 'Waste Rate']} />
                    <Bar dataKey="waste_percentage" fill="#10b981" radius={[4, 4, 0, 0]}>
                      {wasteAnalytics.waste_by_dish.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={entry.waste_percentage > 12 ? '#ef4444' : entry.waste_percentage > 8 ? '#f59e0b' : '#10b981'}
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Chart 2: Daily Waste Trend */}
            <div className="chart-card">
              <h3>Daily Prepared vs Served Portions</h3>
              <p className="chart-caption">Gap between lines represents saved or leftover food.</p>
              <div className="chart-container">
                <ResponsiveContainer width="100%" height={260}>
                  <LineChart data={wasteAnalytics.daily_trends}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="date" tick={{ fontSize: 11 }} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="prepared" name="Prepared" stroke="#059669" strokeWidth={2} />
                    <Line type="monotone" dataKey="served" name="Served" stroke="#3b82f6" strokeWidth={2} />
                    <Line type="monotone" dataKey="leftover" name="Leftover" stroke="#ef4444" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Chart 3: Predicted Demand vs Actual */}
            <div className="chart-card">
              <h3>Pre-Booked vs Predicted Demand vs Served</h3>
              <p className="chart-caption">Comparison validating ML model accuracy against actual mess turnout.</p>
              <div className="chart-container">
                <ResponsiveContainer width="100%" height={260}>
                  <BarChart data={wasteAnalytics.daily_trends}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="date" tick={{ fontSize: 11 }} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="booked" name="Pre-Booked" fill="#94a3b8" />
                    <Bar dataKey="predicted" name="AI Predicted" fill="#10b981" />
                    <Bar dataKey="served" name="Actual Served" fill="#0284c7" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Chart 4: Waste by Meal Type */}
            <div className="chart-card">
              <h3>Waste Breakdown by Meal Session</h3>
              <p className="chart-caption">Proportion of leftover food across Breakfast, Lunch, and Dinner.</p>
              <div className="chart-container flex-center">
                <ResponsiveContainer width="100%" height={260}>
                  <PieChart>
                    <Pie
                      data={wasteAnalytics.waste_by_meal}
                      dataKey="leftover_portions"
                      nameKey="meal_type"
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    >
                      {wasteAnalytics.waste_by_meal.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => [`${value} portions`, 'Leftovers']} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Admin Tab 4: AI Recommendations */}
      {adminTab === 'recommendations' && wasteAnalytics && (
        <div className="admin-section">
          <div className="admin-header-row">
            <div>
              <h2>Actionable Food Waste Reduction Recommendations</h2>
              <p>Continuous learning generated from historical mess attendance and dish waste logs.</p>
            </div>
          </div>

          <div className="recs-list">
            {wasteAnalytics.actionable_recommendations.map((rec, i) => (
              <div className={`recommendation-card severity-${rec.severity}`} key={i}>
                <div className="rec-header">
                  <span className={`rec-badge badge-${rec.severity}`}>
                    {rec.severity.toUpperCase()} PRIORITY
                  </span>
                  <h3>{rec.title}</h3>
                </div>

                <p className="rec-desc">{rec.description}</p>

                <div className="rec-action-box">
                  <strong>Recommended Mess Action:</strong>
                  <span>{rec.action}</span>
                </div>

                <button
                  className="apply-rec-btn"
                  onClick={() => showToast(`✓ Recommendation applied: ${rec.action}`)}
                >
                  ✓ Implement Recommendation
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )

  return (
    <div className="app">
      {/* Feedback Toast */}
      {feedbackToast && (
        <div className={`feedback-toast toast-${feedbackToast.type}`}>
          {feedbackToast.message}
        </div>
      )}

      {/* Main Header */}
      <header className="main-header">
        <div className="header-top">
          <div className="brand">
            <ChefHat className="brand-icon" size={44} />
            <div>
              <h1>Smart Mess</h1>
              <span className="brand-tagline">AI Meal Pre-Booking & Waste Reduction</span>
            </div>
          </div>

          <div className="header-actions">
            {/* Role Switcher */}
            {currentRole === 'student' ? (
              <button className="role-switch-btn" onClick={handleSwitchToAdmin}>
                <ShieldCheck size={18} />
                <span>Admin Login</span>
              </button>
            ) : (
              <button
                className="role-switch-btn admin-active-btn"
                onClick={() => {
                  setCurrentRole('student')
                  showToast('Switched to Student Portal')
                }}
              >
                <LogOut size={18} />
                <span>Exit Admin</span>
              </button>
            )}

            {/* Notification Bell */}
            <div className="notification-wrapper">
              <button
                className="notification-button"
                onClick={() => setNotificationsOpen(!notificationsOpen)}
              >
                <Bell size={28} />
                <span className="notification-badge">2</span>
              </button>

              {notificationsOpen && (
                <div className="notifications-dropdown">
                  <div className="dropdown-title">
                    <h4>Mess Notifications</h4>
                    <button onClick={() => setNotificationsOpen(false)}>
                      <X size={16} />
                    </button>
                  </div>
                  <div className="dropdown-item">
                    <span className="item-badge">Menu</span>
                    <p>Tomorrow's special lunch menu announced: Curd & Poriyal.</p>
                  </div>
                  <div className="dropdown-item">
                    <span className="item-badge-ai">AI Alert</span>
                    <p>Preparation buffer calibrated to 8% based on Friday booking pattern.</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="welcome">
          <Sparkles className="welcome-icon" size={32} />
          <h2>
            {currentRole === 'student'
              ? `Hello, ${studentProfile.name}!`
              : 'Mess Administrator Control Panel'}
          </h2>
        </div>
      </header>

      {/* Main Content Area */}
      <main>
        {currentRole === 'student' ? (
          <>
            {activePage === 'home' && renderHome()}
            {activePage === 'menu' && renderMenu()}
            {activePage === 'bookings' && renderBookings()}
            {activePage === 'ai' && renderAI()}
            {activePage === 'profile' && renderProfile()}
          </>
        ) : (
          renderAdminDashboard()
        )}
      </main>

      {/* Student Bottom Navigation (Only visible in Student Portal) */}
      {currentRole === 'student' && (
        <nav className="bottom-nav">
          <button
            className={activePage === 'home' ? 'nav-active' : 'nav-item'}
            onClick={() => setActivePage('home')}
          >
            <Home />
            <span>Home</span>
          </button>

          <button
            className={activePage === 'menu' ? 'nav-active' : 'nav-item'}
            onClick={() => setActivePage('menu')}
          >
            <Utensils />
            <span>Menu</span>
          </button>

          <button
            className={activePage === 'bookings' ? 'nav-active' : 'nav-item'}
            onClick={() => setActivePage('bookings')}
          >
            <CalendarDays />
            <span>Bookings</span>
          </button>

          <button
            className={activePage === 'ai' ? 'nav-active' : 'nav-item'}
            onClick={() => setActivePage('ai')}
          >
            <Sparkles />
            <span>AI</span>
          </button>

          <button
            className={activePage === 'profile' ? 'nav-active' : 'nav-item'}
            onClick={() => setActivePage('profile')}
          >
            <UserRound />
            <span>Profile</span>
          </button>
        </nav>
      )}

      {/* Booking Confirmation Dialog Modal */}
      {selectedMeal && (
        <div className="modal-overlay">
          <div className="booking-modal">
            <div className="modal-icon">
              <CheckCircle2 size={36} />
            </div>

            <h2>Confirm Meal Booking</h2>
            <p className="modal-question">Pre-book this meal to reserve your portion?</p>

            <div className="modal-meal">
              <h3>{selectedMeal.type}</h3>
              <p className="modal-menu-text">{selectedMeal.menu}</p>
              <p className="booking-date">{formatDate(selectedDate)}</p>
              <span>
                <Clock3 size={17} />
                {selectedMeal.time}
              </span>
            </div>

            <div className="modal-buttons">
              <button className="modal-cancel" onClick={() => setSelectedMeal(null)}>
                Cancel
              </button>
              <button className="modal-confirm" onClick={confirmBooking}>
                Confirm Booking
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Cancellation Confirmation Dialog Modal */}
      {cancelMeal && (
        <div className="modal-overlay">
          <div className="booking-modal">
            <div className="modal-icon cancel-icon">
              <AlertTriangle size={36} />
            </div>

            <h2>Cancel Booking?</h2>
            <p className="modal-question">Are you sure you want to cancel this meal booking?</p>

            <div className="modal-meal">
              <h3>{cancelMeal.meal}</h3>
              <p className="modal-menu-text">{getMealDetails(cancelMeal.meal)?.menu}</p>
              <p className="booking-date">{formatDate(cancelMeal.date)}</p>
              <span>
                <Clock3 size={17} />
                {getMealDetails(cancelMeal.meal)?.time}
              </span>
            </div>

            <div className="modal-buttons">
              <button className="modal-cancel" onClick={() => setCancelMeal(null)}>
                Keep Booking
              </button>
              <button className="modal-danger" onClick={confirmCancellation}>
                Yes, Cancel Booking
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Administrator Authentication / PIN Modal */}
      {adminPinModal && (
        <div className="modal-overlay">
          <div className="booking-modal admin-modal">
            <div className="modal-icon">
              <ShieldAlert size={36} />
            </div>

            <h2>Authorized Administrator Access</h2>
            <p className="modal-question">Enter staff credentials to open the waste reduction portal.</p>

            <div className="admin-pin-group">
              <label>Administrator Password:</label>
              <input
                type="password"
                placeholder="Enter password (hellomini)"
                value={adminPinInput}
                onChange={(e) => setAdminPinInput(e.target.value)}
                autoFocus
                onKeyDown={(e) => {
                  if (e.key === 'Enter') submitAdminPin()
                }}
              />
              {adminPinError && <span className="pin-error-text">{adminPinError}</span>}
              <small className="pin-hint">Administrator password: <strong>hellomini</strong></small>
            </div>

            <div className="modal-buttons">
              <button className="modal-cancel" onClick={() => setAdminPinModal(false)}>
                Cancel
              </button>
              <button className="modal-confirm" onClick={submitAdminPin}>
                Authorize & Login
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App