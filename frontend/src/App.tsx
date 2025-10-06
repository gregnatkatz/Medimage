import { useState, useRef, useEffect } from 'react'
import { 
  Upload, Activity, Brain, Microscope, Moon, Sun, 
  FileImage, CheckCircle2, Loader2, Zap
} from 'lucide-react'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Progress } from '@/components/ui/progress'
import Liver3DViewer from './Liver3DViewer'
import LandingPage from './LandingPage'
import AnalyticsDashboard from './AnalyticsDashboard'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

type Page = 'landing' | 'analysis' | 'dashboard'

function DemoField({ label, value, darkMode }: { label: string; value: string; darkMode: boolean }) {
  return (
    <div>
      <p className={`text-sm mb-1 ${darkMode ? 'text-gray-400' : 'text-slate-600'}`}>
        {label}
      </p>
      <p className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-slate-900'}`}>
        {value}
      </p>
    </div>
  )
}

interface AnalysisResult {
  embeddings: {
    confidence: number
    classification: string
    features: string[]
  }
  segmentation: {
    detected: string[]
    area: string
    severity: string
  }
  gpt5Analysis: string
  metrics: {
    processingTime: string
    accuracy: string
    modelsUsed: number
  }
  demographics?: {
    patient_id: string
    name?: string
    age: number
    gender: string
    ethnicity: string
    study_date: string
    medical_background?: string
  }
}

function App() {
  const [darkMode, setDarkMode] = useState(true)
  const [currentPage, setCurrentPage] = useState<Page>('landing')
  const [selectedModality, setSelectedModality] = useState('liver-mri')
  const [uploadedImage, setUploadedImage] = useState<string | null>(null)
  const [demoPatientData, setDemoPatientData] = useState<AnalysisResult['demographics'] | null>(null)
  const [processing, setProcessing] = useState(false)
  const [analysisStep, setAnalysisStep] = useState(0)
  const [results, setResults] = useState<AnalysisResult | null>(null)
  const [activeTab, setActiveTab] = useState('upload')
  const [useMockData, setUseMockData] = useState(true)
  const [availablePatients, setAvailablePatients] = useState<Array<{patient_id: string, name: string, age: number, gender: string, medical_background: string}>>([])
  const [selectedPatientId, setSelectedPatientId] = useState<string>('')
  const [loadingPatients, setLoadingPatients] = useState(false)
  const ensureDataUrlPrefix = (url: string | null): string | null => {
    if (!url) return null
    if (url.startsWith('data:')) return url
    if (url.startsWith('base64,')) return `data:image/png;${url}`
    if (url.match(/^[a-zA-Z0-9+/=]+$/)) return `data:image/png;base64,${url}`
    return url
  }

  const safeUploadedImage = ensureDataUrlPrefix(uploadedImage)

  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    fetch(`${API_URL}/api/config`)
      .then(res => res.json())
      .then(data => setUseMockData(data.useMockData))
      .catch(err => console.error('Config fetch error:', err))
  }, [])

  useEffect(() => {
    const fetchPatients = async () => {
      if (!['liver-mri', 'liver-ct', 'ultrasound'].includes(selectedModality)) {
        setAvailablePatients([])
        setSelectedPatientId('')
        return
      }
      
      setLoadingPatients(true)
      try {
        const response = await fetch(`${API_URL}/api/patients?modality=${selectedModality}`)
        const data = await response.json()
        if (data.success) {
          setAvailablePatients(data.patients)
          setSelectedPatientId('')
        }
      } catch (error) {
        console.error('Failed to fetch patients:', error)
        setAvailablePatients([])
      } finally {
        setLoadingPatients(false)
      }
    }
    
    fetchPatients()
  }, [selectedModality])

  if (currentPage === 'landing') {
    return <LandingPage darkMode={darkMode} onEnter={() => setCurrentPage('analysis')} />
  }

  if (currentPage === 'dashboard') {
    return <AnalyticsDashboard darkMode={darkMode} onNavigate={setCurrentPage} />
  }

  const modalities = [
    { id: 'liver-mri', name: 'Liver MRI', icon: Brain },
    { id: 'liver-ct', name: 'Liver CT', icon: Activity },
    { id: 'ultrasound', name: 'Ultrasound', icon: Zap },
    { id: 'pathology', name: 'Pathology', icon: Microscope }
  ]

  const analysisSteps = [
    { name: 'Image Upload', status: 'complete' },
    { name: 'Liver Feature Detection', status: analysisStep >= 1 ? 'complete' : 'pending' },
    { name: 'Tumor Segmentation', status: analysisStep >= 2 ? 'complete' : 'pending' },
    { name: 'Clinical Analysis', status: analysisStep >= 3 ? 'complete' : 'pending' }
  ]

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        setUploadedImage(e.target?.result as string)
        setDemoPatientData(null)
        setResults(null)
        setActiveTab('analyze')
      }
      reader.readAsDataURL(file)
    }
  }

  const loadDemoImage = async () => {
    try {
      const formData = new FormData()
      formData.append('modality', selectedModality)
      if (selectedPatientId) {
        formData.append('patient_id', selectedPatientId)
      }
      
      const response = await fetch(`${API_URL}/api/upload-demo`, {
        method: 'POST',
        body: formData
      })
      
      const data = await response.json()
      console.log('Backend returned imageUrl:', data.imageUrl?.substring(0, 100))
      if (data.success) {
        setUploadedImage(data.imageUrl)
        setDemoPatientData(data.patientData || null)
        setResults(null)
        setActiveTab('analyze')
      }
    } catch (error) {
      console.error('Demo load error:', error)
    }
  }

  const dataURLtoBlob = (dataURL: string): Blob => {
    const parts = dataURL.split(',')
    const byteString = atob(parts[1])
    const mimeString = parts[0].split(':')[1].split(';')[0]
    const ab = new ArrayBuffer(byteString.length)
    const ia = new Uint8Array(ab)
    for (let i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i)
    }
    return new Blob([ab], { type: mimeString })
  }

  const runAnalysis = async () => {
    if (!uploadedImage) return
    
    setProcessing(true)
    setAnalysisStep(0)
    setActiveTab('results')

    try {
      const blob = dataURLtoBlob(safeUploadedImage!)
      
      const formData = new FormData()
      formData.append('image', blob, 'image.png')
      formData.append('modality', selectedModality)

      for (let step = 1; step <= 3; step++) {
        setAnalysisStep(step)
        await new Promise(resolve => setTimeout(resolve, 800))
      }

      const analysisResponse = await fetch(`${API_URL}/api/analyze`, {
        method: 'POST',
        body: formData
      })

      if (!analysisResponse.ok) {
        throw new Error('Analysis failed')
      }

      const result = await analysisResponse.json()
      setResults(result.data)
      setAnalysisStep(4)
    } catch (error) {
      console.error('Analysis error:', error)
      alert('Error processing image. Please try again.')
    } finally {
      setProcessing(false)
    }
  }

  return (
    <div className={`min-h-screen transition-colors duration-300 ${darkMode ? 'bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900' : 'bg-gradient-to-br from-blue-50 via-white to-slate-50'}`}>
      <nav className={`border-b ${darkMode ? 'border-slate-700 bg-slate-800/50' : 'border-gray-200 bg-white/50'} backdrop-blur-sm`}>
        <div className="container mx-auto px-4 py-4 flex gap-4 items-center justify-between">
          <div className="flex gap-4">
            <button
              onClick={() => setCurrentPage('landing')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                darkMode ? 'hover:bg-slate-700 text-gray-300' : 'hover:bg-gray-100 text-slate-700'
              }`}
            >
              Home
            </button>
            <button
              className={`px-4 py-2 rounded-lg ${
                darkMode ? 'bg-blue-600 text-white' : 'bg-blue-500 text-white'
              }`}
            >
              Analysis
            </button>
            <button
              onClick={() => setCurrentPage('dashboard')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                darkMode ? 'hover:bg-slate-700 text-gray-300' : 'hover:bg-gray-100 text-slate-700'
              }`}
            >
              Dashboard
            </button>
          </div>
          <Button
            variant="outline"
            size="icon"
            onClick={() => setDarkMode(!darkMode)}
            className={darkMode ? 'border-blue-400 text-blue-400 hover:bg-blue-900/30' : 'border-blue-600 text-blue-600 hover:bg-blue-50'}
          >
            {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </Button>
        </div>
      </nav>
      
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className={`text-4xl font-bold ${darkMode ? 'text-white' : 'text-slate-900'}`}>
            Liver Disease Imaging AI Platform
          </h1>
          <p className={`text-lg mt-2 ${darkMode ? 'text-blue-300' : 'text-blue-600'}`}>
            Powered by Azure AI Foundry and Microsoft Healthcare AI Models
          </p>
          <p className={`text-sm mt-1 ${darkMode ? 'text-gray-400' : 'text-slate-600'}`}>
            Mode: {useMockData ? 'Demo (Mock Data)' : 'Production (Azure AI)'}
          </p>
        </div>

        <Alert className={`mb-6 ${darkMode ? 'bg-blue-900/30 border-blue-500' : 'bg-blue-50 border-blue-300'}`}>
          <Brain className={`h-4 w-4 ${darkMode ? 'text-blue-400' : 'text-blue-600'}`} />
          <AlertDescription className={darkMode ? 'text-blue-200' : 'text-blue-800'}>
            This healthcare AI platform is for research and demonstration purposes only. 
            Not intended for clinical use without proper regulatory approval.
          </AlertDescription>
        </Alert>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-8">
          {modalities.map((modality) => (
            <Card
              key={modality.id}
              className={`cursor-pointer transition-all ${
                selectedModality === modality.id
                  ? darkMode
                    ? 'bg-blue-900/50 border-blue-500 shadow-lg shadow-blue-500/50'
                    : 'bg-blue-100 border-blue-500 shadow-lg'
                  : darkMode
                  ? 'bg-slate-800/50 border-slate-700 hover:bg-slate-800/80'
                  : 'bg-white border-slate-200 hover:bg-slate-50'
              }`}
              onClick={() => setSelectedModality(modality.id)}
            >
              <CardHeader className="text-center pb-4">
                <modality.icon className={`h-8 w-8 mx-auto mb-2 ${
                  selectedModality === modality.id
                    ? darkMode ? 'text-blue-400' : 'text-blue-600'
                    : darkMode ? 'text-gray-400' : 'text-slate-600'
                }`} />
                <CardTitle className={`text-lg ${darkMode ? 'text-white' : 'text-slate-900'}`}>
                  {modality.name}
                </CardTitle>
              </CardHeader>
            </Card>
          ))}
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className={`grid w-full grid-cols-3 ${darkMode ? 'bg-slate-800' : 'bg-slate-100'}`}>
            <TabsTrigger value="upload" className={darkMode ? 'data-[state=active]:bg-blue-900' : ''}>
              Upload Image
            </TabsTrigger>
            <TabsTrigger value="analyze" className={darkMode ? 'data-[state=active]:bg-blue-900' : ''} disabled={!uploadedImage}>
              Analyze
            </TabsTrigger>
            <TabsTrigger value="results" className={darkMode ? 'data-[state=active]:bg-blue-900' : ''} disabled={!results}>
              Results
            </TabsTrigger>
          </TabsList>

          <TabsContent value="upload" className="mt-6">
            <Card className={darkMode ? 'bg-slate-800/50 border-slate-700' : 'bg-white border-slate-200'}>
              <CardHeader>
                <CardTitle className={darkMode ? 'text-white' : 'text-slate-900'}>
                  Upload Liver Imaging
                </CardTitle>
                <CardDescription className={darkMode ? 'text-gray-400' : 'text-slate-600'}>
                  Select a {selectedModality.replace('-', ' ').toUpperCase()} image for liver disease analysis
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div
                  className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all ${
                    darkMode
                      ? 'border-blue-500 bg-slate-900/50 hover:bg-slate-900/80 hover:border-blue-400'
                      : 'border-blue-300 bg-blue-50 hover:bg-blue-100 hover:border-blue-400'
                  }`}
                  onClick={() => fileInputRef.current?.click()}
                >
                  <Upload className={`h-12 w-12 mx-auto mb-4 ${darkMode ? 'text-blue-400' : 'text-blue-600'}`} />
                  <p className={`text-lg font-semibold mb-2 ${darkMode ? 'text-white' : 'text-slate-900'}`}>
                    Click to upload or drag and drop
                  </p>
                  <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-slate-600'}`}>
                    PNG, JPG, DICOM up to 50MB
                  </p>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="hidden"
                  />
                </div>

                {['liver-mri', 'liver-ct', 'ultrasound'].includes(selectedModality) && (
                  <>
                    <div className="text-center">
                      <p className={`mb-3 ${darkMode ? 'text-gray-400' : 'text-slate-600'}`}>or</p>
                    </div>

                    <div className={`p-4 rounded-xl ${darkMode ? 'bg-slate-900/50' : 'bg-slate-50'}`}>
                      <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-slate-700'}`}>
                        Select a Demo Patient
                      </label>
                      <select
                        value={selectedPatientId}
                        onChange={(e) => setSelectedPatientId(e.target.value)}
                        disabled={loadingPatients}
                        className={`w-full p-3 rounded-lg border ${
                          darkMode 
                            ? 'bg-slate-800 border-slate-600 text-white' 
                            : 'bg-white border-slate-300 text-slate-900'
                        } ${loadingPatients ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
                      >
                        <option value="">
                          {loadingPatients ? 'Loading patients...' : 'Random Patient (Default)'}
                        </option>
                        {availablePatients.map((patient) => (
                          <option key={patient.patient_id} value={patient.patient_id}>
                            {patient.name} - {patient.age}y, {patient.gender} - {patient.medical_background.split('.')[0]}
                          </option>
                        ))}
                      </select>
                      <p className={`text-xs mt-2 ${darkMode ? 'text-gray-500' : 'text-slate-500'}`}>
                        Select a specific patient or leave blank for random selection
                      </p>
                    </div>

                    <div className="text-center mt-4">
                      <Button
                        onClick={loadDemoImage}
                        variant="outline"
                        className={darkMode ? 'border-blue-400 text-blue-400 hover:bg-blue-900/30' : 'border-blue-600 text-blue-600'}
                      >
                        <FileImage className="h-4 w-4 mr-2" />
                        Load {selectedPatientId ? 'Selected Patient' : 'Demo'} Image
                      </Button>
                    </div>
                  </>
                )}

                {selectedModality === 'pathology' && (
                  <div className="text-center">
                    <p className={`mb-3 ${darkMode ? 'text-gray-400' : 'text-slate-600'}`}>or</p>
                    <Button
                      onClick={loadDemoImage}
                      variant="outline"
                      className={darkMode ? 'border-blue-400 text-blue-400 hover:bg-blue-900/30' : 'border-blue-600 text-blue-600'}
                    >
                      <FileImage className="h-4 w-4 mr-2" />
                      Load Demo {selectedModality.toUpperCase()} Image
                    </Button>
                  </div>
                )}

                {safeUploadedImage && (
                  <div className={`mt-6 p-4 rounded-xl ${darkMode ? 'bg-slate-900/50' : 'bg-slate-50'}`}>
                    <img
                      src={safeUploadedImage}
                      alt="Uploaded medical image"
                      className="max-w-full h-auto rounded-lg mx-auto"
                      style={{ maxHeight: '400px' }}
                    />
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="analyze" className="mt-6">
            <Card className={darkMode ? 'bg-slate-800/50 border-slate-700' : 'bg-white border-slate-200'}>
              <CardHeader>
                <CardTitle className={darkMode ? 'text-white' : 'text-slate-900'}>
                  Liver Disease Analysis Pipeline
                </CardTitle>
                <CardDescription className={darkMode ? 'text-gray-400' : 'text-slate-600'}>
                  AI-powered hepatology analysis using Azure AI Foundry
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {safeUploadedImage && (
                  <div className={`p-4 rounded-xl ${darkMode ? 'bg-slate-900/50' : 'bg-slate-50'}`}>
                    <img
                      src={safeUploadedImage}
                      alt="Image to analyze"
                      className="max-w-full h-auto rounded-lg mx-auto"
                      style={{ maxHeight: '300px' }}
                    />
                  </div>
                )}

                {demoPatientData && (
                  <div className="my-6">
                    <h3 className={`text-lg font-semibold mb-4 ${darkMode ? 'text-white' : 'text-slate-900'}`}>
                      Patient Information
                    </h3>
                    <div className={`p-6 rounded-xl ${
                      darkMode ? 'bg-slate-800' : 'bg-white'
                    } border ${darkMode ? 'border-slate-700' : 'border-gray-200'}`}>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
                        <DemoField 
                          label="Patient Name" 
                          value={demoPatientData.name || 'N/A'} 
                          darkMode={darkMode} 
                        />
                        <DemoField 
                          label="Age" 
                          value={`${demoPatientData.age} years`} 
                          darkMode={darkMode} 
                        />
                        <DemoField 
                          label="Gender" 
                          value={demoPatientData.gender} 
                          darkMode={darkMode} 
                        />
                      </div>
                      {demoPatientData.medical_background && (
                        <div className="mt-4 pt-4 border-t border-slate-600">
                          <p className={`text-sm mb-1 ${darkMode ? 'text-gray-400' : 'text-slate-600'}`}>
                            Medical Background
                          </p>
                          <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-slate-700'}`}>
                            {demoPatientData.medical_background}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                <div className="space-y-4">
                  {analysisSteps.map((step, idx) => (
                    <div key={idx} className="flex items-center gap-4">
                      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                        step.status === 'complete'
                          ? darkMode ? 'bg-green-900/50 text-green-400' : 'bg-green-100 text-green-600'
                          : processing && analysisStep === idx
                          ? darkMode ? 'bg-blue-900/50 text-blue-400' : 'bg-blue-100 text-blue-600'
                          : darkMode ? 'bg-slate-700 text-gray-400' : 'bg-slate-200 text-slate-400'
                      }`}>
                        {step.status === 'complete' ? (
                          <CheckCircle2 className="h-5 w-5" />
                        ) : processing && analysisStep === idx ? (
                          <Loader2 className="h-5 w-5 animate-spin" />
                        ) : (
                          <span>{idx + 1}</span>
                        )}
                      </div>
                      <div className="flex-1">
                        <div className={`font-medium ${darkMode ? 'text-white' : 'text-slate-900'}`}>
                          {step.name}
                        </div>
                        {processing && analysisStep === idx && (
                          <Progress value={66} className="mt-2 h-2" />
                        )}
                      </div>
                    </div>
                  ))}
                </div>

                <Button
                  onClick={runAnalysis}
                  disabled={processing || !uploadedImage}
                  className={`w-full ${darkMode ? 'bg-blue-600 hover:bg-blue-700' : 'bg-blue-600 hover:bg-blue-700'}`}
                  size="lg"
                >
                  {processing ? (
                    <>
                      <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    <>
                      <Brain className="h-5 w-5 mr-2" />
                      Start AI Analysis
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="results" className="mt-6">
            {results && (
              <div className="space-y-6">
                <Card className={darkMode ? 'bg-slate-800/50 border-slate-700' : 'bg-white border-slate-200'}>
                  <CardHeader>
                    <CardTitle className={darkMode ? 'text-white' : 'text-slate-900'}>
                      Liver Analysis Complete
                    </CardTitle>
                    <CardDescription className={darkMode ? 'text-gray-400' : 'text-slate-600'}>
                      Comprehensive AI-powered liver disease assessment
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="grid grid-cols-3 gap-4">
                      <div className={`${darkMode ? 'bg-blue-900/30' : 'bg-blue-100'} p-4 rounded-xl`}>
                        <div className={`text-2xl font-bold ${darkMode ? 'text-blue-400' : 'text-blue-600'}`}>
                          {results.metrics.processingTime}
                        </div>
                        <div className={`text-xs ${darkMode ? 'text-gray-400' : 'text-slate-600'}`}>
                          Process Time
                        </div>
                      </div>
                      <div className={`${darkMode ? 'bg-green-900/30' : 'bg-green-100'} p-4 rounded-xl`}>
                        <div className={`text-2xl font-bold ${darkMode ? 'text-green-400' : 'text-green-600'}`}>
                          {results.metrics.accuracy}
                        </div>
                        <div className={`text-xs ${darkMode ? 'text-gray-400' : 'text-slate-600'}`}>
                          Accuracy
                        </div>
                      </div>
                      <div className={`${darkMode ? 'bg-purple-900/30' : 'bg-purple-100'} p-4 rounded-xl`}>
                        <div className={`text-2xl font-bold ${darkMode ? 'text-purple-400' : 'text-purple-600'}`}>
                          {results.metrics.modelsUsed}
                        </div>
                        <div className={`text-xs ${darkMode ? 'text-gray-400' : 'text-slate-600'}`}>
                          AI Models
                        </div>
                      </div>
                    </div>

                    {uploadedImage && (
                      <div className="my-6">
                        <h3 className={`text-lg font-semibold mb-4 ${darkMode ? 'text-white' : 'text-slate-900'}`}>
                          3D Liver Visualization
                        </h3>
                        <Liver3DViewer imageUrl={safeUploadedImage!} darkMode={darkMode} />
                      </div>
                    )}

                    {results.demographics && (
                      <div className="my-6">
                        <h3 className={`text-lg font-semibold mb-4 ${darkMode ? 'text-white' : 'text-slate-900'}`}>
                          Patient Demographics
                        </h3>
                        <div className={`p-6 rounded-xl ${
                          darkMode ? 'bg-slate-800' : 'bg-white'
                        } border ${darkMode ? 'border-slate-700' : 'border-gray-200'}`}>
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                            <DemoField 
                              label="Patient ID" 
                              value={results.demographics.patient_id} 
                              darkMode={darkMode} 
                            />
                            <DemoField 
                              label="Age" 
                              value={`${results.demographics.age} years`} 
                              darkMode={darkMode} 
                            />
                            <DemoField 
                              label="Gender" 
                              value={results.demographics.gender} 
                              darkMode={darkMode} 
                            />
                            <DemoField 
                              label="Ethnicity" 
                              value={results.demographics.ethnicity} 
                              darkMode={darkMode} 
                            />
                          </div>
                        </div>
                      </div>
                    )}

                    <div className={`${darkMode ? 'bg-slate-900/50' : 'bg-slate-50'} p-4 rounded-xl`}>
                      <div className={`text-sm font-semibold mb-2 ${darkMode ? 'text-blue-400' : 'text-blue-600'}`}>
                        Liver Feature Classification
                      </div>
                      <div className={`font-bold mb-2 ${darkMode ? 'text-white' : 'text-slate-900'}`}>
                        {results.embeddings.classification}
                      </div>
                      <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-slate-600'} space-y-1`}>
                        {results.embeddings.features.map((feature, idx) => (
                          <div key={idx}>• {feature}</div>
                        ))}
                      </div>
                    </div>

                    <div className={`${darkMode ? 'bg-slate-900/50' : 'bg-slate-50'} p-4 rounded-xl`}>
                      <div className={`text-sm font-semibold mb-2 ${darkMode ? 'text-blue-400' : 'text-blue-600'}`}>
                        Liver Tumor Segmentation
                      </div>
                      <div className="space-y-2">
                        {results.segmentation.detected.map((item, idx) => (
                          <div key={idx} className={`flex items-center justify-between ${darkMode ? 'text-white' : 'text-slate-900'}`}>
                            <span>• {item}</span>
                            <span className={`text-xs px-2 py-1 rounded ${darkMode ? 'bg-blue-900/50' : 'bg-blue-200'}`}>
                              Detected
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className={`${darkMode ? 'bg-slate-900/50' : 'bg-slate-50'} p-4 rounded-xl`}>
                      <div className={`text-sm font-semibold mb-3 ${darkMode ? 'text-blue-400' : 'text-blue-600'} flex items-center gap-2`}>
                        <Brain className="w-4 h-4" />
                        Hepatology Clinical Analysis
                      </div>
                      <div className={`text-sm ${darkMode ? 'text-gray-300' : 'text-slate-700'} whitespace-pre-line leading-relaxed`}>
                        {results.gpt5Analysis}
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <div className={`grid grid-cols-4 gap-4 ${darkMode ? 'bg-slate-800/30' : 'bg-white/50'} backdrop-blur-lg rounded-2xl p-6 border ${darkMode ? 'border-blue-800' : 'border-blue-200'}`}>
                  {[
                    { label: 'Models Used', value: 'MedImageInsight, BiomedParse, GPT-5' },
                    { label: 'Confidence Score', value: results.metrics.accuracy },
                    { label: 'Processing Method', value: useMockData ? 'Demo Mode' : 'Azure AI Foundry' },
                    { label: 'Compliance', value: 'Research Use Only' }
                  ].map((stat, idx) => (
                    <div key={idx} className="text-center">
                      <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-slate-600'} mb-1`}>
                        {stat.label}
                      </div>
                      <div className={`font-semibold text-xs ${darkMode ? 'text-white' : 'text-slate-900'}`}>
                        {stat.value}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App
