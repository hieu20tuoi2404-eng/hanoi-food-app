import React, { useCallback, useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import RarityBadge from '../components/RarityBadge'
import { api, getSessionId } from '../api'

export default function DishDetail() {
  const { slug } = useParams()
  const [dish, setDish] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // review form
  const [rating, setRating] = useState(8)
  const [comment, setComment] = useState('')
  const [name, setName] = useState('')
  const [formMsg, setFormMsg] = useState('')
  const [formError, setFormError] = useState('')

  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      // pass X-Session-Id so view is tracked
      const res = await fetch(`${import.meta.env.VITE_API_BASE || ''}/api/dishes/${slug}`, {
        headers: { 'X-Session-Id': getSessionId() },
      })
      if (!res.ok) throw new Error('Không tìm thấy món ăn')
      setDish(await res.json())
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [slug])

  useEffect(() => {
    load()
  }, [load])

  const submitReview = async (e) => {
    e.preventDefault()
    setFormMsg('')
    setFormError('')
    try {
      const created = await api(`/api/dishes/${dish.id}/reviews`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          rating: Number(rating),
          comment,
          reviewer_name: name.trim() || 'Ẩn danh',
        }),
      })
      setDish((old) => ({
        ...old,
        reviews: [created, ...(old.reviews || [])],
      }))
      setComment('')
      setName('')
      setFormMsg('Đã gửi đánh giá. Cảm ơn bạn!')
    } catch (err) {
      setFormError(err.message)
    }
  }

  if (loading) return <div className="loading">Đang tải...</div>
  if (error) return <div className="empty">{error}<br /><Link className="back-link" to="/">&#8592; Về trang chủ</Link></div>
  if (!dish) return null

  const rarityKey = dish.rarity?.key
  const rarityBorder =
    rarityKey === 'legendary' ? '#f8b500'
      : rarityKey === 'epic' ? '#8e2de2'
      : rarityKey === 'rare' ? '#3b82f6'
      : undefined

  return (
    <div>
      <Link to="/" className="back-link">&#8592; Về trang chủ</Link>

      <div className="detail-header" style={rarityBorder ? { borderLeft: `5px solid ${rarityBorder}`, paddingLeft: 18 } : undefined}>
        <img
          src={dish.image_url || '/images/fallback.svg'}
          alt={dish.name}
          className="detail-img"
          onError={(e) => { e.target.src = '/images/fallback.svg' }}
        />
        <div className="detail-info">
          <div className="detail-topline">
            <RarityBadge rarity={dish.rarity} />
            {dish.is_demo && <span className="detail-demo-badge">Demo - Chưa xác minh</span>}
          </div>
          <h1>{dish.name}</h1>
          <div className="detail-rating">&#9733; {dish.avg_rating.toFixed(1)}/10 &middot; {dish.avg_price.toLocaleString('vi-VN')}đ</div>
          <div className="detail-desc">{dish.description}</div>

          <div className="detail-meta-row">
            {dish.cuisine && (
              <span className="detail-meta-tag">{dish.cuisine}{dish.dish_origin && dish.dish_origin !== dish.cuisine ? ` · ${dish.dish_origin}` : ''}</span>
            )}
            {dish.verification_status && (
              <span className="detail-meta-tag verify">{dish.verification_status === 'demo' ? 'Chưa xác minh' : dish.verification_status}</span>
            )}
          </div>

          {dish.key_ingredients && dish.key_ingredients.length > 0 && (
            <div className="detail-ingredients">
              <b>Thành phần:</b> {dish.key_ingredients.join(', ')}
            </div>
          )}

          {dish.image_source && (
            <div className="detail-source">Nguồn ảnh: {dish.image_source}</div>
          )}
        </div>
      </div>

      <div className="section">
        <h2 className="section-title">Dinh dưỡng &amp; phong cách</h2>
        <div className="nutrition-grid">
          <div className="nutrition-cell">
            <span className="nutrition-icon">🔥</span>
            <span className="nutrition-label">Calories</span>
            <span className="nutrition-value">
              {dish.calories_estimate ? `${dish.calories_estimate} kcal` : 'Chưa có thông tin'}
            </span>
            {dish.calories_source ? (
              <span className="nutrition-note">{dish.calories_source}</span>
            ) : (
              <span className="nutrition-note unverified">Chưa xác minh</span>
            )}
          </div>
          <div className="nutrition-cell">
            <span className="nutrition-icon">🛢️</span>
            <span className="nutrition-label">Dầu mỡ</span>
            <span className="nutrition-value">{{ low: 'Ít', medium: 'Vừa', high: 'Nhiều' }[dish.oil_level] || dish.oil_level || 'Chưa có thông tin'}</span>
          </div>
          <div className="nutrition-cell">
            <span className="nutrition-icon">🌶</span>
            <span className="nutrition-label">Vị cay</span>
            <span className="nutrition-value">{{ none: 'Không cay', low: 'Ít', medium: 'Vừa', high: 'Cay' }[dish.spicy_level] || dish.spicy_level || 'Chưa có thông tin'}</span>
          </div>
          <div className="nutrition-cell">
            <span className="nutrition-icon">💪</span>
            <span className="nutrition-label">Đạm</span>
            <span className="nutrition-value">{{ low: 'Ít', medium: 'Vừa', high: 'Nhiều' }[dish.protein_level] || dish.protein_level || 'Chưa có thông tin'}</span>
          </div>
          <div className="nutrition-cell">
            <span className="nutrition-icon">🥦</span>
            <span className="nutrition-label">Ăn chay</span>
            <span className="nutrition-value">{dish.vegetarian ? 'Có' : 'Không'}</span>
          </div>
          <div className="nutrition-cell">
            <span className="nutrition-icon">🥗</span>
            <span className="nutrition-label">Healthy</span>
            <span className="nutrition-value">{dish.healthy_score != null ? `${dish.healthy_score}/10` : 'Chưa có thông tin'}</span>
          </div>
        </div>
        <div className="detail-source">
          {dish.verification_status === 'demo'
            ? 'Dữ liệu dinh dưỡng đang để chế độ demo - chưa xác minh từ nguồn chính thức.'
            : 'Dữ liệu dinh dưỡng theo metadata món.'}
        </div>
        {dish.dominant_color && (
          <div className="detail-meta-row" style={{ marginTop: 8 }}>
            <span className="detail-meta-tag" style={{ background: 'var(--border)' }}>
              Màu nổi bật: {{ red: 'Đỏ', yellow: 'Vàng', green: 'Xanh', white: 'Trắng', brown: 'Nâu', orange: 'Cam', purple: 'Tím', multi: 'Nhiều màu' }[dish.dominant_color] || dish.dominant_color}
              {dish.color_tags && dish.color_tags.length > 0 ? ` (${dish.color_tags.map((c) => ({ red: 'đỏ', yellow: 'vàng', green: 'xanh', white: 'trắng', brown: 'nâu', orange: 'cam', purple: 'tím', multi: 'nhiều màu' }[c] || c)).join(', ')})` : ''}
            </span>
            <span className="detail-meta-tag verify">{dish.color_source || dish.verification_status === 'demo' ? 'Chưa xác minh' : 'Đã xác minh'}</span>
          </div>
        )}
      </div>

      <div className="section">
        <h2 className="section-title">Quán bán món này</h2>
        {dish.restaurants.length === 0 && <div className="empty">Chưa có dữ liệu quán.</div>}
        {dish.restaurants.map((r) => (
          <div className="restaurant-card" key={r.id}>
            <h3>{r.name}</h3>
            <p>Địa chỉ: {r.address} ({r.district})</p>
            <p>Giờ mở cửa: {r.hours}</p>
            <p>Giá tham khảo: {r.price_range}</p>
            {r.occasion_tags && r.occasion_tags.length > 0 && (
              <p className="restaurant-occasions">
                Phù hợp: {r.occasion_tags.map((t) => ({ solo: 'Một mình', quick: 'Ăn nhanh', date: 'Date', friends: 'Bạn bè', family: 'Gia đình', drinking: 'Nhậu', work: 'Làm việc' }[t] || t)).join(', ')}
                <span className="dish-card-demo" style={{ marginLeft: 6 }}>Chưa xác minh</span>
              </p>
            )}
            <a href={r.maps_link} target="_blank" rel="noreferrer">Mở Google Maps &#8599;</a>
            {r.is_demo && <span className="dish-card-demo" style={{ marginLeft: 8 }}>Chưa xác minh</span>}
          </div>
        ))}
      </div>

      <div className="section">
        <h2 className="section-title">Công thức</h2>
        {dish.recipe ? (
          <div className="recipe-box">
            <h3>{dish.name}</h3>
            <div className="detail-price">Khẩu phần: {dish.recipe.portions} &middot; Thời gian nấu: {dish.recipe.cook_time}</div>
            <h3 style={{ marginTop: 12 }}>Nguyên liệu</h3>
            <ul className="recipe-list">
              {dish.recipe.ingredients.map((ing, i) => (
                <li key={i}>{ing}</li>
              ))}
            </ul>
            <h3>Các bước</h3>
            <ol className="recipe-steps">
              {dish.recipe.steps.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ol>
            <div className="detail-source">Nguồn công thức: {dish.recipe.source}</div>
          </div>
        ) : (
          <div className="empty">Chưa có công thức cho món này.</div>
        )}
      </div>

      <div className="section">
        <h2 className="section-title">Đánh giá ({dish.reviews.length})</h2>

        <form className="review-form" onSubmit={submitReview}>
          <label htmlFor="rating">Điểm (1-10)</label>
          <input
            id="rating"
            type="number"
            min={1}
            max={10}
            value={rating}
            onChange={(e) => setRating(e.target.value)}
            required
          />
          <label htmlFor="name">Tên của bạn (tuỳ chọn)</label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            maxLength={100}
            placeholder="Ẩn danh"
          />
          <label htmlFor="comment">Nhận xét</label>
          <textarea
            id="comment"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            minLength={3}
            maxLength={500}
            placeholder="Chia sẻ cảm nhận của bạn về món này..."
            required
          />
          <button type="submit">Gửi đánh giá</button>
          {formMsg && <p style={{ color: '#2f9e44', marginTop: 8 }}>{formMsg}</p>}
          {formError && <p style={{ color: '#d4451a', marginTop: 8 }}>Lỗi: {formError}</p>}
        </form>

        {dish.reviews.length === 0 && <div className="empty">Chưa có đánh giá. Hãy là người đầu tiên!</div>}
        {dish.reviews.map((rv) => (
          <div className="review-card" key={rv.id}>
            <div className="review-header">
              <div>
                <span className="review-name">{rv.reviewer_name}</span>
                {rv.is_demo && <span className="dish-card-demo" style={{ marginLeft: 6 }}>Demo</span>}
              </div>
              <span className="review-rating">{rv.rating}/10</span>
            </div>
            <div className="review-comment">{rv.comment}</div>
            <div className="review-date">{new Date(rv.created_at).toLocaleDateString('vi-VN')}</div>
          </div>
        ))}
      </div>
    </div>
  )
}