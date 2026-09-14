import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import RarityBadge from './RarityBadge'

const API = import.meta.env.VITE_API_BASE || ''

export default function QuaTrua() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const draw = async () => {
    setLoading(true)
    setError('')
    setData(null)
    try {
      const res = await fetch(`${API}/api/fortunes`)
      if (!res.ok) throw new Error('Chưa xin được quẻ. Thử lại nhé!')
      setData(await res.json())
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="quatrua">
      <div className="quatrua-head">
        <h2 className="quatrua-title"><span className="loot-icon">🔮</span> Quẻ trưa</h2>
        <p className="quatrua-sub">Bói một quẻ xem trưa nay ăn gì cho "hợp duyên"!</p>
      </div>

      <button className="quatrua-btn" onClick={draw} disabled={loading} type="button">
        {loading ? 'Đang xin quẻ...' : 'Xin quẻ ✨'}
      </button>

      {error && <div className="lootbox-error">{error}</div>}

      {data && !loading && (
        <div className={`quatrua-result rarity-card-${data.dish.rarity.key}`}>
          <p className="quatrua-fortune">"{data.fortune}"</p>
          <div className="lootbox-result-main">
            <img
              src={data.dish.image_url || '/images/fallback.svg'}
              alt={data.dish.name}
              className="lootbox-result-img"
              onError={(e) => { e.target.src = '/images/fallback.svg' }}
            />
            <div className="lootbox-result-info">
              <div className="lootbox-result-top" style={{ marginBottom: 6 }}>
                <span className="lootbox-result-label">QUẺ CỦA BẠN</span>
                <RarityBadge rarity={data.dish.rarity} />
              </div>
              <div className="lootbox-result-name">{data.dish.name}</div>
              <div className="lootbox-result-meta">
                <span className="dish-card-rating">&#9733; {data.dish.avg_rating.toFixed(1)}/10</span>
                <span className="dish-card-price">{data.dish.avg_price.toLocaleString('vi-VN')}đ</span>
              </div>
              <Link to={`/dish/${data.dish.slug}`} className="lootbox-result-link">
                Xem chi tiết &#8594;
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}