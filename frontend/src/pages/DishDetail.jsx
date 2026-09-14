import React, { useCallback, useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import RarityBadge from '../components/RarityBadge'

const API = import.meta.env.VITE_API_BASE || ''

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
      const res = await fetch(`${API}/api/dishes/${slug}`)
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
      const res = await fetch(`${API}/api/dishes/${dish.id}/reviews`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          rating: Number(rating),
          comment,
          reviewer_name: name.trim() || 'Ẩn danh',
        }),
      })
      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.detail || 'Đánh giá không hợp lệ')
      }
      const created = await res.json()
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

  return (
    <div>
      <Link to="/" className="back-link">&#8592; Về trang chủ</Link>

      <div className="detail-header">
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
          {dish.image_source && (
            <div className="detail-source">Nguồn ảnh: {dish.image_source}</div>
          )}
        </div>
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