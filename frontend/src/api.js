const API = import.meta.env.VITE_API_BASE || ''

export function getSessionId() {
  let id = localStorage.getItem('angi_session_id')
  if (!id) {
    id = `web-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`
    localStorage.setItem('angi_session_id', id)
  }
  return id
}

export async function api(path, opts = {}) {
  const headers = {
    'X-Session-Id': getSessionId(),
    ...(opts.headers || {}),
  }
  const res = await fetch(`${API}${path}`, { ...opts, headers })
  if (opts.raw) return res
  if (!res.ok) {
    const data = await res.json().catch(() => ({}))
    const err = new Error(data.detail || `HTTP ${res.status}`)
    err.status = res.status
    throw err
  }
  return res.json()
}