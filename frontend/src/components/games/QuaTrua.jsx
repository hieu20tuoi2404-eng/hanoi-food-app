import React, { useState, useEffect, useRef, useCallback } from 'react'
import { Link } from 'react-router-dom'
import RarityBadge from '../cards/RarityBadge'
import { useApp } from '../../context/AppContext'
import { resolveHexagram, TRI_EMOJI } from '../../data/kinhdich'

const API = import.meta.env.VITE_API_BASE || ''

const KINDS = [
  { id: '', label: 'Bất kỳ', emoji: '🎲' },
  { id: 'breakfast', label: 'Bữa sáng', emoji: '☀️' },
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

function shuffle(arr) {
  const a = arr.slice()
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

function normalizeVn(str) {
  return (str || '').toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/đ/g, 'd')
    .trim()
}

// Tên món trong lời gợi ý của quẻ (phần trước dấu gạch ngang)
function foodKeyword(food) {
  return normalizeVn((food || '').split(/[—–]/)[0])
}

const COIN_INTERVAL = 700
const LINE_DRAW_MS = 300

function Coin({ face, animating }) {
  const cls = `qd-coin ${face === 'duong' ? 'qd-coin-yang' : 'qd-coin-yin'} ${animating ? 'qd-coin-anim' : ''}`
  return (
    <div className={cls}>
      <span className="qd-coin-face">{face === 'duong' ? '☰' : '☷'}</span>
      <span className="qd-coin-label">{face === 'duong' ? 'DƯƠNG' : 'ÂM'}</span>
    </div>
  )
}

function HexLine({ yang, moving, index, revealed }) {
  if (!revealed) return <div className="qd-line qd-line-hidden"><span className="qd-line-num">{index + 1}</span></div>
  if (yang) {
    return (
      <div className={`qd-line qd-line-solid ${moving ? 'qd-line-moving' : ''}`}>
        <span className="qd-line-num">{index + 1}</span>
        {moving && <span className="qd-dot">•</span>}
      </div>
    )
  }
  return (
    <div className={`qd-line qd-line-broken ${moving ? 'qd-line-moving' : ''}`}>
      <span className="qd-line-num">{index + 1}</span>
      <span className="qd-gap" />
      {moving && <span className="qd-dot">•</span>}
    </div>
  )
}

export default function QuaTrua() {
  const { mascot } = useApp()
  const [pool, setPool] = useState([])
  const [kind, setKind] = useState('')
  const [budget, setBudget] = useState(0)

  const [phase, setPhase] = useState('idle')
  const [lines, setLines] = useState([])
  const [currentToss, setCurrentToss] = useState(null)
  const [tossIndex, setTossIndex] = useState(-1)
  const [tosses, setTosses] = useState([])
  const [hex, setHex] = useState(null)
  const [dish, setDish] = useState(null)
  const [error, setError] = useState('')

  const timerRef = useRef(null)

  useEffect(() => {
    let cancelled = false
    fetch(`${API}/api/dishes`).then(r => r.json()).then(list => {
      if (!cancelled) setPool(list)
    }).catch(() => {})
    return () => { cancelled = true; clearTimeout(timerRef.current) }
  }, [])

  const reset = useCallback(() => {
    setLines([])
    setCurrentToss(null)
    setTossIndex(-1)
    setTosses([])
    setHex(null)
    setDish(null)
    setError('')
  }, [])

  const startCast = useCallback(async () => {
    if (phase === 'tossing' || phase === 'revealing') return
    reset()
    setPhase('tossing')

    try {
      const allTosses = []
      const allLines = []

      for (let i = 0; i < 6; i++) {
        const result = new Promise(resolve => {
          const r = castSingleToss()
          setCurrentToss(r)
          timerRef.current = setTimeout(() => {
            resolve(r)
          }, COIN_INTERVAL + LINE_DRAW_MS)
        })
        const toss = await result
        allTosses.push(toss)
        allLines.push(toss.yang ? 1 : 0)
        setTosses([...allTosses])
        setLines([...allLines])
        setTossIndex(i)
        setCurrentToss(null)
        await new Promise(r => setTimeout(r, 100))
      }

      const hexResult = resolveHexagram(allLines)
      setHex(hexResult)

      let fpool = pool
      if (kind) fpool = fpool.filter(d => d.meal_type === kind)
      if (budget > 0) fpool = fpool.filter(d => d.avg_price > 0 && d.avg_price <= budget)
      if (!fpool.length) fpool = pool

      // Ưu tiên chọn món khớp với gợi ý của quẻ (hex.food)
      const kw = foodKeyword(hexResult.food)
      const matching = kw ? fpool.filter(d => normalizeVn(d.name).includes(kw)) : []
      const chosenPool = matching.length ? matching : fpool
      const chosen = chosenPool[Math.floor(Math.random() * chosenPool.length)]
      setDish(chosen)

      setPhase('done')
    } catch (e) {
      setPhase('idle')
      setError(e.message)
    }
  }, [phase, pool, kind, budget, reset])

  return (
    <div className="quatrua">
      <div className="quatrua-head">
        <h2 className="quatrua-title"><span className="loot-icon">☯️</span> Gieo Quẻ Kinh Dịch</h2>
        <p className="quatrua-sub">Gieo 3 đồng xu 6 lần · Lấy hào trên dưới · Xem quẻ 64 hexagram</p>
      </div>

      <div className="qd-board">
        <div className="qd-coins-row">
          <Coin face={currentToss?.coins?.[0] ? 'duong' : 'yin'} animating={!!currentToss} />
          <Coin face={currentToss?.coins?.[1] ? 'duong' : 'yin'} animating={!!currentToss} />
          <Coin face={currentToss?.coins?.[2] ? 'duong' : 'yin'} animating={!!currentToss} />
        </div>

        {currentToss && (
          <div className="qd-toss-info">
            Lần {tossIndex + 2}/6 · Tổng: <b>{currentToss.sum}</b> · {currentToss.label}
          </div>
        )}

        <div className="qd-hexagram">
          {[0,1,2,3,4,5].map(i => (
            <HexLine
              key={i}
              yang={lines[i] === 1}
              moving={tosses[i]?.moving}
              index={i}
              revealed={i < lines.length}
            />
          ))}
        </div>

        {tossIndex >= 0 && !currentToss && phase === 'tossing' && (
          <div className="qd-toss-hint">Đang gieo lần {tossIndex + 2}/6...</div>
        )}
      </div>

      <div className="reel-options">
        <div className="reel-option-row">
          <span className="reel-opt-label">Bữa</span>
          <div className="reel-chips">
            {KINDS.map(k => (
              <button key={k.id || 'any'} type="button" className={`reel-chip ${kind === k.id ? 'active' : ''}`} onClick={() => setKind(k.id)}>
                <span className="reel-chip-emoji">{k.emoji}</span> {k.label}
              </button>
            ))}
          </div>
        </div>
        <div className="reel-option-row">
          <span className="reel-opt-label">Ngân sách</span>
          <div className="reel-chips">
            {BUDGETS.map(b => (
              <button key={b.value} type="button" className={`reel-chip ${budget === b.value ? 'active' : ''}`} onClick={() => setBudget(b.value)}>
                <span className="reel-chip-emoji">{b.emoji}</span> {b.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <button className="reel-spin" onClick={startCast} disabled={phase === 'tossing' || phase === 'revealing'} type="button">
        {phase === 'tossing' ? 'Đang gieo...' : phase === 'done' ? 'GIEO LẠI ☯️' : '☯️ GIEO QUẺ'}
      </button>

      {error && <div className="lootbox-error">{error}</div>}

      {hex && phase === 'done' && (
        <div className="qd-result">
          <div className="qd-result-hex">
            <div className="qd-hexagram qd-hexagram-static">
              {[0,1,2,3,4,5].map(i => (
                <HexLine key={i} yang={lines[i] === 1} moving={tosses[i]?.moving} index={i} revealed />
              ))}
            </div>
            <div className="qd-result-info">
              <span className="qd-result-num">Quẻ {hex.n}</span>
              <span className="qd-result-name">{hex.ten}</span>
              <span className="qd-result-han">{hex.han}</span>
              <div className="qd-result-trigram">
                <span>{TRI_EMOJI[hex.lower] || '?'} Hạ: {hex.lower}</span>
                <span>{TRI_EMOJI[hex.upper] || '?'} Thượng: {hex.upper}</span>
              </div>
              <p className="qd-result-y">{hex.y}</p>
              <div className="qd-domains">
                <div className="qd-domain"><span className="qd-domain-icon">💼</span><span className="qd-domain-label">Công việc</span><span className="qd-domain-text">{hex.cv}</span></div>
                <div className="qd-domain"><span className="qd-domain-icon">❤️</span><span className="qd-domain-label">Tình duyên</span><span className="qd-domain-text">{hex.td}</span></div>
                <div className="qd-domain"><span className="qd-domain-icon">🩺</span><span className="qd-domain-label">Sức khỏe</span><span className="qd-domain-text">{hex.sk}</span></div>
                <div className="qd-domain"><span className="qd-domain-icon">💰</span><span className="qd-domain-label">Tài lộc</span><span className="qd-domain-text">{hex.tl}</span></div>
              </div>
            </div>
          </div>

          {dish && (
            <div className="qd-dish">
              <div className="qd-dish-head">
                <span className="lootbox-result-label">GỢI Ý MÓN ĂN</span>
                <RarityBadge rarity={dish.rarity} />
              </div>
              <div className="lootbox-result-main">
                <img
                  src={dish.image_url || '/images/fallback.svg'}
                  alt={dish.name}
                  className="lootbox-result-img"
                  onError={e => { e.target.src = '/images/fallback.svg' }}
                />
                <div className="lootbox-result-info">
                  <div className="lootbox-result-name">{dish.name}</div>
                  <div className="lootbox-result-meta">
                    <span className="dish-card-rating">★ {dish.avg_rating.toFixed(1)}/10</span>
                    <span className="dish-card-price">{dish.avg_price > 0 ? `${dish.avg_price.toLocaleString('vi-VN')}đ` : 'Giá: chưa rõ'}</span>
                  </div>
                  <p className="lootbox-result-desc">{dish.description}</p>
                  <Link to={`/dish/${dish.slug}`} className="lootbox-result-link">Xem chi tiết + quán + công thức →</Link>
                </div>
              </div>
              <p className="quatrua-mascot">
                {normalizeVn(dish.name).includes(foodKeyword(hex.food))
                  ? mascot
                    ? `${mascot.emoji} Gợi ý vui từ linh vật ${mascot.name}: ${hex.food}`
                    : `☯️ ${hex.food}`
                  : mascot
                    ? `${mascot.emoji} Gợi ý vui từ linh vật ${mascot.name}: ${dish.description}`
                    : `☯️ ${dish.description}`}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function castSingleToss() {
  const coins = [0,0,0].map(() => Math.random() < 0.5 ? 0 : 1)
  const sum = coins.reduce((a, b) => a + b + 2, 0)
  return {
    coins,
    sum,
    yang: sum % 2 === 1,
    moving: sum === 6 || sum === 9,
    label: sum === 6 ? 'Lão Âm' : sum === 7 ? 'Thiếu Dương' : sum === 8 ? 'Thiếu Âm' : 'Lão Dương',
  }
}

