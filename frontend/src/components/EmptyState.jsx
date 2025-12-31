import React from 'react'

export default function EmptyState({message}){
  return (
    <div className="border border-dashed border-gray-700 p-6 rounded text-gray-400 text-center">
      {message}
    </div>
  )
}
