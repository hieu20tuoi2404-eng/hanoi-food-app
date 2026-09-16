import React, { useCallback, useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import RarityBadge from '../cards/RarityBadge'

const API = import.meta.env.VITE_API_BASE || ''

const CATS = [
  { id: 'meo-an-sang', name: 'Mèo Sáng', emoji: '🐱', meal: 'breakfast', tierColor: '#fbbf24', left: '14%', top: '60%' },
  { id: 'meo-trua', name: 'Mèo Trưa', emoji: '😺', meal: 'lunch', tierColor: '#fb923c', left: '35%', top: '52%' },
  { id: 'meo-toi', name: 'Mèo Tối', emoji: '🐱‍👤', meal: 'dinner', tierColor: '#8b5cf6', left: '50%', top: '48%' },
  { id: 'meo-an-vat', name: 'Mèo Vặt', emoji: '😸', meal: 'snack', tierColor: '#ec4899', left: '65%', top: '52%' },
  { id: 'meo-nhau', name: 'Mèo Nhậu', emoji: '😾', meal: 'drinking', tierColor: '#ef4444', left: '86%', top: '60%' },
]

const VIDEO_URL = 'https://github.com/hieu20tuoi2404-eng/video/raw/main/cats-office-wide.mp4'

export default function HoiMeo() {
  const [phase, setPhase] = useState('idle')
  const [lockedCat, setLockedCat] = useState(null)
  const [dishes, setDishes] = useState([])
  const [selectedDish, setSelectedDish] = useState(null)
  const [error, setError] = useState('')
  const [muted, setMuted] = useState(true)
  const audioRef = useRef({})
  const audioCtxRef = useRef(null)

  const unlockAudio = useCallback(() => {
    try {
      if (!audioCtxRef.current) audioCtxRef.current = new (window.AudioContext || window.webkitAudioContext)()
      if (audioCtxRef.current.state === 'suspended') audioCtxRef.current.resume()
    } catch {}
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

  const play = useCallback((key, vol = 0.5) => {
    if (muted) return
    const a = audioRef.current[key]
    if (a) { a.currentTime = 0; a.volume = vol; a.play().catch(() => {}) }
  }, [muted])

  const pick = useCallback(async (cat) => {
    if (phase !== 'idle') return
    unlockAudio()
    setLockedCat(cat)
    setPhase('picking')
    setError('')
    play('open', 0.7)

    await new Promise(r => setTimeout(r, 900))
    setPhase('revealing')
    play('tick', 0.3)

    try {
      const results = await Promise.all(
        Array.from({ length: 3 }, () =>
          fetch(`${API}/api/dishes/random?meal=${cat.meal}`).then(r => { if (!r.ok) throw new Error('Lỗi API'); return r.json() })
        )
      )
      const seen = new Set()
      const unique = results.filter(d => { if (seen.has(d.id)) return false; seen.add(d.id); return true })
      await new Promise(r => setTimeout(r, 500))
      play('reveal', 0.8)
      setDishes(unique.length >= 2 ? unique : results)
      setPhase('results')
    } catch (e) {
      setError(e.message)
      setPhase('idle')
    }
  }, [phase, unlockAudio, play])

  const reset = useCallback(() => {
    setPhase('idle'); setLockedCat(null); setDishes([]); setSelectedDish(null); setError('')
  }, [])

  const reducedMotion = typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches

  return (
    <div className={`cat-stage ${phase === 'results' ? 'showing-results' : ''} ${phase === 'revealing' ? 'results-entering' : ''}`}>
      {!reducedMotion && (
        <div className="cat-video-wrap">
          <video src={VIDEO_URL} autoPlay loop muted={muted} playsInline poster="/images/fallback.svg" />
          {CATS.map(cat => (
            <div
              key={cat.id}
              className={`cat-badge ${lockedCat?.id === cat.id ? 'locked' : ''} ${lockedCat && lockedCat.id !== cat.id ? 'not-selected' : ''}`}
              style={{ left: cat.left, top: cat.top, '--cat-tier-color': cat.tierColor, pointerEvents: phase !== 'idle' ? 'none' : 'auto', cursor: phase === 'idle' ? 'pointer' : 'default' }}
              onClick={() => pick(cat)}
            >
              {lockedCat?.id === cat.id && (<><div className="cat-lock-ring" /><div className="cat-lock-sparks" /></>)}
              <div className="cat-badge-content">
                <span className="cat-question">{cat.emoji}</span>
              </div>
              <span className="cat-badge-name">{cat.name}</span>
            </div>
          ))}
          <button className="cat-mute" onClick={() => setMuted(m => !m)} type="button">
            {muted ? '🔇 Tắt tiếng' : '🔊 Có tiếng'}
          </button>
        </div>
      )}

      {reducedMotion && (
        <div className="cat-motion-note">
          <p className="cat-question">Chọn một em mèo!</p>
          <div className="cat-reduced-btns">
            {CATS.map(cat => (
              <button key={cat.id} className="cat-reduced-btn" onClick={() => pick(cat)} disabled={phase !== 'idle'} type="button" style={{ '--cat-tier-color': cat.tierColor }}>
                <span>{cat.emoji}</span><strong>{cat.name}</strong>
              </button>
            ))}
          </div>
        </div>
      )}

      {phase === 'picking' && <div className="cat-status">Đang chọn...</div>}
      {phase === 'revealing' && <div className="cat-status">Đang mở kho...</div>}
      {error && <div className="cat-status cat-error">{error}</div>}

      {phase === 'results' && (
        <div className="cat-results">
          <div className="cat-results-heading">
            <span>{lockedCat?.emoji} HỘI MÈO</span>
            <h2>{lockedCat?.name} gợi ý cho bạn</h2>
            <p>Chọn một món để xem chi tiết!</p>
          </div>
          <div className="cat-result-list">
            {dishes.map((dish, i) => (
              <div
                key={`${dish.id}-${i}`}
                className={`cat-result-card cat-card-enter ${selectedDish?.id === dish.id ? 'is-selected' : selectedDish ? 'not-selected' : ''}`}
                style={{ '--cat-tier-color': lockedCat?.tierColor, animationDelay: `${i * 120}ms` }}
                onClick={() => setSelectedDish(dish)}
              >
                <div className="cat-result-art">
                  <img src={dish.image_url || '/images/fallback.svg'} alt={dish.name} className="food-image" onError={e => { e.target.src = '/images/fallback.svg' }} />
                </div>
                <div className="cat-result-copy">
                  <small>{lockedCat?.name}</small>
                  <strong>{dish.name}</strong>
                  <div className="cat-price">{dish.avg_price?.toLocaleString('vi-VN')}đ</div>
                  <div className="cat-tier-tag">{dish.rarity?.name || 'Món ngon'}</div>
                </div>
                <span className="cat-select-label">chọn →</span>
              </div>
            ))}
          </div>

          {selectedDish && (
            <div className="cat-result-detail">
              <div className="cat-result-detail-head">
                <RarityBadge rarity={selectedDish.rarity} />
              </div>
              <p className="cat-result-detail-desc">{selectedDish.description}</p>
              <div className="cat-actions">
                <Link to={`/dish/${selectedDish.slug}`} className="cat-action-link">Xem chi tiết + quán + công thức →</Link>
                <button className="cat-back" onClick={reset} type="button">← Chọn lại con khác</button>
              </div>
            </div>
          )}
          {!selectedDish && (
            <button className="cat-back" onClick={reset} type="button">← Chọn lại con khác</button>
          )}
        </div>
      )}

      <div className="cat-audio-credit">
        Âm thanh từ <a href="https://github.com/sourcesounds/csgo" target="_blank" rel="noreferrer">SourceSounds</a>
      </div>
    </div>
  )
}
