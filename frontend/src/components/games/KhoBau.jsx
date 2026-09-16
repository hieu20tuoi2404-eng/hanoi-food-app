import React, { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import RarityBadge from '../cards/RarityBadge'
import { BUDGETS, budgetParam } from '../widgets/FilterBar'

const API = import.meta.env.VITE_API_BASE || ''

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

export default function KhoBau() {
  const [budget, setBudget] = useState('t30_60')
  const [meal, setMeal] = useState('')
  const [state, setState] = useState('idle')
  const [reel, setReel] = useState([])
  const [translate, setTranslate] = useState(0)
  const [transition, setTransition] = useState('none')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const winRef = useRef(null)
  const timerRef = useRef(null)

  useEffect(() => () => clearTimeout(timerRef.current), [])

  const spin = async () => {
    if (state === 'spinning') return
    setState('spinning')
    setResult(null)
    setError('')

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
      setState('idle')
      setError(e.message)
    }
  }

  const reset = () => {
    setState('idle')
    setResult(null)
    setReel([])
    setTranslate(0)
    setTransition('none')
    setError('')
  }

  const hasResult = state === 'result' && result

  return (
    <div className="kho-bau">
      <div className="kho-bau-head">
        <div className="kho-bau-tag">HỘI THỢ LÙN · KHO BÁU LÒ RÈN</div>
        <h2 className="kho-bau-title">KÉT KHO BÁU</h2>
        <p className="kho-bau-sub">Khai mở vận may — Lăn xèng thấy món ngon!</p>
      </div>

      <div className={`kho-bau-window ${state === 'spinning' ? 'kho-bau-spinning' : ''}`} ref={winRef}>
        <div className="kho-bau-selector" />
        {state === 'spinning' && <div className="kho-bau-scanline" />}
        <div className="kho-bau-track" style={{ transform: `translateX(-${translate}px)`, transition }}>
          {reel.map((d, i) => {
            const color = RARITY_COLOR[d.rarity.key] || RARITY_COLOR.common
            return (
              <article className={`kho-bau-card ${i === WINNER_INDEX ? 'kho-bau-card-land' : ''}`} key={`${d.id}-${i}`} style={{ '--rc': color }}>
                <span className="kho-bau-tier">{RARITY_TIER[d.rarity.key] || 'THƯỜNG'}</span>
                <img
                  src={d.image_url || '/images/fallback.svg'}
                  alt={d.name}
                  loading="lazy"
                  onError={(e) => { e.target.src = '/images/fallback.svg' }}
                />
                <strong className="kho-bau-name">{d.name}</strong>
                <span className="kho-bau-sub2">
                  {d.avg_price > 0 ? `${d.avg_price.toLocaleString('vi-VN')}đ` : 'Giá: chưa rõ'}
                </span>
              </article>
            )
          })}
        </div>
        <div className="kho-bau-fade-left" />
        <div className="kho-bau-fade-right" />
      </div>

      <div className="kho-bau-controls">
        <div className="kho-bau-opt">
          <label>Ngân sách</label>
          <select value={budget} onChange={(e) => setBudget(e.target.value)}>
            {BUDGETS.map((b) => <option key={b.id} value={b.id}>{b.icon} {b.label}</option>)}
          </select>
        </div>
        <div className="kho-bau-opt">
          <label>Loại bữa</label>
          <select value={meal} onChange={(e) => setMeal(e.target.value)}>
            <option value="">Mọi bữa</option>
            <option value="breakfast">Bữa sáng</option>
            <option value="lunch">Bữa trưa</option>
            <option value="dinner">Bữa tối</option>
            <option value="snack">Ăn vặt</option>
            <option value="drinking">Món nhậu</option>
          </select>
        </div>
        {state === 'spinning' ? (
          <div className="kho-bau-status">Đang lăn xèng...</div>
        ) : result ? (
          <button className="kho-bau-btn kho-bau-btn-reset" onClick={reset} type="button">QUAY LẠI 🔄</button>
        ) : (
          <button className="kho-bau-btn" onClick={spin} type="button">MỞ KÉT 🎰</button>
        )}
      </div>

      {error && <div className="kho-bau-error">{error}</div>}

      {hasResult && (
        <div className={`kho-bau-result rarity-card-${result.rarity.key}`}>
          <div className="kho-bau-result-top">
            <span className="kho-bau-result-label">QUẺ CỦA BẠN</span>
            <RarityBadge rarity={result.rarity} />
          </div>
          <div className="kho-bau-result-main">
            <img
              src={result.image_url || '/images/fallback.svg'}
              alt={result.name}
              className="kho-bau-result-img"
              onError={(e) => { e.target.src = '/images/fallback.svg' }}
            />
            <div className="kho-bau-result-info">
              <div className="kho-bau-result-name">{result.name}</div>
              <div className="kho-bau-result-meta">
                <span>&#9733; {result.avg_rating.toFixed(1)}/10</span>
                <span>{result.avg_price.toLocaleString('vi-VN')}đ</span>
              </div>
              <p className="kho-bau-result-desc">{result.description}</p>
              <Link to={`/dish/${result.slug}`} className="kho-bau-result-link">
                Xem chi tiết + quán + công thức &#8594;
              </Link>
              {result.is_demo && <div className="dish-card-demo">Dữ liệu Demo — Chưa xác minh</div>}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}