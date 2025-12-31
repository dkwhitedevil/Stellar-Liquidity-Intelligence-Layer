const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function fetchCorridor(source, dest){
  if(!source || !dest) return null
  const url = new URL('/api/corridor', API_BASE)
  url.searchParams.set('source', source)
  url.searchParams.set('dest', dest)
  const res = await fetch(url.toString())
  if(!res.ok) throw new Error(`API ${res.status}`)
  return res.json()
}
