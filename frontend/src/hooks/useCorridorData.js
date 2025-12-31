import { useEffect, useState, useRef } from 'react'
import { fetchCorridor } from '../services/api'

export default function useCorridorData(corridor){
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const abortRef = useRef(null)

  useEffect(()=>{
    if(!corridor || !corridor.source || !corridor.dest || corridor.source === corridor.dest){
      setData(null)
      setLoading(false)
      setError(null)
      return
    }

    let cancelled = false
    setLoading(true)
    setError(null)

    (async ()=>{
      try{
        const res = await fetchCorridor(corridor.source, corridor.dest)
        if(cancelled) return
        setData(res)
      }catch(err){
        if(cancelled) return
        setError(err.message || String(err))
        setData(null)
      }finally{
        if(cancelled) return
        setLoading(false)
      }
    })()

    return ()=>{ cancelled = true }
  }, [corridor && corridor.source, corridor && corridor.dest])

  return {data, loading, error}
}
