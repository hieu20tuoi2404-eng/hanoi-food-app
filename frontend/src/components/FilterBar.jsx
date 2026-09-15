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

export default function FilterBar({ filters, onChange }) {
  const set = (key, value) => onChange({ ...filters, [key]: value })

  return (
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
  )
}