import React, { useCallback, useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { CAT_PATHS, PATH_FPS, PATH_NFRAMES } from './catPaths'

const CAT_NAMES = ['Mèo kem', 'Mặt tròn', 'Đốm đen']

const API = import.meta.env.VITE_API_BASE || ''

const RARITY_COLORS = {
  common: '#9d998d',
  rare: '#71a69a',
  epic: '#aa8cbb',
  legendary: '#d65b64',
  mythic: '#d65b64',
}

const VIDEO_URL = 'https://github.com/hieu20tuoi2404-eng/video/raw/main/cats-office-wide.mp4'

const fetchRandomDish = async () => {
  const res = await fetch(`${API}/api/dishes/random`)
  if (!res.ok) throw new Error('Lỗi API')
  return res.json()
}

const delay = (ms) => new Promise(r => setTimeout(r, ms)) // eslint-disable-line no-unused-vars

export default function HoiMeo() {
  const [badges, setBadges] = useState(Array.from({ length: CAT_PATHS.length }, () => null))
  const [phase, setPhase] = useState('idle') // idle | rolling | stopping | revealed
  const [locked, setLocked] = useState(Array.from({ length: CAT_PATHS.length }, () => false))
  const [error, setError] = useState('')
  const [muted, setMuted] = useState(true)
  const videoRef = useRef(null)
  const badgeRefs = useRef([])
  const audioRef = useRef({})
  const audioCtxRef = useRef(null)
  const mountedRef = useRef(true)
  const lockedRef = useRef(Array.from({ length: CAT_PATHS.length }, () => false))
  const lockedDishesRef = useRef([])
  const warmPoolRef = useRef([])
  const timersRef = useRef([])
  const stopHandledRef = useRef(false)
  const phaseRef = useRef(phase)
  phaseRef.current = phase

  const debug = typeof window !== 'undefined' && new URLSearchParams(window.location.search).get('debug') === '1'
  const debugRef = useRef(null)

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

  // Warm a pool of random dishes on mount so "roll" starts instantly on click
  useEffect(() => {
    let on = true
    const warm = async () => {
      try {
        const p = (await Promise.all(Array.from({ length: 10 }, () => fetchRandomDish()))).filter(Boolean)
        if (on && p.length) warmPoolRef.current = p
      } catch {}
    }
    warm()
    return () => { on = false }
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

  // Clear any pending roll timers
  const clearTimers = useCallback(() => {
    timersRef.current.forEach(t => { clearTimeout(t); clearInterval(t) })
    timersRef.current = []
  }, [])

  useEffect(() => () => clearTimers(), [clearTimers])

  // Live reads so a cold-start refill still feeds the roll
  const pick = () => {
    const p = warmPoolRef.current
    return p.length ? p[Math.floor(Math.random() * p.length)] : null
  }
  const pickDistinct = () => {
    const p = warmPoolRef.current
    const taken = new Set(lockedDishesRef.current.map(d => d && d.id))
    const avail = p.filter(d => !taken.has(d.id))
    const src = avail.length ? avail : p
    return src.length ? src[Math.floor(Math.random() * src.length)] : null
  }

  // Cats stop (video ends) → burst effect → assign final dishes → reveal choices
  const handleStop = useCallback(() => {
    if (phaseRef.current !== 'rolling' || stopHandledRef.current) return
    stopHandledRef.current = true
    if (!mountedRef.current) return
    clearTimers()
    const final = []
    lockedDishesRef.current = []
    for (let i = 0; i < CAT_PATHS.length; i++) {
      const d = pickDistinct()
      final.push(d)
      if (d) lockedDishesRef.current.push(d)
    }
    lockedRef.current = Array.from({ length: CAT_PATHS.length }, () => true)
    setLocked(Array.from({ length: CAT_PATHS.length }, () => true))
    setBadges(final)
    setPhase('stopping')
    play('tick', 0.4)
    const id = window.setTimeout(() => {
      if (!mountedRef.current) return
      play('reveal', 0.8)
      setPhase('revealed')
    }, 850)
    timersRef.current.push(id)
  }, [play, clearTimers])

  // Time-synced follower: badges follow real-site cat paths with the video playhead
  useEffect(() => {
    let raf = 0
    const tick = () => {
      const video = videoRef.current
      if (video) {
        let t = video.currentTime
        if (!isFinite(t)) t = 0
        const fr = Math.max(0, Math.min(PATH_NFRAMES - 1, Math.round(t * PATH_FPS)))
        for (let k = 0; k < CAT_PATHS.length; k++) {
          const el = badgeRefs.current[k]
          if (!el) continue
          const p = CAT_PATHS[k][fr]
          el.style.left = `${p[0] * 100}%`
          el.style.top = `${p[1] * 100}%`
          if (phaseRef.current === 'idle') {
            if (p[2]) el.classList.add('obscured')
            else el.classList.remove('obscured')
          }
        }
        if (debugRef.current) {
          const parts = [
            `t=${t.toFixed(2)}s frame=${fr}/${PATH_NFRAMES} ready=${video.readyState} paused=${video.paused} net=${video.networkState}`,
            `W=${video.videoWidth}x${video.videoHeight}`,
          ]
          for (let k = 0; k < CAT_PATHS.length; k++) {
            const p = CAT_PATHS[k][fr]
            parts.push(`b${k}: ${(p[0] * 100).toFixed(1)}%,${(p[1] * 100).toFixed(1)}%${p[2] ? ' hidden' : ''}`)
          }
          debugRef.current.textContent = parts.join('  |  ')
        }
      }
      raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [])

  // Preload video data on mount (shows first frame, does NOT autoplay)
  useEffect(() => {
    const v = videoRef.current
    if (v) v.load()
  }, [])

  const kick = useCallback(async () => {
    if (phase !== 'idle') return
    unlockAudio()
    clearTimers()
    setError('')
    stopHandledRef.current = false
    setPhase('rolling')
    lockedRef.current = Array.from({ length: CAT_PATHS.length }, () => false)
    lockedDishesRef.current = []
    setLocked(Array.from({ length: CAT_PATHS.length }, () => false))
    play('open', 0.7)

    // Video starts running only now (cats jump)
    const v = videoRef.current
    if (v) {
      v.currentTime = 0
      v.play().catch(() => {})
    }

    // All badges keep rolling the whole time the cats are moving, stop only
    // when the video actually ends and the cats come to a halt
    const rollId = window.setInterval(() => {
      if (!mountedRef.current) return
      setBadges(prev => prev.map((d, i) => (lockedRef.current[i] ? d : pick() || d)))
    }, 280)
    timersRef.current.push(rollId)

    // Safety net: if 'ended' never fires (stall/server hiccup), force a stop
    const durMs = v && isFinite(v.duration) && v.duration > 0 ? v.duration * 1000 : 11800
    const safetyId = window.setTimeout(() => { handleStop() }, durMs + 300)
    timersRef.current.push(safetyId)

    // Cold-start: pool not warmed yet — refill so the live roll picks it up
    if (!warmPoolRef.current.length) {
      try {
        const fresh = (await Promise.all(Array.from({ length: 10 }, () => fetchRandomDish()))).filter(Boolean)
        if (fresh.length) warmPoolRef.current = fresh
      } catch {}
    }
  }, [phase, unlockAudio, play, clearTimers, handleStop])

  const reset = useCallback(() => {
    clearTimers()
    stopHandledRef.current = false
    const v = videoRef.current
    if (v) { try { v.pause(); v.currentTime = 0 } catch {} }
    lockedRef.current = Array.from({ length: CAT_PATHS.length }, () => false)
    setLocked(Array.from({ length: CAT_PATHS.length }, () => false))
    setBadges(Array.from({ length: CAT_PATHS.length }, () => null))
    setPhase('idle')
    setError('')
  }, [clearTimers])

  return (
    <div className={`cat-stage ${phase === 'rolling' ? 'rolling' : ''} ${phase === 'stopping' ? 'stopping' : ''} ${phase === 'revealed' ? 'showing-results results-entering' : ''}`}>
      <div className="cat-video-wrap">
        <video ref={videoRef} src={VIDEO_URL} muted={muted} playsInline preload="auto" poster="/images/fallback.svg" onEnded={handleStop} />
        {CAT_PATHS.map((_, i) => {
            const dish = badges[i]
            const isLocked = locked[i]
            const tierColor = dish?.rarity?.key
              ? RARITY_COLORS[dish.rarity.key] || dish.rarity.color
              : '#cbd7b7'
            return (
              <div
                key={i}
                ref={el => { badgeRefs.current[i] = el }}
                className={`cat-badge ${phase === 'rolling' ? 'rolling' : ''} ${phase === 'stopping' ? 'stopping' : ''} ${isLocked ? 'locked' : ''} ${dish ? 'ready' : 'waiting'}`}
                style={{ '--cat-tier-color': tierColor, '--bi': i }}
              >
                {isLocked && (<><div className="cat-lock-ring" /><div className="cat-lock-sparks" /></>)}
                <div className="cat-badge-content">
                  {dish ? (
                    <img key={dish.id} src={dish.image_url || '/images/fallback.svg'} alt={dish.name} className="food-image" onError={e => { e.target.src = '/images/fallback.svg' }} />
                  ) : (
                    <span className="cat-question">?</span>
                  )}
                </div>
                <span className="cat-badge-name">
                  {isLocked && dish
                    ? `${dish.name}${dish.rarity?.name ? ' · ' + dish.rarity.name : ''}`
                    : (dish && phase === 'rolling' ? dish.name : `🐱 ${CAT_NAMES[i]}`)}
                </span>
              </div>
            )
          })}
          <button className="cat-mute" onClick={() => setMuted(m => !m)} type="button">
            {muted ? '🔇 Tắt' : '🔊 Bật'}
          </button>
          {debug && <div ref={debugRef} className="cat-debug-hud" />}
      </div>

      {(phase === 'idle' || phase === 'rolling') && (
        <div className="cat-kick-wrap">
          <button className="cat-kick" onClick={kick} disabled={phase !== 'idle'} type="button" aria-busy={phase === 'rolling'}>
            {phase === 'rolling' ? 'ĐANG QUAY...' : 'NHỜ MÈO CHỌN MÓN ↗'}
          </button>
        </div>
      )}

      {error && <div className="cat-status cat-error">{error}</div>}
      {phase === 'rolling' && <div className="cat-status">🎰 Mèo đang chọn món...</div>}
      {phase === 'stopping' && <div className="cat-status">🐟 Mèo đã dừng — chốt món!</div>}
      {phase === 'idle' && <div className="cat-status">Bấm để nhờ mèo chọn món trưa nay!</div>}

      {phase === 'revealed' && (
        <div className="cat-results">
          <div className="cat-results-heading">
            <span>📋 BIÊN BẢN HỌP TRƯA</span>
            <h2>Mèo đề xuất. Bạn chốt.</h2>
            <p>3 em mèo mỗi em đề cử một món — chọn 1 để ăn trưa 🐟</p>
          </div>
          <div className="cat-result-list">
            {badges.map((dish, i) => dish && (
              <Link
                key={i}
                to={`/dish/${dish.slug}`}
                className="cat-result-card cat-card-enter"
                style={{ '--cat-tier-color': dish.rarity?.key ? RARITY_COLORS[dish.rarity.key] || dish.rarity.color : '#cbd7b7' }}
              >
                <div className="cat-result-art">
                  <img src={dish.image_url || '/images/fallback.svg'} alt={dish.name} className="food-image" onError={e => { e.target.src = '/images/fallback.svg' }} />
                </div>
                <div className="cat-result-copy">
                  <small>{CAT_NAMES[i]} đề cử</small>
                  <strong>{dish.name}</strong>
                  <div className="cat-price">{dish.avg_price?.toLocaleString('vi-VN')}đ</div>
                  <div className="cat-tier-tag">{dish.rarity?.name || 'Món ngon'}</div>
                </div>
                <span className="cat-select-label">Chọn ↗</span>
              </Link>
            ))}
          </div>
          <div className="cat-actions">
            <button className="cat-back" onClick={reset} type="button">⟲ Quay lại (nhờ mèo chọn lại)</button>
          </div>
        </div>
      )}

      <div className="cat-audio-credit">
        Âm thanh từ <a href="https://github.com/sourcesounds/csgo" target="_blank" rel="noreferrer">SourceSounds</a>
      </div>
    </div>
  )
}