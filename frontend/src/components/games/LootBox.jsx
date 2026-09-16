import React, { useEffect, useRef, useState } from 'react'
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

const CARD_W = 176
const GAP = 14
const STEP = CARD_W + GAP
const WINNER_INDEX = 14
const AFTER_WINNER = 8
const REEL_LEN = WINNER_INDEX + AFTER_WINNER + 1
const SPIN_MS = 2600

const RARITY_TIER = {
  common: 'THƯỜNG',
  rare: 'HIẾM',
  epic: 'SỬ THI',
  legendary: 'HUYỀN THOẠI',
}

const RARITY_COLOR = {
  common: '#9d998d',
  rare: '#71a69a',
  epic: '#aa8cbb',
  legendary: '#e4c879',
}

function shuffle(arr) {
  const a = arr.slice()
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

export default function LootBox({ onSpinStart }) {
  const [budget, setBudget] = useState('t30_60')
  const [meal, setMeal] = useState('')
  const [state, setState] = useState('idle') // idle | spinning | result | error
  const [reel, setReel] = useState([])
  const [translate, setTranslate] = useState(0)
  const [transition, setTransition] = useState('none')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const winRef = useRef(null)
  const timerRef = useRef(null)

  useEffect(() => () => clearTimeout(timerRef.current), [])

  const openBox = async () => {
    if (state === 'spinning') return
    setState('spinning')
    setResult(null)
    setError('')
    if (onSpinStart) onSpinStart()

    try {
      const p = new URLSearchParams()
      const budgetQ = budgetParam(budget)
      if (meal) p.set('meal', meal)
      if (budgetQ.min_price) p.set('min_price', budgetQ.min_price)
      if (budgetQ.max_price) p.set('max_price', budgetQ.max_price)
      const q = p.toString()
      const res = await fetch(`${API}/api/dishes${q ? `?${q}` : ''}`)
      if (!res.ok) throw new Error('Không lấy được danh sách món')
      const list = await res.json()
      if (!list.length) throw new Error('Không có món nào khớp — thử tăng ngân sách hoặc đổi bữa nhé!')
      const winner = list[Math.floor(Math.random() * list.length)]

      const raw = [winner, ...shuffle(list.filter((d) => d.id !== winner.id))]
      const startOff = Math.floor(Math.random() * raw.length)
      const cards = []
      for (let i = 0; i < REEL_LEN; i++) {
        if (i === WINNER_INDEX) cards.push(winner)
        else cards.push(raw[(startOff + i) % raw.length])
      }
      setReel(cards)

      const winW = winRef.current ? winRef.current.clientWidth : 640
      const trackW = cards.length * STEP - GAP
      let finalX = WINNER_INDEX * STEP + CARD_W / 2 - winW / 2
      finalX = Math.max(0, Math.min(finalX, trackW - winW))
      const startX = Math.floor(Math.random() * Math.min(180, finalX))

      setTransition('none')
      setTranslate(startX)
      await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))
      setTransition('transform 2500ms cubic-bezier(.09,.72,.08,1) 80ms')
      setTranslate(finalX)

      timerRef.current = setTimeout(() => {
        setState('result')
        setResult(winner)
      }, SPIN_MS)
    } catch (e) {
      setState('error')
      setError(e.message)
    }
  }

  const hasResult = state === 'result' && result

  return (
    <div className="lootbox">
      <div className="lootbox-head">
        <h2 className="lootbox-title"><span className="loot-icon">📦</span> Hòm tiếp tế Hà Nội</h2>
        <p className="lootbox-sub">Chọn ngân sách, quay hòm &amp; để trời quyết định bữa nay ăn gì!</p>
      </div>

      <div className={`reel-window ${state === 'spinning' ? 'reel-spinning' : ''}`} ref={winRef}>
        <div className="reel-selector" />
        {state === 'spinning' && <div className="reel-scanline" />}
        <div
          className="reel-track"
          style={{ transform: `translateX(-${translate}px)`, transition }}
        >
          {reel.map((d, i) => {
            const color = RARITY_COLOR[d.rarity.key] || RARITY_COLOR.common
            return (
              <article
                className={`reel-card ${i === WINNER_INDEX ? 'reel-card-land' : ''}`}
                key={`${d.id}-${i}`}
                style={{ '--rc': color }}
              >
                <span className="reel-card-tier">{RARITY_TIER[d.rarity.key] || 'THƯỜNG'}</span>
                <img
                  src={d.image_url || '/images/fallback.svg'}
                  alt={d.name}
                  loading="lazy"
                  onError={(e) => { e.target.src = '/images/fallback.svg' }}
                />
                <strong className="reel-card-name">{d.name}</strong>
                <span className="reel-card-sub">
                  {d.avg_price > 0 ? `${d.avg_price.toLocaleString('vi-VN')}đ` : 'Giá: chưa rõ'}
                </span>
              </article>
            )
          })}
        </div>
        <div className="reel-fade reel-fade-left" />
        <div className="reel-fade reel-fade-right" />
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

      {state === 'error' && (
        <div className="lootbox-error">{error}</div>
      )}

      {state === 'spinning' && (
        <div className="reel-spinning-hint">📦 Đang lựa chọn cho bạn...</div>
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
  )
}