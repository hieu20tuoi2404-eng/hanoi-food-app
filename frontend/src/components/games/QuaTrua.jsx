import React, { useState, useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import RarityBadge from '../cards/RarityBadge'
import { useApp } from '../../context/AppContext'

const API = import.meta.env.VITE_API_BASE || ''

const CARD_W = 176
const GAP = 14
const STEP = CARD_W + GAP
const WINNER_INDEX = 14
const AFTER_WINNER = 8
const REEL_LEN = WINNER_INDEX + AFTER_WINNER + 1
const SPIN_MS = 2600

const KINDS = [
  { id: '', label: 'Bất kỳ', emoji: '🎲' },
  { id: 'breakfast', label: 'Bữa sáng', emoji: '☕' },
  { id: 'lunch', label: 'Bữa trưa', emoji: '🍚' },
  { id: 'dinner', label: 'Bữa tối', emoji: '🌙' },
  { id: 'snack', label: 'Ăn vặt', emoji: '🍿' },
  { id: 'drinking', label: 'Món nhậu', emoji: '🍻' },
]

const BUDGETS = [
  { value: 0, label: 'Thả ga', emoji: '💸' },
  { value: 50000, label: '≤ 50k', emoji: '🍜' },
  { value: 100000, label: '≤ 100k', emoji: '🥘' },
  { value: 200000, label: '≤ 200k', emoji: '🍱' },
]

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

export default function QuaTrua() {
  const { mascot } = useApp()
  const [pool, setPool] = useState([])
  const [kind, setKind] = useState('')
  const [budget, setBudget] = useState(0)
  const [phase, setPhase] = useState('idle')
  const [reel, setReel] = useState([])
  const [translate, setTranslate] = useState(0)
  const [transition, setTransition] = useState('none')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const winRef = useRef(null)
  const timerRef = useRef(null)

  useEffect(() => {
    let cancelled = false
    fetch(`${API}/api/dishes`)
      .then((r) => r.json())
      .then((list) => {
        if (!cancelled) setPool(list)
      })
      .catch(() => {})
    return () => {
      cancelled = true
      clearTimeout(timerRef.current)
    }
  }, [])

  const spin = async () => {
    if (phase === 'spinning') return
    setError('')
    setResult(null)
    setPhase('spinning')
    try {
      const params = new URLSearchParams()
      if (kind) params.set('meal', kind)
      if (budget > 0) params.set('budget', budget)
      const res = await fetch(`${API}/api/fortunes?${params}`)
      if (!res.ok) throw new Error('Chưa xin được quẻ. Thử lại nhé!')
      const data = await res.json()
      const winner = data.dish

      let fpool = pool
      if (kind) fpool = fpool.filter((d) => d.meal_type === kind)
      if (budget > 0) fpool = fpool.filter((d) => d.avg_price > 0 && d.avg_price <= budget)
      if (!fpool.length) fpool = [winner]

      const raw = [winner, ...shuffle(fpool.filter((d) => d.id !== winner.id))]
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
        setPhase('idle')
        setResult({ winner, fortune: data.fortune, luck: data.luck })
      }, SPIN_MS)
    } catch (e) {
      setPhase('idle')
      setError(e.message)
    }
  }

  const kindLabel = KINDS.find((k) => k.id === kind)
  const budgetLabel = BUDGETS.find((b) => b.value === budget)

  return (
    <div className="quatrua">
      <div className="quatrua-head">
        <h2 className="quatrua-title"><span className="loot-icon">🔮</span> Gieo quẻ</h2>
        <p className="quatrua-sub">Gieo một quẻ xem ăn gì cho &quot;hợp duyên&quot;! Ấn nút để gieo quẻ nhé.</p>
      </div>

      <div className={`reel-window ${phase === 'spinning' ? 'reel-spinning' : ''}`} ref={winRef}>
        {phase === 'spinning' && <div className="reel-scanline" />}
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
                <span className="reel-card-sub">{d.avg_price > 0 ? `${d.avg_price.toLocaleString('vi-VN')}đ` : 'Giá: chưa rõ'}</span>
              </article>
            )
          })}
        </div>
        <div className="reel-fade reel-fade-left" />
        <div className="reel-fade reel-fade-right" />
        <div className="reel-selector" />
      </div>

      <div className="reel-options">
        <div className="reel-option-row">
          <span className="reel-opt-label">Bữa</span>
          <div className="reel-chips">
            {KINDS.map((k) => (
              <button
                key={k.id || 'any'}
                type="button"
                className={`reel-chip ${kind === k.id ? 'active' : ''}`}
                onClick={() => setKind(k.id)}
              >
                <span className="reel-chip-emoji">{k.emoji}</span> {k.label}
              </button>
            ))}
          </div>
        </div>
        <div className="reel-option-row">
          <span className="reel-opt-label">Ngân sách</span>
          <div className="reel-chips">
            {BUDGETS.map((b) => (
              <button
                key={b.value}
                type="button"
                className={`reel-chip ${budget === b.value ? 'active' : ''}`}
                onClick={() => setBudget(b.value)}
              >
                <span className="reel-chip-emoji">{b.emoji}</span> {b.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <button className="reel-spin" onClick={spin} disabled={phase === 'spinning'} type="button">
        {phase === 'spinning' ? 'Đang quay...' : '🎰 GIEO QUẺ'}
      </button>

      {error && <div className="lootbox-error">{error}</div>}

      {result && phase === 'idle' && (
        <div className={`quatrua-result rarity-card-${result.winner.rarity.key}`}>
          <p className="quatrua-fortune">"{result.fortune}"</p>
          <div className="lootbox-result-main">
            <img
              src={result.winner.image_url || '/images/fallback.svg'}
              alt={result.winner.name}
              className="lootbox-result-img"
              onError={(e) => { e.target.src = '/images/fallback.svg' }}
            />
            <div className="lootbox-result-info">
              <div className="lootbox-result-top" style={{ marginBottom: 6 }}>
                <span className="lootbox-result-label">QUẺ CỦA BẠN</span>
                <RarityBadge rarity={result.winner.rarity} />
              </div>
              <div className="lootbox-result-name">{result.winner.name}</div>
              <div className="lootbox-result-meta">
                <span className="dish-card-rating">&#9733; {result.winner.avg_rating.toFixed(1)}/10</span>
                <span className="dish-card-price">
                  {result.winner.avg_price > 0 ? `${result.winner.avg_price.toLocaleString('vi-VN')}đ` : 'Giá: chưa rõ'}
                </span>
              </div>
              <Link to={`/dish/${result.winner.slug}`} className="lootbox-result-link">
                Xem chi tiết &#8594;
              </Link>
            </div>
          </div>
          <p className="quatrua-mascot">
            {mascot
              ? `${mascot.emoji} Gợi ý vui từ linh vật ${mascot.name}: để cơ duyên dẫn đường, đừng nghĩ quá nhiều bạn nhé!`
              : '🔮 Cơ duyên đã chỉ đường, ăn thôi!'}
          </p>
        </div>
      )}

      {phase === 'spinning' && (
        <div className="reel-spinning-hint">
          {(kindLabel ? `${kindLabel.emoji} ${kindLabel.label}` : '🎲 Bất kỳ')}
          {budgetLabel && budget > 0 ? ` · ${budgetLabel.label}` : ''}
        </div>
      )}
    </div>
  )
}