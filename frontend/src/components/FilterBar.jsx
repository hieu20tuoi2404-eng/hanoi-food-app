import React from 'react'

const DISTRICTS = [
  'Hoàn Kiếm', 'Đống Đa', 'Ba Đình', 'Hai Bà Trưng',
  'Thanh Xuân', 'Cầu Giấy', 'Hoàng Mai', 'Long Biên',
  'Nam Từ Liêm',
]

// Budget tiers used for both the grid filter and the loot box spin.
export const BUDGETS = [
  { id: '', label: 'Mọi ngân sách', min: '', max: '', icon: '🎲' },
  { id: 'd30', label: 'Dưới 30k', min: 0, max: 30000, icon: '🌱' },
  { id: 't30_60', label: '30–60k', min: 30000, max: 60000, icon: '🌤' },
  { id: 't60_100', label: '60–100k', min: 60000, max: 100000, icon: '⭐' },
  { id: 't100', label: 'Trên 100k', min: 100000, max: '', icon: '👑' },
]

// Selected budget stored as {id, min, max}.
export function budgetParam(id) {
  const b = BUDGETS.find((x) => x.id === id)
  if (!b || id === '') return { min_price: '', max_price: '' }
  return { min_price: b.min === '' ? '' : String(b.min), max_price: b.max === '' ? '' : String(b.max) }
}

// Phong cách ăn (diet) — khớp key với _build_filters backend
export const DIET_OPTIONS = [
  { id: '', label: 'Mọi kiểu', icon: '🎲' },
  { id: 'healthy', label: 'Healthy', icon: '🥗' },
  { id: 'light_oil', label: 'Ít dầu mỡ', icon: '🌱' },
  { id: 'rich_oil', label: 'Ăn thoải mái', icon: '🍗' },
  { id: 'high_protein', label: 'Nhiều đạm', icon: '💪' },
  { id: 'vegetarian', label: 'Ăn chay', icon: '🥦' },
  { id: 'spicy', label: 'Ăn cay', icon: '🌶' },
  { id: 'light', label: 'Ăn nhẹ', icon: '🍵' },
]

// Hoàn cảnh đi ăn — khớp tag quán trong seed (occasion_tags)
export const OCCASION_OPTIONS = [
  { id: '', label: 'Mọi hoàn cảnh', icon: '🔄' },
  { id: 'solo', label: 'Đi một mình', icon: '🚶' },
  { id: 'date', label: 'Đi date', icon: '💞' },
  { id: 'friends', label: 'Bạn bè', icon: '👯' },
  { id: 'family', label: 'Gia đình', icon: '👨‍👩‍👧' },
  { id: 'drinking', label: 'Đi nhậu', icon: '🍻' },
  { id: 'quick', label: 'Ăn nhanh', icon: '⚡' },
  { id: 'work', label: 'Gặp khách', icon: '💼' },
]

// Màu món ăn — khớp dominant_color/color_tags
export const COLOR_OPTIONS = [
  { id: '', label: 'Mọi màu', icon: '🌈' },
  { id: 'red', label: 'Đỏ', icon: '🔴' },
  { id: 'yellow', label: 'Vàng', icon: '🟡' },
  { id: 'green', label: 'Xanh', icon: '🟢' },
  { id: 'white', label: 'Trắng', icon: '⚪' },
  { id: 'brown', label: 'Nâu', icon: '🟤' },
  { id: 'orange', label: 'Cam', icon: '🟠' },
  { id: 'multi', label: 'Nhiều màu', icon: '🎨' },
]

function ChipGroup({ label, options, value, onPick }) {
  return (
    <div className="mood-group">
      <span className="mood-group-label">{label}</span>
      <div className="mood-chips">
        {options.map((o) => (
          <button
            key={o.id}
            type="button"
            className={`mood-chip ${value === o.id ? 'active' : ''}`}
            onClick={() => onPick(o.id)}
            title={o.label}
          >
            <span className="mood-chip-icon">{o.icon}</span>
            {o.label}
          </button>
        ))}
      </div>
    </div>
  )
}

export default function FilterBar({ filters, onChange }) {
  const set = (key, value) => onChange({ ...filters, [key]: value })

  return (
    <div className="filter-bar-wrap">
      <div className="mood-bar">
        <ChipGroup label="Ăn theo mood" options={DIET_OPTIONS} value={filters.diet || ''} onPick={(id) => set('diet', id)} />
        <ChipGroup label="Hoàn cảnh" options={OCCASION_OPTIONS} value={filters.occasion || ''} onPick={(id) => set('occasion', id)} />
        <ChipGroup label="Màu món" options={COLOR_OPTIONS} value={filters.color || ''} onPick={(id) => set('color', id)} />
      </div>
      <div className="filter-bar">
        <select value={filters.district || ''} onChange={(e) => set('district', e.target.value)}>
          <option value="">Tất cả quận</option>
          {DISTRICTS.map((d) => (
            <option key={d} value={d}>{d}</option>
          ))}
        </select>

        <select value={filters.min_price || ''} onChange={(e) => set('min_price', e.target.value)}>
          <option value="">Mọi giá</option>
          <option value="0">Dưới 30.000d</option>
          <option value="30000">30.000 - 100.000d</option>
          <option value="100000">Trên 100.000d</option>
        </select>

        <select value={filters.min_rating || ''} onChange={(e) => set('min_rating', e.target.value)}>
          <option value="">Mọi điểm</option>
          <option value="9">SỬ THI: 9/10 trở lên</option>
          <option value="8">HIẾM: 8/10 trở lên</option>
          <option value="7">THƯỜNG: 7/10 trở lên</option>
        </select>
      </div>
    </div>
  )
}