import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import RarityBadge from '../cards/RarityBadge'

const API = import.meta.env.VITE_API_BASE || ''

const CATS = [
  { id: 'meo-an-sang', name: 'Mèo Sáng', emoji: '🐱', meal: 'breakfast', desc: 'Mèo dậy sớm, hay đi kiếm bữa sáng', color: '#fbbf24' },
  { id: 'meo-trua', name: 'Mèo Trưa', emoji: '😺', meal: 'lunch', desc: 'Mèo lười, chỉ ăn trưa no nê', color: '#fb923c' },
  { id: 'meo-toi', name: 'Mèo Tối', emoji: '🐱‍👤', meal: 'dinner', desc: 'Mèo đêm, thích ăn tối lãng mạn', color: '#8b5cf6' },
  { id: 'meo-an-vat', name: 'Mèo Vặt', emoji: '😸', meal: 'snack', desc: 'Mèo hay kêu, đòi ăn vặt suốt ngày', color: '#ec4899' },
  { id: 'meo-nhau', name: 'Mèo Nhậu', emoji: '😾', meal: 'drinking', desc: 'Mèo già, chỉ nhậu nhẹt với bạn', color: '#ef4444' },
]

const VIDEO_URL = 'https://github.com/hieu20tuoi2404-eng/video/raw/main/cats-office-wide.mp4'

const DISH_POOL = [
  { name: 'Phở bò Hà Nội', image: '/images/fallback.svg', price: 55000, rating: 9.2 },
  { name: 'Bún chả', image: '/images/fallback.svg', price: 45000, rating: 9.0 },
  { name: 'Bánh cuốn', image: '/images/fallback.svg', price: 35000, rating: 8.8 },
  { name: 'Xôi xéo', image: '/images/fallback.svg', price: 25000, rating: 8.5 },
  { name: 'Bánh mì patê', image: '/images/fallback.svg', price: 20000, rating: 8.2 },
  { name: 'Phở gà', image: '/images/fallback.svg', price: 50000, rating: 8.9 },
  { name: 'Cháo sườn', image: '/images/fallback.svg', price: 30000, rating: 8.3 },
  { name: 'Bánh bao', image: '/images/fallback.svg', price: 15000, rating: 7.8 },
  { name: 'Mì vằn thắn', image: '/images/fallback.svg', price: 40000, rating: 8.4 },
  { name: 'Cốm làng Vòng', image: '/images/fallback.svg', price: 60000, rating: 8.7 },
  { name: 'Bún bò Nam Bộ', image: '/images/fallback.svg', price: 55000, rating: 9.1 },
  { name: 'Cơm tấm sườn nướng', image: '/images/fallback.svg', price: 65000, rating: 9.3 },
]

function useSound() {
  const audioRef = useRef({})

  const load = useCallback((key, url) => {
    if (!audioRef.current[key]) {
      const a = new Audio(url)
      a.preload = 'auto'
      audioRef.current[key] = a
    }
    return audioRef.current[key]
  }, [])

  const play = useCallback((key, options = {}) => {
    const audio = audioRef.current[key]
    if (audio) {
      audio.currentTime = 0
      audio.volume = options.volume ?? 0.5
      audio.play().catch(() => {})
    }
  }, [])

  return { load, play }
}

function Confetti({ count = 60, colors = ['#fde047', '#f8b500', '#fff', '#fbbf24', '#fb923c', '#8b5cf6', '#ec4899'] }) {
  const [particles, setParticles] = useState([])

  useEffect(() => {
    const newParticles = Array.from({ length: count }, (_, i) => ({
      id: i,
      x: Math.random() * 100,
      y: -10 - Math.random() * 20,
      size: 6 + Math.random() * 10,
      color: colors[Math.floor(Math.random() * colors.length)],
      rotation: Math.random() * 360,
      rotationSpeed: (Math.random() - 0.5) * 12,
      fallSpeed: 2 + Math.random() * 4,
      sway: (Math.random() - 0.5) * 1.5,
      opacity: 1,
      delay: Math.random() * 300,
    }))
    setParticles(newParticles)

    const animate = () => {
      setParticles(prev => prev.map(p => {
        if (p.delay > 0) return { ...p, delay: p.delay - 16 }
        const nextY = p.y + p.fallSpeed
        const nextX = p.x + p.sway
        const nextRotation = p.rotation + p.rotationSpeed
        const nextOpacity = nextY > 110 ? Math.max(0, p.opacity - 0.02) : p.opacity
        return { ...p, x: nextX, y: nextY, rotation: nextRotation, opacity: nextOpacity }
      }))
      if (particles.some(p => p.opacity > 0 && p.y < 120)) {
        requestAnimationFrame(animate)
      }
    }
    requestAnimationFrame(animate)

    const timer = setTimeout(() => setParticles([]), 4000)
    return () => clearTimeout(timer)
  }, [count, colors])

  return (
    <div className="hoi-meo-confetti" aria-hidden="true">
      {particles.map(p => (
        <div
          key={p.id}
          className="hoi-meo-confetti-piece"
          style={{
            left: `${p.x}%`,
            top: `${p.y}%`,
            width: `${p.size}px`,
            height: `${p.size}px`,
            background: p.color,
            transform: `rotate(${p.rotation}deg)`,
            opacity: p.opacity,
            transitionDelay: `${p.delay}ms`,
          }}
        />
      ))}
    </div>
  )
}

const SPIN_DURATION = 2500
const REEL_ITEMS = 20

export default function HoiMeo() {
  const [selected, setSelected] = useState(null)
  const [spinning, setSpinning] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [rollHistory, setRollHistory] = useState([])
  const [showConfetti, setShowConfetti] = useState(false)

  const reelRef = useRef(null)
  const spinStartRef = useRef(0)
  const animationRef = useRef(null)
  const { load, play } = useSound()

  useEffect(() => {
    load('spin', 'https://assets.mixkit.co/active_storage/sfx/2000/2000-preview.mp3')
    load('win', 'https://assets.mixkit.co/active_storage/sfx/1434/1434-preview.mp3')
    load('click', 'https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3')
  }, [load])

  const generateReelItems = useCallback(() => {
    const items = []
    for (let i = 0; i < REEL_ITEMS; i++) {
      const dish = DISH_POOL[Math.floor(Math.random() * DISH_POOL.length)]
      items.push({ ...dish, id: `${dish.name}-${i}-${Date.now()}` })
    }
    return items
  }, [])

  const [reelItems, setReelItems] = useState(generateReelItems)

  const spinReel = useCallback((finalDish) => {
    const newItems = generateReelItems()
    const finalItem = { ...finalDish, id: `final-${Date.now()}` }
    newItems[REEL_ITEMS - 3] = finalItem
    setReelItems(newItems)
    setSpinning(true)
    spinStartRef.current = performance.now()
    play('spin', { volume: 0.4 })

    if (animationRef.current) cancelAnimationFrame(animationRef.current)

    const animate = (now) => {
      const elapsed = now - spinStartRef.current
      const progress = Math.min(elapsed / SPIN_DURATION, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      const translateY = eased * (REEL_ITEMS - 3) * 100

      if (reelRef.current) {
        reelRef.current.style.transform = `translateY(-${translateY}%)`
      }

      if (progress < 1) {
        animationRef.current = requestAnimationFrame(animate)
      } else {
        setSpinning(false)
        play('win', { volume: 0.6 })
        setShowConfetti(true)
        setTimeout(() => setShowConfetti(false), 3500)
      }
    }
    animationRef.current = requestAnimationFrame(animate)
  }, [generateReelItems, play])

  const roll = useCallback(async (cat) => {
    setSelected(cat)
    setResult(null)
    setError('')
    play('click', { volume: 0.3 })

    try {
      const p = new URLSearchParams({ meal: cat.meal })
      const res = await fetch(`${API}/api/dishes/random?${p}`)
      if (!res.ok) throw new Error('Không lấy được món')
      const data = await res.json()
      spinReel(data)
      setRollHistory((h) => [data, ...h].slice(0, 5))
    } catch (e) {
      setError(e.message)
      setSpinning(false)
    }
  }, [spinReel, play])

  const reset = useCallback(() => {
    setSelected(null)
    setResult(null)
    setError('')
    setReelItems(generateReelItems())
  }, [generateReelItems])

  return (
    <div className="hoi-meo">
      {/* Video background */}
      <div className="hoi-meo-video-wrap" aria-hidden="true">
        <video
          className="hoi-meo-video"
          src={VIDEO_URL}
          autoPlay
          loop
          muted
          playsInline
          poster="/images/fallback.svg"
        />
        <div className="hoi-meo-video-overlay" />
      </div>

      <div className="hoi-meo-content">
        <div className="hoi-meo-head">
          <div className="hoi-meo-tag">HỘI MÈO · THÚ CƯNG HÀ NỘI</div>
          <h2 className="hoi-meo-title">Hội Mèo Hà Nội</h2>
          <p className="hoi-meo-sub">Chọn một em mèo để nó gợi ý bữa ăn cho bạn!</p>
        </div>

        <div className="hoi-meo-grid">
          {CATS.map((cat) => (
            <button
              key={cat.id}
              className={`hoi-meo-card ${selected?.id === cat.id ? 'selected' : ''} ${spinning ? 'disabled' : ''}`}
              onClick={() => !spinning && roll(cat)}
              disabled={spinning}
              style={{ '--cat-color': cat.color }}
              type="button"
            >
              <span className="hoi-meo-emoji">{cat.emoji}</span>
              <strong>{cat.name}</strong>
              <span className="hoi-meo-desc">{cat.desc}</span>
            </button>
          ))}
        </div>

        {/* Reel */}
        <div className={`hoi-meo-reel-wrap ${spinning ? 'spinning' : ''}`}>
          <div className="hoi-meo-reel-mask">
            <div className="hoi-meo-reel-track" ref={reelRef}>
              {reelItems.map((item, idx) => (
                <div key={item.id} className="hoi-meo-reel-item">
                  <img src={item.image} alt={item.name} className="hoi-meo-reel-img" onError={e => e.target.src = '/images/fallback.svg'} />
                  <span className="hoi-meo-reel-name">{item.name}</span>
                  <span className="hoi-meo-reel-price">{item.price.toLocaleString('vi-VN')}đ</span>
                  <span className="hoi-meo-reel-rating">★ {item.rating.toFixed(1)}</span>
                </div>
              ))}
            </div>
            <div className="hoi-meo-reel-gradient-top" />
            <div className="hoi-meo-reel-gradient-bottom" />
            <div className="hoi-meo-reel-pointer" />
          </div>
          {spinning && <div className="hoi-meo-spin-label">Đang quay...</div>}
        </div>

        {error && <div className="hoi-meo-error">{error}</div>}

        {result && (
          <>
            <Confetti />
            <div className={`hoi-meo-result rarity-card-${result.rarity.key}`}>
              <div className="hoi-meo-result-top">
                <span className="hoi-meo-result-label">
                  {selected?.emoji} {selected?.name} gợi ý
                </span>
                <RarityBadge rarity={result.rarity} />
              </div>
              <div className="hoi-meo-result-main">
                <img
                  src={result.image_url || '/images/fallback.svg'}
                  alt={result.name}
                  className="hoi-meo-result-img"
                  onError={(e) => { e.target.src = '/images/fallback.svg' }}
                />
                <div className="hoi-meo-result-info">
                  <div className="hoi-meo-result-name">{result.name}</div>
                  <div className="hoi-meo-result-meta">
                    <span>&#9733; {result.avg_rating.toFixed(1)}/10</span>
                    <span>{result.avg_price.toLocaleString('vi-VN')}đ</span>
                  </div>
                  <p className="hoi-meo-result-desc">{result.description}</p>
                  <Link to={`/dish/${result.slug}`} className="hoi-meo-result-link">
                    Xem chi tiết + quán + công thức &#8594;
                  </Link>
                  {result.is_demo && <div className="dish-card-demo">Dữ liệu Demo — Chưa xác minh</div>}
                </div>
              </div>
              <button className="hoi-meo-again" onClick={reset} type="button">
                Chọn lại em khác &#8594;
              </button>
            </div>
          </>
        )}

        {rollHistory.length > 0 && !result && (
          <div className="hoi-meo-history">
            <h3>Lịch sử gợi ý</h3>
            <div className="hoi-meo-history-list">
              {rollHistory.map((d, i) => (
                <Link key={`${d.id}-${i}`} to={`/dish/${d.slug}`} className="hoi-meo-history-item">
                  <img src={d.image_url || '/images/fallback.svg'} alt={d.name} />
                  <span>{d.name}</span>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}