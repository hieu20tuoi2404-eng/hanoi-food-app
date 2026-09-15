import React, { useState, useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import RarityBadge from './RarityBadge'
import { useApp } from '../context/AppContext'

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

export default function FateDice() {
  const { mascot } = useApp()
  const [pool, setPool] = useState([])
  const [kind, setKind] = useState('')
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
      .then((list) => { if (!cancelled) setPool(list) })
      .catch(() => {})
    return () => { cancelled = true; clearTimeout(timerRef.current) }
  }, [])

  const spin = async (likely = false) => {
    if (phase === 'spinning') return
    setError('')
    setResult(null)
    setPhase('spinning')
    const sid = localStorage.getItem('angi_session_id') || ''
    try {
      const body = {}
      if (kind) body.meal = kind
      if (likely) body.likely = true
      const res = await fetch(`${API}/api/fate/roll`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Session-Id': sid },
        body: JSON.stringify(body),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Không xúc được')
      const winner = data.dish

      let fpool = pool
      if (kind) fpool = fpool.filter((d) => d.meal_type === kind)
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
        setResult(data)
      }, SPIN_MS)
    } catch (e) {
      setPhase('idle')
      setError(e.message)
    }
  }

  const mascotLabel = (mv) => {
    if (!mv) return null
    return `${mv.emoji || ''} ${mv.name || mv.label || ''}${mv.animal ? ` (${mv.animal})` : ''}`.trim()
  }

  return (
    <div className="widget fate-widget">
      <div className="fate-banner">
        <span className="fate-banner-tag">HỘI THỢ LÙN · VẠN SỰ TÙY DUYÊN</span>
        <h2 className="fate-banner-title">Vạn sự tùy duyên</h2>
        <p className="fate-banner-sub">Một lượt xúc. Để duyên dẫn đường.</p>
      </div>

      <div className="reel-window" ref={winRef}>
        <div className="reel-selector" />
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
      </div>

      <button className="reel-spin" onClick={() => spin(false)} disabled={phase === 'spinning'} type="button">
        {phase === 'spinning' ? 'Đang xúc...' : '🎲 KHAI MỞ DUYÊN'}
      </button>
      <button className="fate-btn-secondary" onClick={() => spin(true)} disabled={phase === 'spinning'} type="button">
        Nghiêng về món ngon hơn
      </button>

      {error && (
        <div className="lootbox-error fate-error-mascot">
          <span className="fate-error-mascot-emoji">{mascot ? mascot.emoji : '🍜'}</span>
          <span>
            {mascot
              ? `${mascot.name} nói: "${mascot.fallback_message}" ${error}`
              : error}
          </span>
        </div>
      )}

      {result && phase === 'idle' && (
        <div className={`fate-result rarity-card-${result.dish.rarity.key}`}>
          <div className="fate-roll-line">
            <span className="fate-dice">⚄</span>
            <span className="fate-roll-num">Ra mặt <b>{result.roll}</b></span>
            {result.linh_vat && <span className="fate-linh-vat">{mascotLabel(result.linh_vat)}</span>}
          </div>
          {result.linh_vat && result.message && <p className="fate-message">"{result.message}"</p>}

          {result.limit_reached && (
            <div className="fate-limit-card">
              <span className="fate-limit-emoji">{result.linh_vat ? result.linh_vat.emoji : '🎯'}</span>
              <p>Bạn đã quay 3 lần rồi. Hôm nay hãy thử món này nhé!</p>
              <p className="fate-limit-sub">
                Đây là gợi ý vui từ linh vật của bạn, bạn vẫn có thể chọn món khác.
              </p>
            </div>
          )}

          <div className="lootbox-result-main">
            <img
              src={result.dish.image_url || '/images/fallback.svg'}
              alt={result.dish.name}
              className="lootbox-result-img"
              onError={(e) => { e.target.src = '/images/fallback.svg' }}
            />
            <div className="lootbox-result-info">
              <div className="lootbox-result-top" style={{ marginBottom: 6 }}>
                <span className="lootbox-result-label">QUẺ CỦA BẠN</span>
                <RarityBadge rarity={result.dish.rarity} />
              </div>
              <div className="lootbox-result-name">{result.dish.name}</div>
              <div className="lootbox-result-meta">
                <span className="dish-card-rating">&#9733; {result.dish.avg_rating.toFixed(1)}/10</span>
                <span className="dish-card-price">
                  {result.dish.avg_price > 0 ? `${result.dish.avg_price.toLocaleString('vi-VN')}đ` : 'Giá: chưa rõ'}
                </span>
              </div>
              <div className="fate-actions">
                <Link to={`/dish/${result.dish.slug}`} className="lootbox-result-link">
                  Chọn món này &#8594;
                </Link>
                <button
                  type="button"
                  className="fate-btn-soft"
                  onClick={() => { setPhase('idle'); setResult(null) }}
                >
                  Quay lại
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {phase === 'spinning' && (
        <div className="reel-spinning-hint">
          {KINDS.find((k) => k.id === kind)
            ? `${KINDS.find((k) => k.id === kind).emoji} ${KINDS.find((k) => k.id === kind).label}`
            : '🎲 Bất kỳ'}
        </div>
      )}
    </div>
  )
}