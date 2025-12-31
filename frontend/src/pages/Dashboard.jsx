import React, {useEffect, useState} from 'react'
import Section from '../components/Section'
import CorridorSelector from '../components/CorridorSelectorSimple'
import ScoresView from '../components/ScoresView'
import ForecastView from '../components/ForecastView'
import AdvisoryView from '../components/AdvisoryView'
import GraphSummary from '../components/GraphSummary'
import StabilityView from '../components/StabilityView'
import { getScores, getForecasts, getAdvisories, getGraphSummary, getGraphPaths } from '../api/client'

export default function Dashboard(){
  const [from, setFrom] = useState('USDC')
  const [to, setTo] = useState('XLM')

  const [scores, setScores] = useState([])
  const [forecasts, setForecasts] = useState([])
  const [advisories, setAdvisories] = useState([])
  const [paths, setPaths] = useState([])
  const [pathsLoading, setPathsLoading] = useState(false)
  const [graph, setGraph] = useState(null)

  useEffect(()=>{
    getScores().then(r=>setScores(r.data)).catch(()=>setScores([]))
    getForecasts().then(r=>setForecasts(r.data)).catch(()=>setForecasts([]))
    getGraphSummary().then(r=>setGraph(r.data)).catch(()=>setGraph(null))
  },[])

  useEffect(()=>{
    if(!from || !to) return setAdvisories([])
    getAdvisories(from, to).then(r=>setAdvisories(r.data)).catch(()=>setAdvisories([]))
  },[from,to])

  useEffect(()=>{
    // Fetch candidate paths using the new /graph/paths endpoint
    let cancelled = false
    if(!from || !to){ setPaths([]); return }
    setPathsLoading(true)
    setPaths([])

    getGraphPaths(from, to).then(r=>{
      if(cancelled) return
      setPaths(r.data)
    }).catch(()=>{
      if(cancelled) return
      setPaths([])
    }).finally(()=>{
      if(cancelled) return
      setPathsLoading(false)
    })

    return ()=>{ cancelled = true }
  },[from,to])

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-10">
      <Section title="Corridor Selection">
        <CorridorSelector from={from} to={to} setFrom={setFrom} setTo={setTo} />
      </Section>

      <Section title="Reliability & Stability">
        <ScoresView scores={scores} />
      </Section>

      <Section title="Forecasts & Risk">
        <ForecastView forecasts={forecasts} />
      </Section>

      <Section title="Routing Advisories">
        <AdvisoryView advisories={advisories} />
      </Section>

      <Section title="Candidate Paths">
        {pathsLoading ? <div className="text-gray-400">Loading candidate paths…</div> : <AdvisoryView advisories={paths} />}
        {!pathsLoading && paths && paths.length===0 && <div className="text-sm text-gray-500 mt-2">No candidate paths found for this corridor.</div>}
      </Section>

      <Section title="Economic Signal Graph">
        <GraphSummary summary={graph} />
      </Section>

      <Section title="Stability Metrics">
        <StabilityView />
      </Section>
    </div>
  )
}
