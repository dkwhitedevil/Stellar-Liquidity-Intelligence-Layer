import React from 'react'
import './Limitations.css'

export default function Limitations(){
  return (
    <section className="limitations">
      <h3>Design Limitations & Conservatism</h3>
      <div className="box">
        <ul>
          <li>SLIL does not execute transactions</li>
          <li>SLIL may output neutral scores (0.5)</li>
          <li>SLIL may output zero advisories</li>
          <li>SLIL prioritizes correctness over coverage</li>
        </ul>
        <p className="em">Absence of output is treated as information, not failure.</p>
      </div>
    </section>
  )
}
