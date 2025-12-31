import { useEffect, useState } from 'react'
import { getStabilityLatest, computeStability } from '../api/client'

export default function useStability(){
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const refresh = async ()=>{
    setLoading(true)
    setError(null)
    try{
      const res = await getStabilityLatest()
      setData(res.data.stability || [])
    }catch(err){
      setError(err.message || String(err))
    }finally{
      setLoading(false)
    }
  }

  const compute = async (window_size=6, window_minutes=5)=>{
    setLoading(true)
    setError(null)
    try{
      const res = await computeStability(window_size, window_minutes)
      // server returns the snapshot in res.data.stability
      setData(res.data.stability || [])
    }catch(err){
      setError(err.message || String(err))
    }finally{
      setLoading(false)
    }
  }

  useEffect(()=>{ refresh() }, [])

  return { data, loading, error, refresh, compute }
}
