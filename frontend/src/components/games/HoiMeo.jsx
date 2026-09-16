import React, { useCallback, useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import RarityBadge from '../cards/RarityBadge'

const API = import.meta.env.VITE_API_BASE || ''

const RARITY_COLORS = {
  common: '#9d998d',
  rare: '#71a69a',
  epic: '#aa8cbb',
  legendary: '#d65b64',
  mythic: '#d65b64',
}

const CAT_POSITIONS = [
  { left: '18%', top: '62%' },
  { left: '40%', top: '57%' },
  { left: '50%', top: '53%' },
  { left: '62%', top: '52%' },
  { left: '83%', top: '60%' },
]

const VIDEO_URL = 'https://github.com/hieu20tuoi2404-eng/video/raw/main/cats-office-wide.mp4'

const fetchRandomDish = async () => {
  const res = await fetch(`${API}/api/dishes/random`)
  if (!res.ok) throw new Error('Lỗi API')
  return res.json()
}

const delay = (ms) => new Promise(r => setTimeout(r, ms))

export default function HoiMeo() {
  const [badges, setBadges] = useState(Array.from({ length: CAT_POSITIONS.length }, () => null))
  const [phase, setPhase] = useState('idle') // idle | spinning | revealed
  const [winnerIdx, setWinnerIdx] = useState(null)
  const [winnerDish, setWinnerDish] = useState(null)
  const [error, setError] = useState('')
  const [muted, setMuted] = useState(true)
  const audioRef = useRef({})
  const audioCtxRef = useRef(null)
  const mountedRef = useRef(true)

  const unlockAudio = useCallback(() => {
    try {
      if (!audioCtxRef.current) audioCtxRef.current = new (window.AudioContext || window.webkitAudioContext)()
      if (audioCtxRef.current.state === 'suspended') audioCtxRef.current.resume()
    } catch {}
  }, [])

  useEffect(() => {
    mountedRef.current = true
    return () => { mountedRef.current = false }
  }, [])

  useEffect(() => {
    const sounds = {
      open: 'https://assets.mixkit.co/active_storage/sfx/2000/2000-preview.mp3',
      tick: 'https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3',
      reveal: 'https://assets.mixkit.co/active_storage/sfx/1434/1434-preview.mp3',
    }
    Object.entries(sounds).forEach(([key, url]) => {
      const a = new Audio(url); a.preload = 'auto'; audioRef.current[key] = a
    })
  }, [])

  // Load one random dish per cat position
  useEffect(() => {
    let cancelled = false
    const load = async () => {
      try {
        const results = await Promise.all(CAT_POSITIONS.map(() => fetchRandomDish()))
        if (!cancelled) setBadges(results)
      } catch {
        setError('Không lấy được món — kiểm tra kết nối')
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  const play = useCallback((key, vol = 0.5) => {
    if (muted) return
    const a = audioRef.current[key]
    if (a) { a.currentTime = 0; a.volume = vol; a.play().catch(() => {}) }
  }, [muted])

  const kick = useCallback(async () => {
    if (phase !== 'idle') return
    unlockAudio()
    setPhase('spinning')
    setWinnerIdx(null)
    setWinnerDish(null)
    setError('')
    play('open', 0.7)

    try {
      const winner = await fetchRandomDish()
      await delay(950)
      if (!mountedRef.current) return
      play('tick', 0.3)
      const idx = Math.floor(Math.random() * CAT_POSITIONS.length)
      setWinnerIdx(idx)
      setWinnerDish(winner)
      setBadges(prev => {
        const next = [...prev]
        next[idx] = winner
        return next
      })
      await delay(350)
      play('reveal', 0.8)
      setPhase('revealed')
    } catch (e) {
      if (!mountedRef.current) return
      setError(e.message || 'Không lấy được món')
      setPhase('idle')
    }
  }, [phase, unlockAudio, play])

  const reset = useCallback(async () => {
    setPhase('idle')
    setWinnerIdx(null)
    setWinnerDish(null)
    setError('')
    try {
      const results = await Promise.all(CAT_POSITIONS.map(() => fetchRandomDish()))
      if (mountedRef.current) setBadges(results)
    } catch {}
  }, [])

  const reducedMotion = typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches

  return (
    <div className={`cat-stage ${phase === 'revealed' ? 'showing-results results-entering' : ''}`}>
      {!reducedMotion && (
        <div className="cat-video-wrap">
          <video src={VIDEO_URL} autoPlay loop muted={muted} playsInline poster="/images/fallback.svg" />
          {CAT_POSITIONS.map((pos, i) => {
            const dish = badges[i]
            const isLocked = phase === 'revealed' && winnerIdx === i
            const obscured = phase !== 'idle' && !isLocked
            const tierColor = isLocked && winnerDish?.rarity?.key
              ? RARITY_COLORS[winnerDish.rarity.key] || winnerDish.rarity.color
              : (dish?.rarity?.key ? RARITY_COLORS[dish.rarity.key] || dish.rarity.color : '#cbd7b7')
            return (
              <div
                key={i}
                className={`cat-badge ${isLocked ? 'locked' : ''} ${obscured ? 'obscured' : ''} ${dish ? 'ready' : 'waiting'}`}
                style={{ left: pos.left, top: pos.top, '--cat-tier-color': tierColor }}
              >
                {isLocked && (<><div className="cat-lock-ring" /><div className="cat-lock-sparks" /></>)}
                <div className="cat-badge-content">
                  {dish ? (
                    <img src={dish.image_url || '/images/fallback.svg'} alt={dish.name} className="food-image" onError={e => { e.target.src = '/images/fallback.svg' }} />
                  ) : (
                    <span className="cat-question">?</span>
                  )}
                </div>
                {isLocked && dish && <span className="cat-badge-name">{dish.name}</span>}
              </div>
            )
          })}
          <button className="cat-mute" onClick={() => setMuted(m => !m)} type="button">
            {muted ? '🔇 Tắt' : '🔊 Bật'}
          </button>
        </div>
      )}

      {reducedMotion && (
        <div className="cat-motion-note">
          <p className="cat-question">Mỗi em mèo có một món ngon trên đầu!</p>
        </div>
      )}

      {/* Spin action */}
      {phase !== 'revealed' && (
        <div className="cat-kick-wrap">
          <button className="cat-kick" onClick={kick} disabled={phase !== 'idle'} type="button" aria-busy={phase === 'spinning'}>
            {phase === 'spinning' ? 'ĐANG QUAY...' : 'KICK NGAY ↗'}
          </button>
        </div>
      )}

      {error && <div className="cat-status cat-error">{error}</div>}
      {phase === 'spinning' && <div className="cat-status">Đang chọn món...</div>}
      {phase === 'idle' && <div className="cat-status">Bấm Kick để quay món trưa nay!</div>}

      {phase === 'revealed' && winnerDish && (
        <div className="cat-results">
          <div className="cat-results-heading">
            <span>🐱 HỘI MÈO</span>
            <h2>Em mèo này chốt cho bạn món!</h2>
            <p>Món {winnerDish.name} xuất hiện trên đầu một em mèo 🎉</p>
          </div>
          <div className="cat-result-list">
            <div className="cat-result-card cat-card-enter is-selected" style={{ '--cat-tier-color': RARITY_COLORS[winnerDish.rarity?.key] || '#cbd7b7' }}>
              <div className="cat-result-art">
                <img src={winnerDish.image_url || '/images/fallback.svg'} alt={winnerDish.name} className="food-image" onError={e => { e.target.src = '/images/fallback.svg' }} />
              </div>
              <div className="cat-result-copy">
                <small>{winnerDish.category || 'Món ngon'}</small>
                <strong>{winnerDish.name}</strong>
                <div className="cat-price">{winnerDish.avg_price?.toLocaleString('vi-VN')}đ</div>
                <div className="cat-tier-tag">{winnerDish.rarity?.name || 'Món ngon'}</div>
              </div>
              <span className="cat-select-label">chốt ✓</span>
            </div>
          </div>
          <div className="cat-result-detail">
            <div className="cat-result-detail-head"><RarityBadge rarity={winnerDish.rarity} /></div>
            <p className="cat-result-detail-desc">{winnerDish.description}</p>
            <div className="cat-actions">
              <Link to={`/dish/${winnerDish.slug}`} className="cat-action-link">Xem chi tiết + quán + công thức →</Link>
              <button className="cat-back" onClick={reset} type="button">← Quay lại chọn món khác</button>
            </div>
          </div>
        </div>
      )}

      <div className="cat-audio-credit">
        Âm thanh từ <a href="https://github.com/sourcesounds/csgo" target="_blank" rel="noreferrer">SourceSounds</a>
      </div>
    </div>
  )
}