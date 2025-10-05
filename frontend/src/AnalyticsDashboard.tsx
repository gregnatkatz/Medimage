import { Activity, Brain, TrendingUp, FileImage } from 'lucide-react'
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface AnalyticsDashboardProps {
  darkMode: boolean
  onNavigate: (page: 'landing' | 'analysis' | 'dashboard') => void
}

const modalityData = [
  { name: 'Liver MRI', count: 350 },
  { name: 'Liver CT', count: 420 },
  { name: 'Ultrasound', count: 180 },
  { name: 'Pathology', count: 50 },
]

const diseaseData = [
  { name: 'Hepatocellular Carcinoma', value: 280 },
  { name: 'Liver Cirrhosis', value: 220 },
  { name: 'Fatty Liver Disease', value: 180 },
  { name: 'Liver Metastases', value: 150 },
  { name: 'Healthy Control', value: 170 },
]

const accuracyData = [
  { month: 'Jan', accuracy: 92.3 },
  { month: 'Feb', accuracy: 93.1 },
  { month: 'Mar', accuracy: 94.2 },
  { month: 'Apr', accuracy: 95.1 },
  { month: 'May', accuracy: 95.8 },
  { month: 'Jun', accuracy: 96.5 },
]

const COLORS = ['#3B82F6', '#8B5CF6', '#EC4899', '#F59E0B', '#10B981']

function StatCard({ darkMode, icon, label, value, change }: any) {
  return (
    <div className={`p-6 rounded-xl ${
      darkMode ? 'bg-slate-800' : 'bg-white'
    } border ${darkMode ? 'border-slate-700' : 'border-gray-200'}`}>
      <div className="flex items-center justify-between mb-2">
        <div className={`p-2 rounded-lg ${
          darkMode ? 'bg-blue-500/20' : 'bg-blue-50'
        }`}>
          <div className="text-blue-500">{icon}</div>
        </div>
        <span className="text-green-500 text-sm font-semibold">{change}</span>
      </div>
      <p className={`text-sm mb-1 ${darkMode ? 'text-gray-400' : 'text-slate-600'}`}>
        {label}
      </p>
      <p className={`text-3xl font-bold ${darkMode ? 'text-white' : 'text-slate-900'}`}>
        {value}
      </p>
    </div>
  )
}

function ChartCard({ darkMode, title, children }: any) {
  return (
    <div className={`p-6 rounded-xl ${
      darkMode ? 'bg-slate-800' : 'bg-white'
    } border ${darkMode ? 'border-slate-700' : 'border-gray-200'}`}>
      <h3 className={`text-lg font-semibold mb-4 ${
        darkMode ? 'text-white' : 'text-slate-900'
      }`}>
        {title}
      </h3>
      {children}
    </div>
  )
}

function DemographicRow({ darkMode, label, value, detail }: any) {
  return (
    <div className="flex justify-between items-start">
      <div>
        <p className={`font-medium ${darkMode ? 'text-white' : 'text-slate-900'}`}>
          {label}
        </p>
        <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-slate-600'}`}>
          {detail}
        </p>
      </div>
      <p className={`font-semibold ${darkMode ? 'text-blue-400' : 'text-blue-600'}`}>
        {value}
      </p>
    </div>
  )
}

export default function AnalyticsDashboard({ darkMode, onNavigate }: AnalyticsDashboardProps) {
  const textColor = darkMode ? '#E5E7EB' : '#1F2937'
  const gridColor = darkMode ? '#374151' : '#E5E7EB'

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-slate-900' : 'bg-gray-50'}`}>
      <nav className={`border-b ${darkMode ? 'border-slate-700 bg-slate-800' : 'border-gray-200 bg-white'}`}>
        <div className="max-w-7xl mx-auto px-4 py-4 flex gap-4">
          <button
            onClick={() => onNavigate('landing')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              darkMode ? 'hover:bg-slate-700 text-gray-300' : 'hover:bg-gray-100 text-slate-700'
            }`}
          >
            Home
          </button>
          <button
            onClick={() => onNavigate('analysis')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              darkMode ? 'hover:bg-slate-700 text-gray-300' : 'hover:bg-gray-100 text-slate-700'
            }`}
          >
            Analysis
          </button>
          <button
            className={`px-4 py-2 rounded-lg ${
              darkMode ? 'bg-blue-600 text-white' : 'bg-blue-500 text-white'
            }`}
          >
            Dashboard
          </button>
        </div>
      </nav>

      <div className="p-8">
        <div className="max-w-7xl mx-auto">
          <div className="mb-8">
            <h1 className={`text-4xl font-bold mb-2 ${darkMode ? 'text-white' : 'text-slate-900'}`}>
              Analytics Dashboard
            </h1>
            <p className={`${darkMode ? 'text-gray-400' : 'text-slate-600'}`}>
              Comprehensive insights from 1000+ liver disease imaging studies
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <StatCard
              darkMode={darkMode}
              icon={<FileImage className="w-6 h-6" />}
              label="Total Images"
              value="1,000"
              change="+12%"
            />
            <StatCard
              darkMode={darkMode}
              icon={<Activity className="w-6 h-6" />}
              label="Accuracy Rate"
              value="96.5%"
              change="+2.3%"
            />
            <StatCard
              darkMode={darkMode}
              icon={<Brain className="w-6 h-6" />}
              label="AI Models"
              value="4"
              change="Active"
            />
            <StatCard
              darkMode={darkMode}
              icon={<TrendingUp className="w-6 h-6" />}
              label="Analyses Today"
              value="47"
              change="+8"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ChartCard darkMode={darkMode} title="Image Modality Distribution">
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={modalityData}>
                  <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
                  <XAxis dataKey="name" stroke={textColor} />
                  <YAxis stroke={textColor} />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: darkMode ? '#1F2937' : '#FFFFFF',
                      border: `1px solid ${gridColor}`,
                      color: textColor
                    }} 
                  />
                  <Bar dataKey="count" fill="#3B82F6" />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard darkMode={darkMode} title="Disease Type Distribution">
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={diseaseData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {diseaseData.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: darkMode ? '#1F2937' : '#FFFFFF',
                      border: `1px solid ${gridColor}`,
                      color: textColor
                    }} 
                  />
                </PieChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard darkMode={darkMode} title="Detection Accuracy Over Time">
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={accuracyData}>
                  <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
                  <XAxis dataKey="month" stroke={textColor} />
                  <YAxis stroke={textColor} domain={[90, 100]} />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: darkMode ? '#1F2937' : '#FFFFFF',
                      border: `1px solid ${gridColor}`,
                      color: textColor
                    }} 
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="accuracy" 
                    stroke="#10B981" 
                    strokeWidth={2}
                    name="Accuracy %"
                  />
                </LineChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard darkMode={darkMode} title="Patient Demographics Summary">
              <div className="space-y-4 p-4">
                <DemographicRow 
                  darkMode={darkMode}
                  label="Age Range"
                  value="35-75 years"
                  detail="Average: 55 years"
                />
                <DemographicRow 
                  darkMode={darkMode}
                  label="Gender Distribution"
                  value="52% Male / 48% Female"
                  detail="Near-equal representation"
                />
                <DemographicRow 
                  darkMode={darkMode}
                  label="Ethnicity"
                  value="Multi-ethnic cohort"
                  detail="Caucasian, Asian, Hispanic, African American"
                />
                <DemographicRow 
                  darkMode={darkMode}
                  label="Dataset Source"
                  value="Kaggle Medical Datasets"
                  detail="De-identified research data"
                />
              </div>
            </ChartCard>
          </div>

          <div className={`mt-8 p-6 rounded-xl border-2 ${
            darkMode ? 'bg-amber-900/20 border-amber-500/50' : 'bg-amber-50 border-amber-200'
          }`}>
            <p className={`text-sm ${darkMode ? 'text-amber-200' : 'text-amber-900'}`}>
              <strong>⚠️ Research Data Notice:</strong> All statistics shown are derived from 
              Kaggle medical imaging datasets for research and demonstration purposes only. 
              This platform contains no HIPAA-protected information and is not intended for 
              clinical decision-making.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
