import React from 'react'
import './CorridorSelector.css'

const ASSETS = [
  'XLM', 'USDC', 'EUR', 'BTC', 'ETH'
]

export default function CorridorSelector({corridor, setCorridor}){
  return (
    <section className="corridor">
      <h3>Corridor Selection</h3>
      <p className="explain"><strong>These inputs define the corridor for analysis only. No transactions are executed. SLIL provides intelligence, not action.</strong></p>
      <div className="inputs">
        <label>Source asset
          <select value={corridor.source} onChange={e=>setCorridor(c=>({...c,source:e.target.value}))}>
            <option value="">-- select --</option>
            {ASSETS.map(a=> <option key={a} value={a}>{a}</option>)}
          </select>
        </label>
        <label>Destination asset
          <select value={corridor.dest} onChange={e=>setCorridor(c=>({...c,dest:e.target.value}))}>
            <option value="">-- select --</option>
            {ASSETS.map(a=> <option key={a} value={a}>{a}</option>)}
          </select>
        </label>
        <label>Time horizon (optional)
          <select value={corridor.horizon} onChange={e=>setCorridor(c=>({...c,horizon:e.target.value}))}>
            <option value="short">Short-term</option>
            <option value="next">Next window</option>
          </select>
        </label>

        <label>Risk sensitivity
          <select value={corridor.risk} onChange={e=>setCorridor(c=>({...c,risk:e.target.value}))}>
            <option>Low</option>
            <option>Medium</option>
            <option>High</option>
          </select>
        </label>
      </div>

      <div className="helpers">
        {(!corridor.source || !corridor.dest) && <div className="helper">Select both source and destination assets to fetch corridor intelligence.</div>}
        {corridor.source && corridor.dest && corridor.source === corridor.dest && <div className="helper error">Source and destination must be different.</div>}
        <div className="actions">
          <button onClick={()=>setCorridor({source:'XLM', dest:'USDC', horizon:'short', risk:'Medium'})}>Load demo corridor (XLM → USDC)</button>
        </div>
      </div>
    </section>
  )
}
