import React, { useState } from 'react'
import EmptyState from './EmptyState'
import useStability from '../hooks/useStability'

export default function StabilityView(){
  const { data, loading, error, refresh, compute } = useStability()
  const [windowSize, setWindowSize] = useState(6)
  const [windowMinutes, setWindowMinutes] = useState(5)

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <label className="text-sm text-gray-400">Window size</label>
          <input type="number" min={1} value={windowSize} onChange={e=>setWindowSize(Number(e.target.value))} className="w-20 p-1 bg-gray-800 border border-gray-700 rounded" />
          <label className="text-sm text-gray-400">Window minutes</label>
          <input type="number" min={1} value={windowMinutes} onChange={e=>setWindowMinutes(Number(e.target.value))} className="w-20 p-1 bg-gray-800 border border-gray-700 rounded" />
          <button onClick={()=>compute(windowSize, windowMinutes)} className="ml-3 px-3 py-1 bg-blue-600 rounded">Compute</button>
        </div>
        <div>
          <button onClick={refresh} className="px-3 py-1 bg-gray-700 rounded">Refresh</button>
        </div>
      </div>

      {loading && <div className="text-gray-400">Loading stability metrics…</div>}
      {error && <div className="text-red-400">{error}</div>}

      {!loading && !error && (!data || data.length===0) && (
        <EmptyState message="No stability data available. Try computing." />
      )}

      {!loading && data && data.length>0 && (
        <div className="grid grid-cols-1 gap-3">
          {data.map((r,i)=> (
            <div key={i} className="bg-gray-900 p-3 rounded border border-gray-800">
              <div className="flex justify-between items-center">
                <div>
                  <div className="font-semibold">{r.entity} — {r.metric}</div>
                  <div className="text-xs text-gray-400">Sample count: {r.sample_count} | Trend: {r.trend.toFixed(3)}</div>
                </div>
                <div className="text-sm">
                  <div className="text-xs text-gray-400">Stability</div>
                  <div className="font-bold">{(r.stability_index != null) ? r.stability_index.toFixed(3) : '—'}</div>
                </div>
              </div>
              <div className="mt-2 text-xs text-gray-400">Variability: {r.variability.toFixed(4)}</div>
              <div className="mt-2 text-sm text-gray-500">{r.explanation}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
