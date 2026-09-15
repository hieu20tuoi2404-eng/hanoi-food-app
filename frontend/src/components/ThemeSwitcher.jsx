import React from 'react'
import { useApp } from '../context/AppContext'

const THEME_ICONS = {
  'ha-noi-co-dien': '🏯',
  'pho-dem': '🌙',
  'hoi-meo': '🐱',
  healthy: '🥗',
  'toi-gian': '⬜',
  'tet-le-hoi': '🎆',
}

export default function ThemeSwitcher() {
  const { themes, themeId, setThemeId } = useApp()

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
          <span className="theme-dot-icon">{THEME_ICONS[t.id] || '🎨'}</span>
        </button>
      ))}
    </div>
  )
}