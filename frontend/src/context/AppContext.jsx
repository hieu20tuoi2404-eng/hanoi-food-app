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

const AppContext = createContext({
  sessionId: '',
  api: null,
  themes: [],
  themeId: '',
  setThemeId: () => {},
  appliedTheme: DEFAULT_THEME,
  mascots: [],
  mascotId: null,
  mascot: null,
  mascotReady: false,
  setMascotId: () => {},
  clearMascot: () => {},
  pickerSeen: false,
  openMascotPicker: () => {},
  closeMascotPicker: () => {},
  animationsEnabled: true,
  toggleAnimations: () => {},
})

export function AppProvider({ children }) {
  const [sessionId] = useState(getSessionId)
  const [themes, setThemes] = useState([])
  const [themeId, setThemeId] = useState(DEFAULT_THEME.id)
  const [appliedTheme, setAppliedTheme] = useState(DEFAULT_THEME)
  const [mascots, setMascots] = useState([])
  const [mascotId, setMascotIdState] = useState(() => localStorage.getItem('angi_mascot_id'))
  const [mascotReady, setMascotReady] = useState(false)
  const [pickerSeen, setPickerSeen] = useState(() => localStorage.getItem('angi_mascot_picker_seen') === '1')
  const [animationsEnabled, setAnimationsEnabled] = useState(
    () => localStorage.getItem('angi_animations') !== '0',
  )

  // Reflect animation preference on <html> so CSS can toggle.
  useEffect(() => {
    document.documentElement.dataset.animations = animationsEnabled ? 'on' : 'off'
  }, [animationsEnabled])

  const toggleAnimations = useCallback(() => {
    setAnimationsEnabled((prev) => {
      const next = !prev
      localStorage.setItem('angi_animations', next ? '1' : '0')
      return next
    })
  }, [])

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
    root.dataset.mascot = theme.mascot || theme.mascot_id || 'default'
    root.dataset.theme = theme.id || 'default'
    setAppliedTheme(theme)
  }, [])

  // Load themes + the user's saved theme + mascots + user mascot on mount.
  useEffect(() => {
    let cancelled = false
    ;(async () => {
      try {
        const [themesRes, selRes, mascotsRes, userMascotRes] = await Promise.all([
          fetch(`${API}/api/themes`),
          fetch(`${API}/api/themes/selection`, { headers: { 'X-Session-Id': sessionId } }),
          fetch(`${API}/api/mascots`),
          fetch(`${API}/api/user/mascot`, { headers: { 'X-Session-Id': sessionId } }),
        ])
        if (themesRes.ok) {
          const list = await themesRes.json()
          if (!cancelled) setThemes(list)
        }
        if (selRes.ok && !cancelled) {
          const sel = await selRes.json()
          if (sel.theme_id) setThemeId(sel.theme_id)
        }
        if (mascotsRes.ok) {
          const list = await mascotsRes.json()
          if (!cancelled) setMascots(list)
        }
        if (userMascotRes.ok) {
          const sel = await userMascotRes.json()
          if (!cancelled && sel.mascot_id) {
            setMascotIdState(sel.mascot_id)
            localStorage.setItem('angi_mascot_id', sel.mascot_id)
          }
        }
      } catch (e) {
        /* offline: keep defaults */
      } finally {
        if (!cancelled) setMascotReady(true)
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

  const setMascotId = useCallback(
    async (newId) => {
      setMascotIdState(newId)
      if (newId) localStorage.setItem('angi_mascot_id', newId)
      else localStorage.removeItem('angi_mascot_id')
      try {
        await api(newId ? '/api/user/mascot' : '/api/user/mascot', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newId ? { mascot_id: newId } : { mascot_id: null }),
        })
      } catch (e) {
        /* non-fatal — local choice kept */
      }
    },
    [api],
  )

  const clearMascot = useCallback(async () => {
    setMascotIdState(null)
    localStorage.removeItem('angi_mascot_id')
    try {
      await api('/api/user/mascot', { method: 'DELETE' })
    } catch (e) {
      /* non-fatal */
    }
  }, [api])

  const openMascotPicker = useCallback(() => {
    setPickerSeen(false)
  }, [])

  const closeMascotPicker = useCallback(() => {
    setPickerSeen(true)
    localStorage.setItem('angi_mascot_picker_seen', '1')
  }, [])

  const mascot = useMemo(
    () => (mascotId ? mascots.find((m) => m.id === mascotId) || null : null),
    [mascotId, mascots],
  )

  const value = useMemo(
    () => ({
      sessionId,
      api,
      themes,
      themeId,
      setThemeId: changeTheme,
      appliedTheme,
      mascots,
      mascotId,
      mascot,
      mascotReady,
      setMascotId,
      clearMascot,
      pickerSeen,
      openMascotPicker,
      closeMascotPicker,
      animationsEnabled,
      toggleAnimations,
    }),
    [
      sessionId, api, themes, themeId, changeTheme, appliedTheme,
      mascots, mascotId, mascot, mascotReady, setMascotId, clearMascot,
      pickerSeen, openMascotPicker, closeMascotPicker,
      animationsEnabled, toggleAnimations,
    ],
  )

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export function useApp() {
  return useContext(AppContext)
}