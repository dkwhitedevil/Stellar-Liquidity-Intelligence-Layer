import React from 'react'

export default function CorridorSelector({from, to, setFrom, setTo}){
  return (
    <div className="flex gap-4">
      <input value={from} onChange={e=>setFrom(e.target.value)} placeholder="Source asset (e.g. USDC)" className="bg-gray-900 border border-gray-800 p-2 rounded w-full" />
      <input value={to} onChange={e=>setTo(e.target.value)} placeholder="Destination asset (e.g. XLM)" className="bg-gray-900 border border-gray-800 p-2 rounded w-full" />
    </div>
  )
}
