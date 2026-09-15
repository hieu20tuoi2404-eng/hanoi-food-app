import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import RarityBadge from './RarityBadge'
import { useApp } from '../context/AppContext'

const API = import.meta.env.VITE_API_BASE || ''

export default function FateDice() {
  const { mascot } = useApp()
  const [state, setState] = useState('idle') // idle | rolling | result
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [elapsed, setElapsed] = useState(0)

  const roll = async (likely = false) => {
    setError('')
    setResult(null)
    setState('rolling')
    const sid = localStorage.getItem('angi_session_id') || ''
    const t0 = Date.now()
    try {
      const res = await fetch(`${API}/api/fate/roll`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Session-Id': sid },
        body: JSON.stringify({ likely }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Không xúc được')
      const wait = Math.max(0, 700 - (Date.now() - t0))
      await new Promise((r) => setTimeout(r, wait))
      setResult(data)
      setState('result')
    } catch (e) {
      setError(e.message)
      setState('idle')
    }
  }

  const mascotLabel = (mv) => {
    if (!mv) return null
    return `${mv.emoji || ''} ${mv.name || mv.label || ''}${mv.animal ? ` (${mv.animal})` : ''}`.trim()
  }

  return (
    <div className="widget fate-widget">
      <h3 className="widget-title">🎲 Vạn sự tùy duyên</h3>
      <p className="widget-sub">Xúc xắc lớn quyết định số phận bữa ăn hôm nay!</p>

      <div className="fate-controls">
        <button type="button" className="lootbox-open fate-btn" onClick={() => roll(false)} disabled={state === 'rolling'}>
          {state === 'rolling' ? 'Đang xúc...' : 'Xúc ngẫu nhiên 🎲'}
        </button>
        <button type="button" className="fate-btn-soft" onClick={() => roll(true)} disabled={state === 'rolling'}>
          Tôi nghiêng về món ngon hơn (gợi ý theo điểm)
        </button>
      </div>

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

      {result && state === 'result' && (
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
            <img src={result.dish.image_url} alt={result.dish.name} className="lootbox-result-img"
                 onError={(e) => { e.target.src = '/images/fallback.svg' }} />
            <div className="lootbox-result-info">
              <RarityBadge rarity={result.dish.rarity} />
              <div className="lootbox-result-name">{result.dish.name}</div>
              <div className="lootbox-result-meta">
                <span>&#9733; {result.dish.avg_rating.toFixed(1)}/10</span>
                <span>{result.dish.avg_price.toLocaleString('vi-VN')}đ</span>
              </div>
              <div className="fate-actions">
                <Link to={`/dish/${result.dish.slug}`} className="lootbox-result-link">Chọn món này &#8594;</Link>
                <button type="button" className="fate-btn-soft" onClick={() => { setState('idle'); setResult(null) }}>Quay lại</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}