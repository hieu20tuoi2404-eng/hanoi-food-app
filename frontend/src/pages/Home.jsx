import React, { useCallback, useEffect, useState } from 'react'
import DishCard from '../components/DishCard'
import FilterBar from '../components/FilterBar'
import LootBox from '../components/LootBox'
import QuaTrua from '../components/QuaTrua'
import ExplorationProfile from '../components/ExplorationProfile'
import ZodiacWidget from '../components/ZodiacWidget'
import FateDice from '../components/FateDice'
import GroupVote from '../components/GroupVote'
import { Link } from 'react-router-dom'
import { useApp } from '../context/AppContext'

const API = import.meta.env.VITE_API_BASE || ''

const CATEGORIES = [
  { slug: '', label: 'Tất cả' },
  { slug: 'breakfast', label: 'Bữa sáng' },
  { slug: 'lunch', label: 'Bữa trưa' },
  { slug: 'dinner', label: 'Bữa tối' },
  { slug: 'snack', label: 'Ăn vặt' },
  { slug: 'drinking', label: 'Món nhậu' },
]

const CATEGORY_ICONS = { '': '🍽', breakfast: '☀️', lunch: '🍚', dinner: '🌙', snack: '🍿', drinking: '🍻' }

const PRICE_RANGES = {
  '': '',
  below30: { label: 'Dưới 30.000đ', min_price: 0, max_price: 30000 },
  mid: { label: '30.000 - 100.000đ', min_price: 30000, max_price: 100000 },
  above100: { label: 'Trên 100.000đ', min_price: 100000, max_price: '' },
}

function toQuery(meal, f, search) {
  const p = new URLSearchParams()
  if (meal) p.set('meal', meal)
  if (search) p.set('search', search)
  if (f.district) p.set('district', f.district)
  if (f.min_price !== undefined && f.min_price !== '') p.set('min_price', f.min_price)
  if (f.max_price !== undefined && f.max_price !== '') p.set('max_price', f.max_price)
  if (f.min_rating) p.set('min_rating', f.min_rating)
  if (f.diet) p.set('diet', f.diet)
  if (f.occasion) p.set('occasion', f.occasion)
  if (f.color) p.set('color', f.color)
  const q = p.toString()
  return q ? `?${q}` : ''
}

export default function Home() {
  const { mascot } = useApp()
  const [meal, setMeal] = useState('')
  const [filters, setFilters] = useState({ district: '', price: '', min_rating: '', diet: '', occasion: '', color: '' })
  const [search, setSearch] = useState('')
  const [dishes, setDishes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const buildFilters = useCallback((f) => {
    const base = { district: f.district || '', min_rating: f.min_rating || '' }
    if (!f.price) return { ...base, min_price: '', max_price: '' }
    const r = PRICE_RANGES[f.price]
    return { ...base, min_price: r.min_price, max_price: r.max_price }
  }, [])

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setError('')
    const q = toQuery(meal, buildFilters(filters), search)
    fetch(`${API}/api/dishes${q}`)
      .then((r) => {
        if (!r.ok) throw new Error('Lỗi tải danh sách')
        return r.json()
      })
      .then((data) => {
        if (!cancelled) setDishes(data)
      })
      .catch((e) => {
        if (!cancelled) setError(e.message)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [meal, filters, buildFilters, search])

  const activeCount = dishes.length

  return (
    <div>
      {/* Hero */}
      <div className="hero">
        <div className="hero-inner">
          <h1 className="hero-title">Hà Nội hôm nay ĂN GÌ?</h1>
          <p className="hero-sub">
            30 món Hà Nội chính hiệu, từ quán vỉa hè tới mâm cơm gia đình.
            Không biết ăn gì? Để "hòm tiếp tế" quay giúp bạn! 🎲
          </p>
          {mascot && (
            <div className="hero-mascot" style={{ '--mascot-color': mascot.theme_color }}>
              <span className="hero-mascot-emoji">{mascot.emoji}</span>
              <p className="hero-mascot-greeting">
                <b>{mascot.name} – {mascot.animal}</b> nói: "{mascot.greeting}"
              </p>
            </div>
          )}
          <div className="hero-stats">
            <span className="hero-stat"><b>{activeCount}</b> món</span>
            <span className="hero-stat"><b>4</b> bữa</span>
            <span className="hero-stat"><b>9</b> quận</span>
            <span className="hero-stat"><b>100%</b> demo</span>
          </div>
        </div>
      </div>

      {/* Drivable widget row */}
      <div className="widgets-row">
        <FateDice />
        <ZodiacWidget />
        <GroupVote />
      </div>

      {/* Exploration profile */}
      <ExplorationProfile />

      {/* Loot box */}
      <LootBox />

      {/* Quẻ trưa */}
      <QuaTrua />

      {/* Category tabs */}
      <div className="category-bar">
        {CATEGORIES.map((c) => (
          <button
            key={c.slug}
            className={`category-btn ${meal === c.slug ? 'active' : ''}`}
            onClick={() => setMeal(c.slug)}
          >
            <span className="category-icon">{CATEGORY_ICONS[c.slug]}</span>
            {c.label}
          </button>
        ))}
      </div>

      {/* Search */}
      <div className="search-bar">
        <input
          type="search"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Tìm món... ví dụ: phở, bún chả, xôi"
          className="search-input"
        />
      </div>

      <FilterBar filters={{ ...filters, price: filters.price }} onChange={setFilters} />

      <div className="section">
        <h2 className="section-title">
          {search ? `Kết quả tìm "${search}"` : meal ? CATEGORIES.find((c) => c.slug === meal).label : 'Kho tiếp tế - mọi món'}
        </h2>
        {loading && <div className="loading">Đang tải món ăn...</div>}
        {error && !loading && <div className="empty">Lỗi: {error}</div>}

        {!loading && !error && dishes.length === 0 && (
          <div className="empty">
            {mascot
              ? <>
                  <span className="empty-mascot-emoji">{mascot.emoji}</span>
                  "{mascot.encouragement}"
                </>
              : 'Không có món phù hợp. Thử đổi bộ lọc hoặc bớt từ khoá tìm nhé!'}
            <br />
            <Link className="back-link" to="/">&#8592; Reset</Link>
          </div>
        )}

        {!loading && dishes.length > 0 && (
          <div className="dish-grid">
            {dishes.map((d) => (
              <DishCard key={d.id} dish={d} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}