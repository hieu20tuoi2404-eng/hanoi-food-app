import React from 'react'
import { Link } from 'react-router-dom'
import RarityBadge from './RarityBadge'

const MEAL_LABELS = {
  breakfast: 'Bữa sáng',
  lunch: 'Bữa trưa',
  dinner: 'Bữa tối',
  snack: 'Ăn vặt',
}

export default function DishCard({ dish }) {
  return (
    <Link to={`/dish/${dish.slug}`} className="dish-card">
      <div className="dish-card-img-wrap">
        <img
          src={dish.image_url || '/images/fallback.svg'}
          alt={dish.name}
          className="dish-card-img"
          loading="lazy"
          onError={(e) => {
            e.target.src = '/images/fallback.svg'
          }}
        />
        <div className="dish-card-rare">
          <RarityBadge rarity={dish.rarity} />
        </div>
        <span className="dish-card-meal">{MEAL_LABELS[dish.meal_type] || dish.meal_type}</span>
      </div>
      <div className="dish-card-body">
        <div className="dish-card-name">{dish.name}</div>
        <p className="dish-card-desc">{dish.description}</p>
        <div className="dish-card-meta">
          <span className="dish-card-rating">&#9733; {dish.avg_rating.toFixed(1)}/10</span>
          <span className="dish-card-price">{dish.avg_price.toLocaleString('vi-VN')}đ</span>
        </div>
        <div className="dish-card-foot">
          {dish.is_demo && <span className="dish-card-demo">Demo · Chưa xác minh</span>}
          <span className="dish-card-open">Xem chi tiết &#8594;</span>
        </div>
      </div>
    </Link>
  )
}