import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import DishDetail from './pages/DishDetail'

export default function App() {
  return (
    <div className="app">
      <Navbar />
      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dish/:slug" element={<DishDetail />} />
        </Routes>
      </main>
    </div>
  )
}
