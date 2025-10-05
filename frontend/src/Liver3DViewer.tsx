import { useState } from 'react'
import { ZoomIn, ZoomOut, RotateCw, Maximize2 } from 'lucide-react'

interface Liver3DViewerProps {
  imageUrl: string
  darkMode: boolean
}

export default function Liver3DViewer({ imageUrl, darkMode }: Liver3DViewerProps) {
  const [zoom, setZoom] = useState(1)
  const [rotation, setRotation] = useState(0)
  const [pan, setPan] = useState({ x: 0, y: 0 })
  const [isDragging, setIsDragging] = useState(false)
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 })

  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault()
    const delta = e.deltaY > 0 ? 0.9 : 1.1
    setZoom(prev => Math.max(0.5, Math.min(3, prev * delta)))
  }

  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true)
    setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y })
  }

  const handleMouseMove = (e: React.MouseEvent) => {
    if (isDragging) {
      setPan({
        x: e.clientX - dragStart.x,
        y: e.clientY - dragStart.y
      })
    }
  }

  const handleMouseUp = () => {
    setIsDragging(false)
  }

  const resetView = () => {
    setZoom(1)
    setRotation(0)
    setPan({ x: 0, y: 0 })
  }

  return (
    <div className="w-full h-[500px] rounded-lg overflow-hidden border-2 border-blue-500/30 relative">
      <div 
        className={`w-full h-full flex items-center justify-center ${
          darkMode ? 'bg-[#1a1a2e]' : 'bg-[#f0f4f8]'
        }`}
        onWheel={handleWheel}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        style={{ cursor: isDragging ? 'grabbing' : 'grab' }}
      >
        <img
          src={imageUrl}
          alt="Liver Medical Imaging Scan"
          className="max-w-full max-h-full object-contain transition-transform duration-200 select-none"
          style={{
            transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom}) rotate(${rotation}deg)`,
            pointerEvents: 'none'
          }}
          draggable={false}
        />
      </div>
      
      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex gap-2 bg-black/50 backdrop-blur-sm rounded-lg p-2">
        <button
          onClick={() => setZoom(prev => Math.min(3, prev * 1.2))}
          className={`p-2 rounded transition-colors ${
            darkMode ? 'bg-blue-600 hover:bg-blue-700' : 'bg-blue-500 hover:bg-blue-600'
          } text-white`}
          title="Zoom In"
        >
          <ZoomIn className="w-4 h-4" />
        </button>
        <button
          onClick={() => setZoom(prev => Math.max(0.5, prev / 1.2))}
          className={`p-2 rounded transition-colors ${
            darkMode ? 'bg-blue-600 hover:bg-blue-700' : 'bg-blue-500 hover:bg-blue-600'
          } text-white`}
          title="Zoom Out"
        >
          <ZoomOut className="w-4 h-4" />
        </button>
        <button
          onClick={() => setRotation(prev => (prev + 90) % 360)}
          className={`p-2 rounded transition-colors ${
            darkMode ? 'bg-blue-600 hover:bg-blue-700' : 'bg-blue-500 hover:bg-blue-600'
          } text-white`}
          title="Rotate 90°"
        >
          <RotateCw className="w-4 h-4" />
        </button>
        <button
          onClick={resetView}
          className={`p-2 rounded transition-colors ${
            darkMode ? 'bg-blue-600 hover:bg-blue-700' : 'bg-blue-500 hover:bg-blue-600'
          } text-white`}
          title="Reset View"
        >
          <Maximize2 className="w-4 h-4" />
        </button>
      </div>

      <div className={`absolute top-4 left-4 text-sm ${
        darkMode ? 'text-gray-300' : 'text-gray-700'
      } bg-black/30 backdrop-blur-sm px-3 py-1 rounded`}>
        Drag to pan • Scroll to zoom • Click rotate
      </div>
    </div>
  )
}
