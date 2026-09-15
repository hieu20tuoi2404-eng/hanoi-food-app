import React, { useEffect, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import ThemeSwitcher from './ThemeSwitcher'

export default function Navbar() {
  const [now, setNow] = useState(new Date())
  const loc = useLocation()

  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 1000)
    return () => clearInterval(timer)
  }, [])

  const vn = new Intl.DateTimeFormat('vi-VN', {
    weekday: 'long',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }).format(now)

  return (
    <div className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="navbar-brand">
          <span className="navbar-logo">🍜</span>
          An Gi Ha Noi?
          <span className="navbar-tag">Hà Nội food roulette</span>
        </Link>
        <div className="navbar-right">
          {loc.pathname !== '/bo-suu-tap' && (
            <Link to="/bo-suu-tap" className="navbar-collection-link">🎮 Bộ sưu tập</Link>
          )}
          {loc.pathname === '/bo-suu-tap' && (
            <Link to="/" className="navbar-collection-link">🏠 Trang chủ</Link>
          )}
          <ThemeSwitcher />
          <span className="navbar-quote">"Ăn gì hôm nay?"</span>
          <span className="navbar-clock">{vn}</span>
        </div>
      </div>
    </div>
  )
}