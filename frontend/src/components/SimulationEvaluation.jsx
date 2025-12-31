import React from 'react'
import './SimulationEvaluation.css'

export default function SimulationEvaluation(){
  return (
    <section className="simulation">
      <h3>Simulation & Evaluation</h3>
      <p><strong>SLIL is evaluated using counterfactual simulation. We compare baseline Stellar behavior with SLIL-assisted advisory logic under identical historical conditions.</strong></p>
      <ul>
        <li>Reduced path failure (simulated)</li>
        <li>Improved stability under volatility</li>
        <li>No protocol changes required</li>
      </ul>
      <p className="note">Evaluation is framed transparently; where results are simulated they are clearly labeled as such in the UI.</p>
    </section>
  )
}
