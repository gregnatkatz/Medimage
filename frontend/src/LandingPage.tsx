interface LandingPageProps {
  darkMode: boolean
  onEnter: () => void
}

export default function LandingPage({ darkMode, onEnter }: LandingPageProps) {
  return (
    <div className={`min-h-screen flex flex-col items-center justify-center p-8 ${
      darkMode ? 'bg-slate-900' : 'bg-gradient-to-br from-blue-50 to-indigo-100'
    }`}>
      <div className="mb-8">
        <img 
          src="/logo.png" 
          alt="Azure AI Logo" 
          className="h-20 object-contain"
        />
      </div>

      <h1 className={`text-5xl font-bold mb-4 text-center ${
        darkMode ? 'text-white' : 'text-slate-900'
      }`}>
        Liver Disease Imaging AI Platform
      </h1>

      <p className={`text-xl mb-8 text-center max-w-2xl ${
        darkMode ? 'text-gray-300' : 'text-slate-700'
      }`}>
        Powered by Azure AI Foundry and Advanced Medical Imaging Models
      </p>

      <div className="mb-12">
        <img 
          src="/Liver_03_animation.gif" 
          alt="3D Rotating Liver Model" 
          className="w-[400px] h-[400px] rounded-xl border-4 border-blue-500/40 shadow-2xl"
        />
      </div>

      <div className={`max-w-4xl mb-12 p-8 rounded-xl shadow-xl ${
        darkMode ? 'bg-slate-800/70' : 'bg-white/70'
      } backdrop-blur-md border-2 ${
        darkMode ? 'border-blue-500/40' : 'border-blue-300'
      }`}>
        <h2 className={`text-3xl font-bold mb-6 ${
          darkMode ? 'text-white' : 'text-slate-900'
        }`}>
          Executive Summary
        </h2>
        <div className={`space-y-4 text-left ${
          darkMode ? 'text-gray-300' : 'text-slate-700'
        }`}>
          <p className="text-lg leading-relaxed">
            This demonstration platform showcases advanced AI capabilities for liver disease 
            detection and analysis using Microsoft Azure AI Foundry services integrated with 
            state-of-the-art medical imaging models.
          </p>
          <p className="font-semibold text-lg">
            Key Features:
          </p>
          <ul className="list-disc list-inside space-y-2 ml-4 text-base">
            <li>Multi-modal liver imaging analysis (MRI, CT, Ultrasound)</li>
            <li>Advanced tumor detection and segmentation using MedImageParse and MedImageInsight</li>
            <li>Interactive 3D visualization of liver structures</li>
            <li>Comprehensive analytics dashboard with clinical metrics</li>
            <li>Patient demographics integration from medical datasets</li>
            <li>Real-time AI-powered clinical insights via Azure OpenAI GPT-4.1</li>
            <li>Rich testing capabilities inspired by Stanford MedAI research</li>
          </ul>
          <p className="text-base">
            <strong>Dataset:</strong> 1000+ liver disease images from Kaggle medical imaging datasets, 
            organized into demo (60%) and live testing (40%) splits, including CT, MRI, and ultrasound modalities.
          </p>
        </div>
      </div>

      <button
        onClick={onEnter}
        className="px-8 py-4 bg-gradient-to-r from-blue-500 to-indigo-600 text-white 
                   rounded-xl font-semibold text-lg hover:from-blue-600 hover:to-indigo-700 
                   transition-all transform hover:scale-105 shadow-lg"
      >
        Enter Platform
      </button>

      <div className={`mt-12 max-w-2xl text-center text-sm ${
        darkMode ? 'text-gray-400' : 'text-slate-600'
      } border-t ${
        darkMode ? 'border-gray-700' : 'border-gray-300'
      } pt-6`}>
        <p className="font-semibold mb-2">⚠️ RESEARCH AND EDUCATIONAL USE ONLY</p>
        <p>
          This platform uses Kaggle medical imaging datasets for research and demonstration purposes. 
          All data is de-identified and contains no HIPAA-protected health information. 
          This system is NOT intended for clinical diagnosis or treatment decisions.
        </p>
      </div>
    </div>
  )
}
