import React from 'react'
import './GraphTransparency.css'

export default function GraphTransparency({graphInfo}){
  const info = graphInfo || {nodes: 0, edges: 0, snapshot: null}
  return (
    <section className="graph-transparency">
      <h3>Graph & Data Transparency</h3>
      <div className="meta">
        <div>Nodes: <strong>{info.nodes}</strong></div>
        <div>Edges: <strong>{info.edges}</strong></div>
        <div>Last snapshot: <strong>{info.snapshot || 'none'}</strong></div>
      </div>
      <p className="explain">The economic signal graph encodes structure only. It contains no routing logic, weights, or optimization.</p>
    </section>
  )
}
