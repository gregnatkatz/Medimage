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
    <div className="w-[400px] h-[400px] rounded-xl overflow-hidden border-2 border-blue-500/30">
      <Canvas
        camera={{ position: [0, 0, 8], fov: 50 }}
        style={{ background: darkMode ? '#1a1a2e' : '#f0f4f8' }}
      >
        <ambientLight intensity={0.6} />
        <directionalLight position={[10, 10, 5]} intensity={1} />
        <directionalLight position={[-10, -10, -5]} intensity={0.5} />
        <pointLight position={[5, 5, 5]} intensity={0.5} color="#ffffff" />
        
        <LiverWithTumor />
        
        <OrbitControls 
          enablePan={false}
          enableZoom={true}
          enableRotate={true}
          autoRotate={false}
          minDistance={5}
          maxDistance={12}
        />
      </Canvas>
    </div>
  )
}
