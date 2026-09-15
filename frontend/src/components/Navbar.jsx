import React, { useEffect, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import ThemeSwitcher from './ThemeSwitcher'
import { useApp } from '../context/AppContext'

export default function Navbar() {
  const [now, setNow] = useState(new Date())
  const loc = useLocation()
  const { mascot } = useApp()

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
          {mascot && (
            <Link to="/chon-con-giap" className="navbar-mascot" title={`Đổi linh vật (${mascot.name} – ${mascot.animal})`}>
              <span className="navbar-mascot-emoji" style={{ '--mascot-color': mascot.theme_color }}>
                {mascot.emoji}
              </span>
            </Link>
          )}
          {loc.pathname !== '/bo-suu-tap' && (
            <Link to="/bo-suu-tap" className="navbar-collection-link">🎮 Bộ sưu tập</Link>
          )}
          {loc.pathname === '/bo-suu-tap' && (
            <Link to="/" className="navbar-collection-link">🏠 Trang chủ</Link>
          )}
          {loc.pathname !== '/cai-dat' && (
            <Link to="/cai-dat" className="navbar-collection-link">⚙️ Cài đặt</Link>
          )}
          <ThemeSwitcher />
          <span className="navbar-quote">"Ăn gì hôm nay?"</span>
          <span className="navbar-clock">{vn}</span>
        </div>
      </div>
    </div>
  )
}