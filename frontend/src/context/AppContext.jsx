import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react'

const API = import.meta.env.VITE_API_BASE || ''

function getSessionId() {
  let id = localStorage.getItem('angi_session_id')
  if (!id) {
    id = `web-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`
    localStorage.setItem('angi_session_id', id)
  }
  return id
}

const DEFAULT_THEME = {
  id: 'ha-noi-co-dien',
  name: 'Hà Nội cổ điển',
  colors: {
    bg: '#faf8f5',
    bg_gradient: 'linear-gradient(160deg, #fff8f0 0%, #faf5ef 45%, #f6f0ea 100%)',
    card_bg: '#ffffff',
    text: '#211a14',
    text_muted: '#6b6257',
    accent: '#d4451a',
    accent_dark: '#b03810',
    accent_light: '#fff1eb',
    border: '#e9e2d9',
  },
  mascot: 'default',
}

const AppContext = createContext({ sessionId: '', api: null, themes: [], themeId: '', setThemeId: () => {}, appliedTheme: DEFAULT_THEME })

export function AppProvider({ children }) {
  const [sessionId] = useState(getSessionId)
  const [themes, setThemes] = useState([])
  const [themeId, setThemeId] = useState(DEFAULT_THEME.id)
  const [appliedTheme, setAppliedTheme] = useState(DEFAULT_THEME)

  const applyTheme = useCallback((theme) => {
    if (!theme || !theme.colors) return
    const root = document.documentElement
    const c = theme.colors
    root.style.setProperty('--bg', c.bg)
    root.style.setProperty('--bg-gradient', c.bg_gradient)
    root.style.setProperty('--card-bg', c.card_bg)
    root.style.setProperty('--text', c.text)
    root.style.setProperty('--text-muted', c.text_muted)
    root.style.setProperty('--accent', c.accent)
    root.style.setProperty('--accent-dark', c.accent_dark)
    root.style.setProperty('--accent-light', c.accent_light)
    root.style.setProperty('--border', c.border)
    root.dataset.mascot = theme.mascot || 'default'
    root.dataset.theme = theme.id || 'default'
    setAppliedTheme(theme)
  }, [])

  // Load themes + the user's saved theme on mount.
  useEffect(() => {
    let cancelled = false
    ;(async () => {
      try {
        const [themesRes, selRes] = await Promise.all([
          fetch(`${API}/api/themes`),
          fetch(`${API}/api/themes/selection`, { headers: { 'X-Session-Id': sessionId } }),
        ])
        if (themesRes.ok) {
          const list = await themesRes.json()
          if (!cancelled) setThemes(list)
        }
        if (selRes.ok && !cancelled) {
          const sel = await selRes.json()
          if (sel.theme_id) setThemeId(sel.theme_id)
        }
      } catch (e) {
        /* offline: keep defaults */
      }
    })()
    return () => {
      cancelled = true
    }
  }, [sessionId])

  // Apply whatever theme_id is active (also applies saved value after mount).
  useEffect(() => {
    const theme = themes.find((t) => t.id === themeId) || (themeId === DEFAULT_THEME.id ? DEFAULT_THEME : themes[0] || DEFAULT_THEME)
    applyTheme(theme)
  }, [themeId, themes, applyTheme])

  const changeTheme = useCallback(
    async (newId) => {
      setThemeId(newId)
      try {
        await fetch(`${API}/api/themes/select`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Session-Id': sessionId },
          body: JSON.stringify({ theme_id: newId }),
        })
      } catch (e) {
        /* non-fatal */
      }
    },
    [sessionId],
  )

  const api = useMemo(
    () => async (path, opts = {}) => {
      const headers = { 'X-Session-Id': sessionId, ...(opts.headers || {}) }
      const res = await fetch(`${API}${path}`, { ...opts, headers })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        const err = new Error(data.detail || `HTTP ${res.status}`)
        err.status = res.status
        throw err
      }
      return res.json()
    },
    [sessionId],
  )

  const value = useMemo(
    () => ({ sessionId, api, themes, themeId, setThemeId: changeTheme, appliedTheme }),
    [sessionId, api, themes, themeId, changeTheme, appliedTheme],
  )

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export function useApp() {
  return useContext(AppContext)
}