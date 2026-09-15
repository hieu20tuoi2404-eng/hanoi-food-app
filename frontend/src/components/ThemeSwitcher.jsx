import React from 'react'
import { useApp } from '../context/AppContext'

const THEME_ICONS = {
  'ha-noi-co-dien': '🏯',
  'pho-dem': '🌙',
  healthy: '🥗',
  'toi-gian': '⬜',
  'tet-le-hoi': '🎆',
}

export default function ThemeSwitcher() {
  const { themes, themeId, setThemeId, mascots } = useApp()

  const iconFor = (t) => {
    if (THEME_ICONS[t.id]) return THEME_ICONS[t.id]
    if (t.mascot_id) {
      const m = mascots.find((mm) => mm.id === t.mascot_id)
      if (m) return m.emoji
    }
    return '🎨'
  }

  return (
    <div className="theme-switcher">
      <span className="theme-switcher-label" title="Đổi giao diện">
        🎨
      </span>
      {themes.map((t) => (
        <button
          key={t.id}
          type="button"
          className={`theme-dot ${themeId === t.id ? 'active' : ''}`}
          title={t.name}
          onClick={() => setThemeId(t.id)}
          style={{ '--dot': t.colors.accent }}
        >
          <span className="theme-dot-icon">{iconFor(t)}</span>
        </button>
      ))}
    </div>
  )
}