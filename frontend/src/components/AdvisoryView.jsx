import React from 'react'
import EmptyState from './EmptyState'

export default function AdvisoryView({advisories}){
  if(!advisories || advisories.length===0) return <EmptyState message="No route advisories generated. System remains conservative." />
  return (
    <div className="space-y-4">
      {advisories.map((a,i)=> (
        <div key={i} className="bg-gray-900 p-4 rounded border border-gray-800">
          <div className="flex items-center justify-between">
            <div className="font-semibold">{a.source} → {a.destination}</div>
            <div className="text-sm text-gray-400">Score: {(a.score != null) ? a.score.toFixed(2) : '—'}</div>
          </div>

          <div className="mt-2 flex items-center space-x-3">
            <div className="text-xs text-gray-400">Risk:</div>
            <div className="px-2 py-1 rounded-full text-xs font-medium" style={{backgroundColor: a.risk > 0.5 ? '#7f1d1d' : '#065f46'}}>{(a.risk != null) ? a.risk : '—'}</div>
          </div>

          {a.path && Array.isArray(a.path) && (
            <div className="flex flex-wrap gap-2 mt-3">
              {a.path.map((hop, idx)=> (
                <div key={idx} className="px-2 py-1 bg-gray-800 border border-gray-700 rounded-full text-sm">{hop}</div>
              ))}
            </div>
          )}

          {a.explanation || a.explain ? (
            <div className="text-xs text-gray-500 mt-3">{a.explanation || a.explain}</div>
          ) : null}
        </div>
      ))}
    </div>
  )
}
