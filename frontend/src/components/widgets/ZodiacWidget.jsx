import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import RarityBadge from '../cards/RarityBadge'

const API = import.meta.env.VITE_API_BASE || ''

function sessionHeaders(extra = {}) {
  const headers = { ...extra }
  const sid = localStorage.getItem('angi_session_id')
  if (sid) headers['X-Session-Id'] = sid
  return headers
}

export default function ZodiacWidget() {
  const [day, setDay] = useState('')
  const [month, setMonth] = useState('')
  const [year, setYear] = useState('')
  const [consent, setConsent] = useState(false)
  const [saved, setSaved] = useState(null)
  const [rec, setRec] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const look = async () => {
    setError('')
    setRec(null)
    if (!day || !month) {
      setError('Vui lòng nhập ngày và tháng sinh.')
      return
    }
    setLoading(true)
    try {
      // Tạo profile nếu chưa có + lấy gợi ý
      const profileRes = await fetch(`${API}/api/zodiac/profile`, {
        method: 'POST',
        headers: sessionHeaders({ 'Content-Type': 'application/json' }),
        body: JSON.stringify({ day: Number(day), month: Number(month), year: year ? Number(year) : null, consent_save: consent }),
      })
      if (!profileRes.ok) {
        const d = await profileRes.json()
        throw new Error(d.detail || 'Không lưu được')
      }
      setSaved(await profileRes.json())
      const recRes = await fetch(`${API}/api/zodiac/recommendation?day=${Number(day)}&month=${Number(month)}`)
      if (!recRes.ok) throw new Error('Không lấy được gợi ý')
      setRec(await recRes.json())
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const clearProfile = async () => {
    if (!saved || !saved.id) return
    try {
      await fetch(`${API}/api/zodiac/profile/${saved.id}`, { method: 'DELETE', headers: sessionHeaders() })
      setSaved(null)
      setRec(null)
    } catch (e) {
      setError(e.message)
    }
  }

  const ENG = 'Gợi ý vui, không phải tư vấn khoa học hoặc dự đoán chắc chắn.'

  return (
    <div className="widget zodiac-widget">
      <h3 className="widget-title">♈ Cung hoàng đạo &amp; món hợp</h3>
      <p className="widget-sub">Nhập ngày sinh để xem gợi ý món "hợp duyên" (chỉ để vui!).</p>

      <div className="zodiac-inputs">
        <input type="number" min={1} max={31} placeholder="Ngày" value={day} onChange={(e) => setDay(e.target.value)} />
        <input type="number" min={1} max={12} placeholder="Tháng" value={month} onChange={(e) => setMonth(e.target.value)} />
        <input type="number" min={1900} max={2100} placeholder="Năm (tùy chọn)" value={year} onChange={(e) => setYear(e.target.value)} />
      </div>
      <div className="zodiac-consent">
        <label>
          <input type="checkbox" checked={consent} onChange={(e) => setConsent(e.target.checked)} />
          Cho phép lưu năm sinh để gợi ý tốt hơn (không bắt buộc)
        </label>
      </div>
      <button className="lootbox-open zodiac-btn" type="button" onClick={look} disabled={loading}>
        {loading ? 'Đang bói...' : 'Xem gợi ý ✨'}
      </button>

      {error && <div className="lootbox-error">{error}</div>}

      {rec && (
        <div className="zodiac-result">
          <div className="zodiac-sign">
            <span className="zodiac-sign-emoji">{rec.sign.emoji}</span>
            <span className="zodiac-sign-name">{rec.sign.name}</span>
          </div>
          <p className="zodiac-flavour">Hợp khẩu vị: {rec.flavour}</p>
          {rec.dish ? (
            <div className="zodiac-dish">
              <img src={rec.dish.image_url} alt={rec.dish.name} className="lootbox-result-img" onError={(e) => { e.target.src = '/images/fallback.svg' }} />
              <div>
                <RarityBadge rarity={rec.dish.rarity} />
                <div className="lootbox-result-name">{rec.dish.name}</div>
                <div className="lootbox-result-meta">
                  <span>&#9733; {rec.dish.avg_rating.toFixed(1)}/10</span>
                  <span>{rec.dish.avg_price.toLocaleString('vi-VN')}đ</span>
                </div>
                <Link to={`/dish/${rec.dish.slug}`} className="lootbox-result-link">Xem chi tiết &#8594;</Link>
              </div>
            </div>
          ) : (
            <p className="empty small">Chưa có món hợp. Thử nhập ngày sinh khác.</p>
          )}
          <p className="entertainment-note">{ENG}</p>
          {saved && saved.id && (
            <button type="button" className="zodiac-clear" onClick={clearProfile}>Xóa thông tin ngày sinh</button>
          )}
        </div>
      )}
    </div>
  )
}