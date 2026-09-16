import React from 'react'
import { Link } from 'react-router-dom'

const MEAL_LABELS = {
  breakfast: 'Bữa sáng',
  lunch: 'Bữa trưa',
  dinner: 'Bữa tối',
  snack: 'Ăn vặt',
  drinking: 'Món nhậu',
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
        <span className="dish-card-meal">{MEAL_LABELS[dish.meal_type] || dish.meal_type}</span>
      </div>
      <div className="dish-card-body">
        <div className="dish-card-name">{dish.name}</div>
        <p className="dish-card-desc">{dish.description}</p>

        {dish.key_ingredients && dish.key_ingredients.length > 0 && (
          <div className="dish-card-tags">
            {dish.key_ingredients.slice(0, 3).map((ing, i) => (
              <span key={i} className="dish-card-tag">{ing}</span>
            ))}
            {dish.key_ingredients.length > 3 && <span className="dish-card-tag more">+{dish.key_ingredients.length - 3}</span>}
          </div>
        )}

        <div className="dish-card-meta">
          <span className="dish-card-rating">&#9733; {dish.avg_rating.toFixed(1)}/10</span>
          <span className="dish-card-price">{dish.avg_price.toLocaleString('vi-VN')}đ</span>
        </div>
        <div className="dish-card-health">
          {dish.healthy_score != null && <span className="dish-card-health-item" title="Điểm healthy">🥗 {dish.healthy_score}/10</span>}
          {dish.oil_level === 'high' && <span className="dish-card-health-item oil-high" title="Nhiều dầu mỡ">🛢️ nhiều dầu</span>}
          {dish.oil_level === 'low' && <span className="dish-card-health-item" title="Ít dầu mỡ">🛢️ ít dầu</span>}
          {dish.spicy_level === 'high' && <span className="dish-card-health-item" title="Cay">🌶 cay</span>}
          {dish.vegetarian && <span className="dish-card-health-item veg" title="Ăn chay được">🥦 chay</span>}
          {dish.calories_estimate != null && (
            <span className="dish-card-health-item" title={dish.calories_source || 'Calories'}>🔥 {dish.calories_estimate} kcal</span>
          )}
        </div>
        <div className="dish-card-foot">
          {dish.is_demo && <span className="dish-card-demo">Demo · Chưa xác minh</span>}
          {dish.cuisine && <span className="dish-card-cuisine">{dish.cuisine}{dish.dish_origin && dish.dish_origin !== dish.cuisine ? ` · ${dish.dish_origin}` : ''}</span>}
          <span className="dish-card-open">Xem chi tiết &#8594;</span>
        </div>
      </div>
    </Link>
  )
}