import React, { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useApp } from '../../context/AppContext'

export default function MascotPicker() {
  const { mascots, themes, setMascotId, closeMascotPicker, setThemeId } = useApp()
  const navigate = useNavigate()
  const loc = useLocation()
  const isPickerPage = loc.pathname === '/chon-con-giap'
  const [selectedId, setSelectedId] = useState(null)
  const [birthday, setBirthday] = useState('') // yyyy-mm-dd
  const [suggestion, setSuggestion] = useState(null) // { mascot_id, note }

  const selected = mascots.find((m) => m.id === selectedId) || null

  const handleBirthday = () => {
    if (!birthday) {
      setSuggestion(null)
      return
    }
    const [y, m, d] = birthday.split('-').map(Number)
    // Very approximate Western-zodiac → con giáp mapping, entertainment only.
    const sign =
      ((m === 3 && d >= 21) || (m === 4 && d <= 19)) ? '🐰' :
      ((m === 4 && d >= 20) || (m === 5 && d <= 20)) ? '🐂' :
      ((m === 5 && d >= 21) || (m === 6 && d <= 20)) ? '🐵' :
      ((m === 6 && d >= 21) || (m === 7 && d <= 22)) ? '🐈' :
      ((m === 7 && d >= 23) || (m === 8 && d <= 22)) ? '🐯' :
      ((m === 8 && d >= 23) || (m === 9 && d <= 22)) ? '🐐' :
      ((m === 9 && d >= 23) || (m === 10 && d <= 23)) ? '🐓' :
      ((m === 10 && d >= 24) || (m === 11 && d <= 21)) ? '🐍' :
      ((m === 11 && d >= 22) || (m === 12 && d <= 21)) ? '🐴' :
      ((m === 12 && d >= 22) || (m === 1 && d <= 19)) ? '🐂' :
      ((m === 1 && d >= 20) || (m === 2 && d <= 18)) ? '🐀' : '🐷'
    const matched = mascots.find((mm) => mm.emoji === sign)
    if (matched) {
      setSuggestion({
        mascot_id: matched.id,
        emoji: matched.emoji,
        name: matched.name,
        animal: matched.animal,
        note: 'Gợi ý vui theo ngày sinh — bạn có thể chọn con giáp khác nhé!',
      })
      setSelectedId(matched.id)
    } else {
      setSuggestion(null)
    }
  }

  const confirm = async () => {
    if (!selected) return
    await setMascotId(selected.id)
    // If a zodiac theme matches this mascot, suggest switching to it (not forced).
    const zodiac = themes?.find((t) => t.mascot_id === selected.id)
    if (zodiac) setThemeId(zodiac.id)
    closeMascotPicker()
    if (isPickerPage) navigate('/')
  }

  const skip = () => {
    closeMascotPicker()
    if (isPickerPage) navigate('/')
  }

  return (
    <div className="mascot-picker-overlay">
      <div className="mascot-picker">
        <h2>Chọn người bạn đồng hành</h2>
        <p className="mascot-picker-sub">
          12 con giáp sẽ đồng hành, gợi ý món và cổ vũ bạn. Gợi ý vui, không phải tư vấn khoa học.
        </p>

        {selected && (
          <div className="mascot-preview" style={{ '--preview-color': selected.theme_color }}>
            <span className="mascot-preview-emoji">{selected.emoji}</span>
            <div className="mascot-preview-info">
              <strong>{selected.name} – {selected.animal}</strong>
              <span>{selected.greeting}</span>
            </div>
          </div>
        )}

        <div className="mascot-grid">
          {mascots.map((m) => (
            <button
              key={m.id}
              type="button"
              className={`mascot-card ${selectedId === m.id ? 'active' : ''}`}
              style={{ '--mascot-color': m.theme_color, '--mascot-secondary': m.secondary_color }}
              onClick={() => setSelectedId(m.id)}
            >
              <span className="mascot-card-emoji">{m.emoji}</span>
              <span className="mascot-card-name">{m.name}</span>
              <span className="mascot-card-animal">{m.animal}</span>
            </button>
          ))}
        </div>

        <div className="mascot-birthday">
          <label htmlFor="mascot-birthday">
            🎂 Có thể gợi ý theo ngày sinh (tuỳ chọn, chỉ để giải trí):
          </label>
          <div className="mascot-birthday-row">
            <input
              id="mascot-birthday"
              type="date"
              value={birthday}
              onChange={(e) => { setBirthday(e.target.value); setSuggestion(null) }}
            />
            <button type="button" className="btn btn-ghost" onClick={handleBirthday}>
              Gợi ý
            </button>
          </div>
          {suggestion && (
            <p className="mascot-suggestion">
              Gợi ý: <strong>{suggestion.emoji} {suggestion.name} – {suggestion.animal}</strong>. {suggestion.note}
            </p>
          )}
        </div>

        <div className="mascot-picker-actions">
          <button type="button" className="btn btn-primary" disabled={!selected} onClick={confirm}>
            {selected ? `Chọn linh vật ${selected.emoji} (${selected.name})` : 'Chọn linh vật này'}
          </button>
          {selectedId && (
            <button type="button" className="btn btn-ghost" onClick={() => setSelectedId(null)}>
              Đổi linh vật
            </button>
          )}
          <button type="button" className="btn btn-ghost" onClick={skip}>
            Tiếp tục không chọn
          </button>
        </div>
        <p className="mascot-picker-footnote">
          Lựa chọn được lưu trên thiết bị của bạn. Bạn có thể đổi hoặc xoá trong Cài đặt.
        </p>
      </div>
    </div>
  )
}