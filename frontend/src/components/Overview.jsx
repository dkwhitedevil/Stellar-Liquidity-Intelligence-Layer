import React from 'react'
import './Overview.css'
import SubmissionChecklist from './SubmissionChecklist'

export default function Overview(){
  return (
    <section className="overview">
      <h2>Project Overview</h2>
      <p className="lead"> <strong>SLIL is a read-only intelligence layer built on top of Stellar.
      It observes real network data, extracts economic signals, structures them into a time-aware graph, computes reliability and stability metrics, forecasts uncertainty-aware risk, and produces non-executing routing advisories — without modifying Stellar Core or submitting transactions.</strong></p>

      <div className="phase-diagram">
        <strong>Phase diagram:</strong>
        <div className="diagram">Observe → Measure → Structure → Interpret → Forecast → Advise</div>
      </div>

      <p className="note">This frontend presents research-grade transparency, clear empty states, and conservative advisory logic. It produces intelligence only — no execution UI is provided.</p>

      <SubmissionChecklist />
    </section>
  )
}
