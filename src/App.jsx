import { useState } from 'react'
import './App.css'

function App() {
  const [activePage, setActivePage] = useState('home')
  const [bookedMeal, setBookedMeal] = useState(null)

  const meals = [
    {
      type: 'Breakfast',
      icon: '🍳',
      time: '7:30 AM - 9:00 AM',
      menu: 'Idli, Sambar & Chutney',
    },
    {
      type: 'Lunch',
      icon: '🍛',
      time: '12:00 PM - 2:00 PM',
      menu: 'Rice, Sambar, Poriyal & Curd',
    },
    {
      type: 'Dinner',
      icon: '🥘',
      time: '7:00 PM - 8:30 PM',
      menu: 'Chapati & Vegetable Curry',
    },
  ]

  const renderPage = () => {
    if (activePage === 'home') {
      return (
        <>
          <h2>Today's Menu</h2>

          <div className="meal-list">
            {meals.map((meal) => (
              <div className="meal-card" key={meal.type}>
                <div className="meal-icon">{meal.icon}</div>

                <div className="meal-info">
                  <h3>{meal.type}</h3>
                  <p>{meal.menu}</p>
                  <small>{meal.time}</small>
                </div>

                <button
                  onClick={() => setBookedMeal(meal.type)}
                  disabled={bookedMeal === meal.type}
                >
                  {bookedMeal === meal.type ? 'Booked' : 'Book'}
                </button>
              </div>
            ))}
          </div>

          {bookedMeal && (
            <div className="booking-message">
              Your {bookedMeal.toLowerCase()} is booked!
            </div>
          )}
        </>
      )
    }

    if (activePage === 'menu') {
      return (
        <>
          <h2>Menu</h2>
          <p>View breakfast, lunch and dinner menus here.</p>
        </>
      )
    }

    if (activePage === 'bookings') {
      return (
        <>
          <h2>My Bookings</h2>
          {bookedMeal ? (
            <p>You have booked: {bookedMeal}</p>
          ) : (
            <p>No meals booked yet.</p>
          )}
        </>
      )
    }

    if (activePage === 'ai') {
      return (
        <>
          <h2>AI Assistant</h2>
          <p>Your smart meal assistant will appear here.</p>
        </>
      )
    }

    if (activePage === 'profile') {
      return (
        <>
          <h2>Profile</h2>
          <p>Student profile will appear here.</p>
        </>
      )
    }
  }

  return (
    <div className="app">
      <header>
        <h1>Smart Mess</h1>
        <p>Good morning!</p>
      </header>

      <main>{renderPage()}</main>

      <nav>
        <button
          className={activePage === 'home' ? 'nav-active' : 'nav-item'}
          onClick={() => setActivePage('home')}
        >
          Home
        </button>

        <button
          className={activePage === 'menu' ? 'nav-active' : 'nav-item'}
          onClick={() => setActivePage('menu')}
        >
          Menu
        </button>

        <button
          className={activePage === 'bookings' ? 'nav-active' : 'nav-item'}
          onClick={() => setActivePage('bookings')}
        >
          Bookings
        </button>

        <button
          className={activePage === 'ai' ? 'nav-active' : 'nav-item'}
          onClick={() => setActivePage('ai')}
        >
          AI
        </button>

        <button
          className={activePage === 'profile' ? 'nav-active' : 'nav-item'}
          onClick={() => setActivePage('profile')}
        >
          Profile
        </button>
      </nav>
    </div>
  )
}

export default App