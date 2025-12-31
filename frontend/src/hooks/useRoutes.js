import { useEffect, useState } from 'react'
import { getRecommendedRoutes } from '../api/client'

export default function useRoutes(){
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const refresh = async (from, to, max_hops=3, banned=null, min_liq=null)=>{
    setLoading(true)
    setError(null)
    try{
      const res = await getRecommendedRoutes(from, to, max_hops, banned, min_liq)
      setData(res.data || [])
    }catch(err){
      setError(err.message || String(err))
    }finally{
      setLoading(false)
    }
  }

  // no auto-run — require explicit corridor selection due to parameter needs
  useEffect(()=>{}, [])

  return { data, loading, error, refresh }
}
