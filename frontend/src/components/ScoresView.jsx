import React from 'react'
import MetricCard from './MetricCard'

export default function ScoresView({scores}){
  if(!scores || scores.length===0) return <MetricCard title="Scores" value="No data" />
  return (
    <div className="grid grid-cols-2 gap-4">
      {scores.map((s,i)=> (
        <MetricCard key={i} title={`${s.entity} — ${s.score_type}`} value={s.value.toFixed(2)} subtitle={s.explanation} />
      ))}
    </div>
  )
}
