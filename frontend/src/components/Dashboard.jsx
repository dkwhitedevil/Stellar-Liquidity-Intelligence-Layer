import React from 'react'
import './Dashboard.css'

function ScoreCard({title, value, note}){
  return (
    <div className="score-card">
      <div className="score-title">{title}</div>
      <div className="score-value">{value}</div>
      <div className="score-note">{note}</div>
    </div>
  )
}

function ForecastCard({metric, value, range}){
  return (
    <div className="forecast-card">
      <div className="metric">{metric}</div>
      <div className="value">{value}</div>
      <div className="range">Uncertainty: {range}</div>
    </div>
  )
}

function RoutingSection({advisories}){
  if(!advisories || advisories.length===0){
    return (
      <div className="routing-empty">
        <strong>No route advisories generated.</strong>
        <p>Current forecast evidence is insufficient to responsibly advise on this corridor. The system remains conservative by design.</p>
      </div>
    )
  }
  return (
    <div className="routing-list">
      {advisories.map((a,i)=> (
        <div className="routing-item" key={i}>
          <div className="candidate">Candidate {i+1}</div>
          <div className="score">Score: {a.score} | Risk: {a.risk}</div>
          <div className="explain">{a.explain}</div>
        </div>
      ))}
    </div>
  )
}

import useCorridorData from '../hooks/useCorridorData'
import RoutesView from './RoutesView'

export default function Dashboard({corridor, setGraphInfo}){
  const {data, loading, error} = useCorridorData(corridor)

  const reliability = data && data.reliability !== null ? data.reliability : '—'
  const stability = data && data.stability !== null ? data.stability : '—'
  const forecasts = data && data.forecasts ? data.forecasts : []
  const advisories = data && data.advisories ? data.advisories : []

  // propagate graph info up to App
  React.useEffect(()=>{
    if(setGraphInfo){
      setGraphInfo(data && data.graph ? data.graph : null)
    }
  }, [data, setGraphInfo])

  return (
    <section className="dashboard">
      <h2>System State Dashboard</h2>

      {error && <div className="panel error">API error: {error}</div>}

      <div className="dashboard-grid">
        <div className="panel">
          <h3>Reliability & Stability</h3>
          <div className="cards">
            <ScoreCard title="Reliability" value={loading? 'loading...' : reliability} note="Scores are retrospective and bounded. A value of 0.5 indicates neutral confidence due to limited data." />
            <ScoreCard title="Stability" value={loading? 'loading...' : stability} note="Scores are retrospective and bounded. A value of 0.5 indicates neutral confidence due to limited data." />
          </div>
        </div>

        <div className="panel">
          <h3>Forecasts & Risk</h3>
          <div className="forecasts">
            {loading && <div className="forecast-note">Loading forecasts…</div>}
            {!loading && forecasts.length===0 && <div className="forecast-note">Forecasts are generated only when sufficient historical data exists. No forecast is produced otherwise.</div>}
            {forecasts.map((f,i)=>(
              <ForecastCard key={i} metric={f.metric} value={f.expected || f.value} range={f.uncertainty || f.range} />
            ))}
          </div>
        </div>

        <div className="panel">
          <h3>Routing Advisories</h3>
          {loading ? <div className="routing-empty">Loading advisories…</div> : <RoutingSection advisories={advisories}/>}        
        </div>

        <div className="panel">
          <h3>Recommended Routes</h3>
          <RoutesView from={corridor && corridor.source} to={corridor && corridor.dest} />
        </div>
      </div>
    </section>
  )
}
