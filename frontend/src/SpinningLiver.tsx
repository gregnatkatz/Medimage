import { useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import * as THREE from 'three'

interface SpinningLiverProps {
  darkMode: boolean
}

function LiverWithTumor() {
  const liverRef = useRef<THREE.Mesh>(null)
  const tumorRef = useRef<THREE.Mesh>(null)
  
  useFrame((_, delta) => {
    if (liverRef.current) {
      liverRef.current.rotation.y += delta * 0.5
    }
    if (tumorRef.current) {
      tumorRef.current.rotation.y += delta * 0.5
      const scale = 1 + Math.sin(Date.now() * 0.003) * 0.1
      tumorRef.current.scale.set(scale, scale, scale)
    }
  })

  return (
    <group>
      <mesh ref={liverRef} position={[0, 0, 0]}>
        <sphereGeometry args={[2, 32, 32]} />
        <meshStandardMaterial 
          color="#8B4513"
          roughness={0.7}
          metalness={0.2}
          transparent
          opacity={0.8}
        />
      </mesh>
      
      <mesh ref={tumorRef} position={[1.2, 0.5, 0.8]}>
        <sphereGeometry args={[0.4, 16, 16]} />
        <meshStandardMaterial 
          color="#FF0000"
          emissive="#FF3333"
          emissiveIntensity={0.5}
          roughness={0.4}
          metalness={0.3}
        />
      </mesh>

      <mesh position={[1.2, 0.5, 0.8]}>
        <sphereGeometry args={[0.5, 16, 16]} />
        <meshBasicMaterial 
          color="#FF6666"
          transparent
          opacity={0.2}
        />
      </mesh>
    </group>
  )
}

export default function SpinningLiver({ darkMode }: SpinningLiverProps) {
  return (
    <div className="w-[700px] h-[700px] rounded-xl overflow-hidden border-4 border-blue-500/40 shadow-2xl">
      <Canvas
        camera={{ position: [0, 0, 8], fov: 50 }}
        style={{ background: darkMode ? '#0f172a' : '#dbeafe' }}
      >
        <ambientLight intensity={0.7} />
        <directionalLight position={[10, 10, 5]} intensity={1.2} />
        <directionalLight position={[-10, -10, -5]} intensity={0.6} />
        <pointLight position={[5, 5, 5]} intensity={0.7} color="#60a5fa" />
        <pointLight position={[-5, -5, -5]} intensity={0.4} color="#3b82f6" />
        
        <LiverWithTumor />
        
        <OrbitControls 
          enablePan={false}
          enableZoom={true}
          enableRotate={true}
          autoRotate={true}
          autoRotateSpeed={2}
          minDistance={5}
          maxDistance={12}
        />
      </Canvas>
    </div>
  )
}
