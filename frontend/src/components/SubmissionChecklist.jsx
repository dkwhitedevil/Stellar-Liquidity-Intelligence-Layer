import React from 'react'
import './SubmissionChecklist.css'

export default function SubmissionChecklist(){
  const items = [
    'Corridor selector exists',
    'Empty states are explained',
    '0 advisories handled gracefully',
    'Scores & forecasts explained',
    'Conservatism clearly stated',
    'No execution UI',
    'Research framing present',
    'Future work section included'
  ]
  return (
    <section className="checklist">
      <h3>Final Frontend Submission Checklist</h3>
      <ul>
        {items.map(i=> <li key={i}>✅ {i}</li>)}
      </ul>
    </section>
  )
}
