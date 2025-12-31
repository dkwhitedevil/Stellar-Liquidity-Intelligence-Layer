import React from 'react'
import MetricCard from './MetricCard'
import EmptyState from './EmptyState'

export default function ForecastView({forecasts}){
  if(!forecasts || forecasts.length===0) return <EmptyState message="No forecasts available. Insufficient historical data." />
  return (
    <div className="grid grid-cols-2 gap-4">
      {forecasts.map((f,i)=> (
        <MetricCard key={i} title={`${f.entity} — ${f.metric}`} value={Math.round(f.expected || f.value)} subtitle={`Uncertainty ±${Math.round(f.uncertainty || 0)}`} />
      ))}
    </div>
  )
}
