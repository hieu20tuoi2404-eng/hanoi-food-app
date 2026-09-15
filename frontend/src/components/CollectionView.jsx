import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import DishCard from './DishCard'

export default function CollectionView() {
  const API = import.meta.env.VITE_API_BASE || ''
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [search, setSearch] = useState('')
  const [minRarity, setMinRarity] = useState(0)

  useEffect(() => {
    let cancelled = false
    const sid = localStorage.getItem('angi_session_id') || ''
    fetch(`${API}/api/collection`, { headers: { 'X-Session-Id': sid } })
      .then((r) => {
        if (!r.ok) throw new Error('Không tải được bộ sưu tập')
        return r.json()
      })
      .then((d) => {
        if (!cancelled) setData(d)
      })
      .catch((e) => {
        if (!cancelled) setError(e.message)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [])

  const ratio = data && data.total ? Math.round((data.collected / data.total) * 100) : 0

  const cards = (data?.cards || []).filter((c) => {
    if (search && !c.name.toLowerCase().includes(search.toLowerCase())) return false
    if (minRarity && c.rarity.level > minRarity) return false
    return true
  })

  return (
    <div className="collection">
      <div className="collection-head">
        <h2 className="section-title">🎴 Bộ sưu tập món Hà Nội</h2>
        <p className="collection-sub">
          Xem món ăn để mở khóa thẻ! Đây chỉ là trò chơi khám phá, không phải đánh giá chất lượng tuyệt đối.
        </p>
        {data && (
          <div className="collection-progress">
            <div className="collection-progress-track">
              <div className="collection-progress-fill" style={{ width: `${ratio}%` }} />
            </div>
            <span>{data.collected}/{data.total} đã sưu tầm ({ratio}%)</span>
          </div>
        )}
      </div>

      <div className="collection-tools">
        <input
          type="search"
          className="search-input"
          placeholder="Tìm món trong bộ sưu tập..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select value={minRarity} onChange={(e) => setMinRarity(Number(e.target.value))}>
          <option value={0}>Tất cả độ hiếm</option>
          <option value={1}>Hiếm trở lên</option>
          <option value={2}>Sử thi trở lên</option>
          <option value={3}>Huyền thoại</option>
        </select>
      </div>

      {loading && <div className="loading">Đang mở album...</div>}
      {error && !loading && <div className="empty">Lỗi: {error}</div>}

      {!loading && !error && (
        <>
          {cards.length === 0 ? (
            <div className="empty">Không có thẻ nào khớp.</div>
          ) : (
            <div className="dish-grid collection-grid">
              {cards.map((c) => (
                <Link key={c.id} to={`/dish/${c.slug}`} className={`collection-slot ${c.collected ? 'collected' : 'locked'}`} style={{ '--slot-accent': c.rarity.key }}>
                  {c.collected ? (
                    <DishCard dish={c} />
                  ) : (
                    <div className="collection-locked-card">
                      <span className="collection-locked-icon">🔒</span>
                      <span className="collection-locked-name">{c.name}</span>
                      <span className="collection-locked-rare">{c.rarity.label}?</span>
                    </div>
                  )}
                </Link>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}