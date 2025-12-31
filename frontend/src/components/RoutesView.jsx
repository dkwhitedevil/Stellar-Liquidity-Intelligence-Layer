import React from 'react'
import useRoutes from '../hooks/useRoutes'

export default function RoutesView({from, to}){
  const {data, loading, error, refresh} = useRoutes()

  React.useEffect(()=>{
    if(from && to){
      refresh(from, to)
    }
  }, [from, to])

  if(!from || !to){
    return <div className="panel">Specify both source and destination to get route recommendations.</div>
  }

  if(loading) return <div className="panel">Loading route recommendations…</div>
  if(error) return <div className="panel error">Error: {error}</div>

  if(!data || data.length===0){
    return <div className="panel">No route recommendations available for the selected corridor.</div>
  }

  return (
    <div className="panel">
      <h4>Recommended Routes</h4>
      <div className="routes-list">
        {data.map((r,i)=> (
          <div className="route-item" key={i}>
            <div className="route-rank">#{i+1} — Score: {r.score.toFixed ? r.score.toFixed(2) : r.score}</div>
            <div className="route-path">Path: {r.path.join(' → ')}</div>
            <div className="route-meta">Risk: {r.risk} | Edge penalty: {r.edge_penalty}</div>
            <div className="route-explain">{r.explanation}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
