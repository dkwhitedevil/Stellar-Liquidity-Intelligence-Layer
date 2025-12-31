import React from 'react'
import MetricCard from './MetricCard'

export default function GraphSummary({summary}){
  if(!summary) return null
  return (
    <div className="grid grid-cols-3 gap-4">
      <MetricCard title="Graph Nodes" value={summary.nodes} />
      <MetricCard title="Graph Edges" value={summary.edges} />
      <MetricCard title="Last Snapshot" value={summary.timestamp || summary.snapshot} />
    </div>
  )
}
