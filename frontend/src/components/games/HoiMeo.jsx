import React, { useCallback, useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import RarityBadge from '../cards/RarityBadge'
import { CAT_PATHS, PATH_FPS, PATH_NFRAMES } from './catPaths'

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

const delay = (ms) => new Promise(r => setTimeout(r, ms))

export default function HoiMeo() {
  const [badges, setBadges] = useState(Array.from({ length: CAT_PATHS.length }, () => null))
  const [phase, setPhase] = useState('idle') // idle | spinning | revealed
  const [winnerIdx, setWinnerIdx] = useState(null)
  const [winnerDish, setWinnerDish] = useState(null)
  const [error, setError] = useState('')
  const [muted, setMuted] = useState(true)
  const videoRef = useRef(null)
  const badgeRefs = useRef([])
  const audioRef = useRef({})
  const audioCtxRef = useRef(null)
  const mountedRef = useRef(true)
  const phaseRef = useRef(phase)
  phaseRef.current = phase

  const reducedMotion = typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches

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

  // Load one random dish per badge (3 cats) — badges always visible on heads,
  // static until user clicks KICK (then random reels start)
  useEffect(() => {
    let cancelled = false
    const load = async () => {
      try {
        const results = await Promise.all(CAT_PATHS.map(() => fetchRandomDish()))
        if (!cancelled) setBadges(results)
      } catch {}
    }
    load()
    return () => { cancelled = true }
  }, [])

  // Fast reel roll while spinning: food images swap every 350ms
  useEffect(() => {
    if (phase !== 'spinning') return
    const roll = async () => {
      try {
        const results = await Promise.all(CAT_PATHS.map(() => fetchRandomDish()))
        if (mountedRef.current && phaseRef.current === 'spinning') setBadges(results)
      } catch {}
    }
    const id = window.setInterval(roll, 350)
    return () => clearInterval(id)
  }, [phase])

  // Time-synced follower: badges follow real-site cat paths with the video playhead
  useEffect(() => {
    if (reducedMotion) return
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
  }, [reducedMotion])

  // Preload video data on mount (shows first frame, does NOT autoplay)
  useEffect(() => {
    const v = videoRef.current
    if (v) v.load()
  }, [])

  const kick = useCallback(async () => {
    if (phase !== 'idle') return
    unlockAudio()
    setPhase('spinning')
    setWinnerIdx(null)
    setWinnerDish(null)
    setError('')
    play('open', 0.7)

    // Start video (cats run) + load 3 random dishes into badges immediately
    const v = videoRef.current
    if (v) {
      v.currentTime = 0
      v.play().catch(() => {})
    }
    try {
      const init = await Promise.all(CAT_PATHS.map(() => fetchRandomDish()))
      if (mountedRef.current) setBadges(init)
    } catch {}

    try {
      const winner = await fetchRandomDish()
      await delay(950)
      if (!mountedRef.current) return
      play('tick', 0.3)
      const idx = Math.floor(Math.random() * CAT_PATHS.length)
      setWinnerIdx(idx)
      setWinnerDish(winner)
      setBadges(prev => {
        const next = [...prev]
        next[idx] = winner
        return next
      })
      await delay(350)
      if (!mountedRef.current) return
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
      const results = await Promise.all(CAT_PATHS.map(() => fetchRandomDish()))
      if (mountedRef.current) setBadges(results)
    } catch {}
  }, [])

  return (
    <div className={`cat-stage ${phase === 'spinning' ? 'spinning' : ''} ${phase === 'revealed' ? 'showing-results results-entering' : ''}`}>
      {!reducedMotion && (
        <div className="cat-video-wrap">
          <video ref={videoRef} src={VIDEO_URL} loop muted={muted} playsInline poster="/images/fallback.svg" />
          {CAT_PATHS.map((_, i) => {
            const dish = badges[i]
            const isLocked = phase === 'revealed' && winnerIdx === i
            const obscured = phase !== 'idle' && !isLocked
            const tierColor = isLocked && winnerDish?.rarity?.key
              ? RARITY_COLORS[winnerDish.rarity.key] || winnerDish.rarity.color
              : (dish?.rarity?.key ? RARITY_COLORS[dish.rarity.key] || dish.rarity.color : '#cbd7b7')
            return (
              <div
                key={i}
                ref={el => { badgeRefs.current[i] = el }}
                className={`cat-badge ${isLocked ? 'locked' : ''} ${obscured ? 'obscured' : ''} ${dish ? 'ready' : 'waiting'}`}
                style={{ '--cat-tier-color': tierColor }}
              >
                {isLocked && (<><div className="cat-lock-ring" /><div className="cat-lock-sparks" /></>)}
                <div className="cat-badge-content">
                  {dish ? (
                    <img key={dish.id} src={dish.image_url || '/images/fallback.svg'} alt={dish.name} className="food-image" onError={e => { e.target.src = '/images/fallback.svg' }} />
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
          {debug && <div ref={debugRef} className="cat-debug-hud" />}
        </div>
      )}

      {reducedMotion && (
        <div className="cat-motion-note">
          <p className="cat-question">Mỗi em mèo có một món ngon trên đầu!</p>
        </div>
      )}

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
            <h2>Con mèo này chốt cho bạn món!</h2>
            <p>3 em mèo mỗi em chọn một món, em nào chốt trước là món trưa nay 🎉</p>
          </div>
          <div className="cat-result-list">
            {badges.map((dish, i) => dish && (
              <div
                key={i}
                className={`cat-result-card cat-card-enter ${i === winnerIdx ? 'is-selected' : 'not-selected'}`}
                style={{ '--cat-tier-color': dish.rarity?.key ? RARITY_COLORS[dish.rarity.key] || dish.rarity.color : '#cbd7b7' }}
              >
                <div className="cat-result-art">
                  <img src={dish.image_url || '/images/fallback.svg'} alt={dish.name} className="food-image" onError={e => { e.target.src = '/images/fallback.svg' }} />
                </div>
                <div className="cat-result-copy">
                  <small>{dish.category || 'Món ngon'}</small>
                  <strong>{dish.name}</strong>
                  <div className="cat-price">{dish.avg_price?.toLocaleString('vi-VN')}đ</div>
                  <div className="cat-tier-tag">{dish.rarity?.name || 'Món ngon'}</div>
                </div>
                <span className="cat-select-label">{i === winnerIdx ? 'chốt ✓' : '–'}</span>
              </div>
            ))}
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