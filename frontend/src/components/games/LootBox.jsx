import React, { useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import RarityBadge from '../cards/RarityBadge'
import { BUDGETS, budgetParam } from '../widgets/FilterBar'

const API = import.meta.env.VITE_API_BASE || ''

export const MEAL_OPTIONS = [
  { slug: '', label: 'Mọi bữa' },
  { slug: 'breakfast', label: 'Bữa sáng' },
  { slug: 'lunch', label: 'Bữa trưa' },
  { slug: 'dinner', label: 'Bữa tối' },
  { slug: 'snack', label: 'Ăn vặt' },
  { slug: 'drinking', label: 'Món nhậu' },
]

export default function LootBox({ onSpinStart }) {
  const [budget, setBudget] = useState('t30_60')
  const [meal, setMeal] = useState('')
  const [state, setState] = useState('idle') // idle | spinning | result | error
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [flash, setFlash] = useState(0)
  const spins = useRef(0)

  const openBox = async () => {
    setState('spinning')
    setResult(null)
    setError('')
    setFlash(0)
    spins.current = 0
    if (onSpinStart) onSpinStart()

    // fun spinning animation
    const spinTimer = setInterval(() => {
      spins.current += 1
      setFlash(spins.current)
    }, 140)

    try {
      const p = new URLSearchParams()
      const budgetQ = budgetParam(budget)
      if (meal) p.set('meal', meal)
      if (budgetQ.min_price) p.set('min_price', budgetQ.min_price)
      if (budgetQ.max_price) p.set('max_price', budgetQ.max_price)
      const q = p.toString()
      const res = await fetch(`${API}/api/dishes/random${q ? `?${q}` : ''}`)
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || 'Không có món phù hợp với ngân sách này')
      }
      const dish = await res.json()
      // tiny delay so the spinner is visible
      await new Promise((r) => setTimeout(r, 900))
      clearInterval(spinTimer)
      setResult(dish)
      setState('result')
    } catch (e) {
      clearInterval(spinTimer)
      setError(e.message)
      setState('error')
    }
  }

  const hasResult = state === 'result' && result

  return (
    <div className="lootbox">
      <div className="lootbox-head">
        <h2 className="lootbox-title"><span className="loot-icon">📦</span> Hòm tiếp tế Hà Nội</h2>
        <p className="lootbox-sub">Chọn ngân sách, mở hòm &amp; để trời quyết định bữa nay ăn gì!</p>
      </div>

      <div className="lootbox-controls">
        <div className="lootbox-option">
          <label>Ngân sách</label>
          <select value={budget} onChange={(e) => setBudget(e.target.value)}>
            {BUDGETS.map((b) => (
              <option key={b.id} value={b.id}>{b.icon} {b.label}</option>
            ))}
          </select>
        </div>
        <div className="lootbox-option">
          <label>Loại bữa</label>
          <select value={meal} onChange={(e) => setMeal(e.target.value)}>
            {MEAL_OPTIONS.map((m) => (
              <option key={m.slug} value={m.slug}>{m.label}</option>
            ))}
          </select>
        </div>

        <button
          className="lootbox-open"
          onClick={openBox}
          disabled={state === 'spinning'}
          type="button"
        >
          {state === 'spinning' ? 'Đang mở hòm...' : 'MỞ HÒM 🎲'}
        </button>
      </div>

      {/* Spinner / result zone */}
      <div className="lootbox-stage">
        {state === 'spinning' && (
          <div className="lootbox-spin">
            <div className={`lootbox-lid ${flash % 2 ? 'lid-up' : 'lid-down'}`} aria-hidden="true" />
            <div className="lootbox-particles">
              {Array.from({ length: 8 }).map((_, i) => (
                <span key={i} className="particle" style={{ ['--i']: i }} />
              ))}
            </div>
            <div className="lootbox-spin-text">Đang lựa chọn cho bạn...</div>
          </div>
        )}

        {state === 'error' && (
          <div className="lootbox-error">
            Không có món nào khớp — thử tăng ngân sách hoặc đổi bữa nhé!
          </div>
        )}

        {hasResult && (
          <div className={`lootbox-result rarity-card-${result.rarity.key}`}>
            <div className="lootbox-result-top">
              <span className="lootbox-result-label">QUẺ CỦA BẠN</span>
              <RarityBadge rarity={result.rarity} />
            </div>
            <div className="lootbox-result-main">
              <img
                src={result.image_url || '/images/fallback.svg'}
                alt={result.name}
                className="lootbox-result-img"
                onError={(e) => { e.target.src = '/images/fallback.svg' }}
              />
              <div className="lootbox-result-info">
                <div className="lootbox-result-name">{result.name}</div>
                <div className="lootbox-result-meta">
                  <span className="dish-card-rating">&#9733; {result.avg_rating.toFixed(1)}/10</span>
                  <span className="dish-card-price">{result.avg_price.toLocaleString('vi-VN')}đ</span>
                </div>
                <p className="lootbox-result-desc">{result.description}</p>
                <Link to={`/dish/${result.slug}`} className="lootbox-result-link">
                  Xem chi tiết + quán + công thức &#8594;
                </Link>
                {result.is_demo && <div className="dish-card-demo">Dữ liệu Demo - Chưa xác minh</div>}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}