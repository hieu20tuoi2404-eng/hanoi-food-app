import React, { useCallback, useMemo, useState } from 'react'
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

export default function HoiMeo() {
  const [selected, setSelected] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [rollHistory, setRollHistory] = useState([])

  const roll = useCallback(async (cat) => {
    setSelected(cat)
    setLoading(true)
    setResult(null)
    setError('')
    try {
      const p = new URLSearchParams({ meal: cat.meal })
      const res = await fetch(`${API}/api/dishes/random?${p}`)
      if (!res.ok) throw new Error('Không lấy được món')
      const data = await res.json()
      setResult(data)
      setRollHistory((h) => [data, ...h].slice(0, 5))
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [])

  const reset = useCallback(() => {
    setSelected(null)
    setResult(null)
    setError('')
  }, [])

  return (
    <div className="hoi-meo">
      <div className="hoi-meo-head">
        <div className="hoi-meo-tag">HỘI MÈO · THÚ CƯNG HÀ NỘI</div>
        <h2 className="hoi-meo-title">Hội Mèo Hà Nội</h2>
        <p className="hoi-meo-sub">Chọn một em mèo để nó gợi ý bữa ăn cho bạn!</p>
      </div>

      <div className="hoi-meo-grid">
        {CATS.map((cat) => (
          <button
            key={cat.id}
            className={`hoi-meo-card ${selected?.id === cat.id ? 'selected' : ''}`}
            onClick={() => roll(cat)}
            disabled={loading}
            style={{ '--cat-color': cat.color }}
            type="button"
          >
            <span className="hoi-meo-emoji">{cat.emoji}</span>
            <strong>{cat.name}</strong>
            <span className="hoi-meo-desc">{cat.desc}</span>
          </button>
        ))}
      </div>

      {loading && <div className="hoi-meo-loading">Đang chọn món...</div>}
      {error && <div className="hoi-meo-error">{error}</div>}

      {result && (
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
            Chọn lại em khác 🔄
          </button>
        </div>
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
  )
}