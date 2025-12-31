import axios from 'axios'

const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8000' })

export const getScores = () => api.get('/scores')
export const getForecasts = () => api.get('/forecasts')
export const getAdvisories = (from, to) => api.get('/advisories', { params: { from, to } })
export const getGraphSummary = () => api.get('/graph/summary')
export const getGraphPaths = (from, to, max_hops = 3) => api.get('/graph/paths', { params: { from, to, max_hops } })

// Phase 6: recommended routes (supports banned list and min liquidity)
export const getRecommendedRoutes = (from, to, max_hops = 3, banned = null, min_liq = null) => {
  const params = { from, to, max_hops }
  if(banned) params.banned = Array.isArray(banned) ? banned.join(',') : banned
  if(min_liq !== null && min_liq !== undefined) params.min_liq = min_liq
  return api.get('/routes/recommend', { params })
}

// Stability endpoints
export const getStabilityLatest = () => api.get('/stability/latest')
export const computeStability = (window_size = 6, window_minutes = 5) => api.get('/stability/compute', { params: { window_size, window_minutes } })

export default api
