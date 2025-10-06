# Liver Disease Imaging AI Platform

A comprehensive medical imaging AI demonstration platform focused on liver disease analysis, powered by Azure AI Foundry and advanced medical imaging models.

![Azure AI Logo](frontend/public/logo.png)

## 🎯 Project Overview

This platform demonstrates advanced AI capabilities for liver disease detection and analysis using Microsoft Azure AI Foundry services integrated with state-of-the-art medical imaging models including BiomedParse, MedImageParse, MedImageInsight, and GPT-5.

## 📥 Kaggle Dataset Setup

This application requires Kaggle liver imaging datasets for testing and demonstration. **Do not commit these large dataset files to the repository.**

### Download Instructions

1. **Install Kaggle CLI:**
```bash
pip install kaggle
```

2. **Configure Kaggle credentials:**
   - Go to [Kaggle Account Settings](https://www.kaggle.com/settings)
   - Click "Create New API Token" to download `kaggle.json`
   - Place it in `~/.kaggle/kaggle.json` and set permissions:
```bash
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

3. **Download the dataset:**
```bash
cd data/kaggle
kaggle datasets download -d andrewmvd/liver-tumor-segmentation
unzip liver-tumor-segmentation.zip
```

4. **Organize the data:**
```bash
mkdir -p Task03_Liver_rs/images
cd volume_pt1
for f in volume-*.nii; do cp "$f" "../Task03_Liver_rs/images/liver_${f#volume-}"; done
```

The final structure should be:
```
data/
└── kaggle/
    └── liver-tumor/
        └── Task03_Liver_rs/
            └── images/
                ├── liver_0.nii
                ├── liver_1.nii
                └── ...
```

### Dataset Information
- **Size:** ~5.2 GB
- **Format:** NIfTI (.nii) 3D medical imaging volumes
- **Source:** [Kaggle - Liver Tumor Segmentation](https://www.kaggle.com/datasets/andrewmvd/liver-tumor-segmentation)
- **License:** Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)



### Current Features (Implemented ✅)

- **Landing Page**: Professional entry point with Azure AI branding, spinning 3D liver model with highlighted tumor, and executive summary
- **Multi-Modal Image Analysis**: Support for Liver MRI, Liver CT, Ultrasound, and Pathology imaging
- **Interactive 2D Image Viewer**: Interactive liver image viewer with zoom, rotate, pan, and reset controls
- **Analytics Dashboard**: Comprehensive charts showing:
  - Image modality distribution (bar chart)
  - Disease type distribution (pie chart)
  - Detection accuracy over time (line chart)
  - Patient demographics summary
- **Patient Demographics**: Integration of demographic data from Kaggle medical datasets
- **Research Disclaimer**: Clear warnings on landing and dashboard pages
- **Dark/Light Mode Toggle**: Responsive UI with theme support
- **Mock AI Pipeline**: Complete simulation of Azure AI Foundry workflow ready for real endpoint integration

### Tech Stack

**Backend:**
- FastAPI (Python 3.12)
- Poetry for dependency management
- Mock Azure AI services (ready to switch to real endpoints)

**Frontend:**
- React + TypeScript + Vite
- Tailwind CSS for styling
- React Three Fiber for landing page 3D liver model
- Recharts for analytics dashboard
- Lucide React for icons

**Data:**
- Kaggle datasets: 3D Liver Tumor Segmentation (2.2GB) + CHAOS T1&T2 (588MB)
- Total: 2.8GB of liver disease imaging data
- Location: `/home/ubuntu/medical-ai-demo/data/kaggle/`
- **Format**: NIfTI (.nii, .nii.gz) 3D volumes - fully compatible with:
  - **MedImageParse 2D**: Extract and analyze individual slices for pathology detection
  - **MedImageParse 3D**: Process entire 3D volumes for tumor segmentation, size measurement, and staging
  - Can be converted to PNG/JPEG for BiomedParse and other 2D models

## 🚀 Getting Started

### Prerequisites

- Python 3.12+ (managed via pyenv)
- Node.js 18+ (managed via nvm)
- Poetry for Python dependency management
- pnpm or npm for Node.js dependencies

### Installation

1. **Clone the repository** (tomorrow after repo creation)

2. **Backend Setup:**
```bash
cd backend
poetry install
cp .env.example .env
# Configure Azure credentials in .env
poetry run fastapi dev app/main.py
```

3. **Frontend Setup:**
```bash
cd frontend
npm install
cp .env.example .env
# Configure backend URL in .env
npm run dev
```

4. **Access the application:**
- Frontend: http://localhost:5173/
- Backend API: http://localhost:8000/
- API Docs: http://localhost:8000/docs

## 📊 Current Status

### ✅ Completed (October 5, 2025)

- [x] FastAPI backend with mock Azure AI services
- [x] React frontend with full navigation
- [x] Landing page with spinning liver + tumor
- [x] Analysis page with image upload
- [x] Results page with 3D viewer, demographics, clinical analysis
- [x] Analytics dashboard with 4 charts
- [x] Azure AI logo integration
- [x] Kaggle dataset download (2.8GB)
- [x] Interactive 2D image viewer with zoom/rotate/pan controls
- [x] Research disclaimers on all pages
- [x] Dark mode support throughout

### 🔄 Ready for Tomorrow (October 6, 2025)

The application is fully functional with mock endpoints and ready for Azure AI Foundry integration.

## 🤖 AI Models Architecture

This platform integrates 5 specialized Azure AI models, each serving a distinct purpose in the liver disease analysis pipeline:

### 1. MedImageInsight
**Purpose:** Image embedding and classification  
**What it adds:** Generates semantic embeddings for medical images, enabling similarity search, image retrieval, and initial classification. Creates vector representations that capture anatomical and pathological features.  
**Use case:** Quick screening, finding similar cases, initial triage of liver imaging studies

### 2. MedImageParse (2D)
**Purpose:** 2D medical image segmentation  
**What it adds:** Specialized segmentation across multiple liver imaging modalities (MRI, CT, ultrasound, pathology). Accurately identifies and delineates liver structures, lesions, and anatomical boundaries in individual slices.  
**Use case:** Slice-by-slice analysis, pathology detection in 2D images, detailed boundary identification

### 3. MedImageParse 3D
**Purpose:** Volumetric 3D segmentation  
**What it adds:** Complete 3D volume analysis for CT/MRI scans. Critical for accurate tumor size measurement, volumetric assessment, staging, and surgical planning. Processes entire NIfTI volumes rather than individual slices.  
**Use case:** 3D tumor reconstruction, volume calculation, preoperative planning, disease staging

### 4. BiomedParse
**Purpose:** Unified detection, recognition, and segmentation  
**What it adds:** Versatile model supporting 9 imaging modalities with combined object detection and segmentation. Can identify multiple anatomical structures and pathologies simultaneously with text-based prompts.  
**Use case:** Multi-structure analysis, comprehensive organ assessment, flexible prompted segmentation

### 5. GPT-5
**Purpose:** Clinical reasoning and analysis  
**What it adds:** Advanced language model that synthesizes findings from all imaging models into comprehensive clinical reports. Provides differential diagnoses, confidence assessments, and recommended follow-up actions using state-of-the-art reasoning capabilities.  
**Use case:** Clinical report generation, diagnostic reasoning, patient communication, decision support

### Integration Flow

```
Input Image
    ↓
MedImageInsight → [Embeddings & Initial Classification]

## 🔄 Configuration

The application supports two modes:

- **Mock Mode (Default)**: Uses simulated AI responses for testing
- **Production Mode**: Connects to real Azure AI services

Configure via `backend/.env`:

```bash
# Toggle between mock and real AI services
USE_MOCK_DATA=true  # Set to false for production mode

# Azure Authentication
AZURE_TENANT_ID=your_tenant_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_API_VERSION=2025-01-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1

# Azure ML Medical Imaging Endpoint
AZURE_ML_ENDPOINT=your_ml_endpoint
AZURE_ML_API_KEY=your_ml_api_key

# Medical Imaging Model Deployments
MEDIMAGEPARSE_DEPLOYMENT=medimageparse-deployment
MEDIMAGEINSIGHT_DEPLOYMENT=medimageinsight-deployment
MEDIMAGEPARSE3D_DEPLOYMENT=medimageparse3d
```

## 🚀 Deploying Medical Imaging Models to Azure

### Option 1: Deploy via Azure ML Endpoint

1. **Set environment variables** with your Azure credentials:
```bash
export AZURE_ML_ENDPOINT_NAME="medparse101-gnk"
export AZURE_ML_ENDPOINT="https://medparse101-gnk.eastus2.inference.ml.azure.com/score"
export AZURE_ML_API_KEY="your-api-key-here"
```

2. **Run the deployment script**:
```bash
python deploy_medical_models.py
```

### Option 2: Deploy via Azure AI Foundry

1. **Set environment variables**:
```bash
export FOUNDRY_ENDPOINT="https://your-foundry-endpoint.services.ai.azure.com"
export FOUNDRY_API_KEY="your-foundry-api-key"
export AZURE_ML_ENDPOINT_NAME="medparse101-gnk"
export AZURE_ML_ENDPOINT="https://medparse101-gnk.eastus2.inference.ml.azure.com/score"
export AZURE_ML_API_KEY="your-ml-api-key"
```

2. **Run the deployment script**:
```bash
python deploy_medical_models_foundry.py
```

## 🔄 Switching to Real Azure AI Endpoints

Once the Azure ML endpoint is fully deployed, switch from mock to real endpoints:

1. **Update backend/.env**:
```bash
USE_MOCK_DATA=false
```

2. **Restart the backend**:
```bash
cd backend
poetry run fastapi dev app/main.py
```

3. **Verify real endpoint is active**:
```bash
curl http://localhost:8000/healthz
```

Expected response should show `"mode": "production"` instead of `"mode": "mock"`.

4. **Test with real medical imaging analysis** by uploading images through the frontend.


    ↓
MedImageParse 2D/3D + BiomedParse → [Detailed Segmentation]
    ↓
GPT-5 → [Clinical Analysis & Report]
    ↓
Structured Output with Visualizations
```

## 🔧 Next Steps: Azure AI Foundry Integration

### Tomorrow's Tasks (October 6, 2025)

#### 1. Azure Resource Setup
- [ ] Create Azure AI Foundry hub and project
- [ ] Deploy required AI models:
  - **MedImageInsight**: Image embedding model for classification and similarity search
  - **MedImageParse**: 2D segmentation across liver imaging modalities (MRI, CT, ultrasound, pathology)
  - **MedImageParse 3D**: Volumetric segmentation for 3D CT/MRI scans - critical for tumor size/staging
  - **BiomedParse**: Unified detection, recognition, and segmentation across 9 imaging modalities
  - **CxrReportGen**: Automated chest X-ray report generation (optional for liver focus)
  - **GPT-5**: Clinical reasoning and comprehensive analysis
- [ ] Obtain API keys and endpoint URLs
- [ ] Configure RBAC permissions

#### 2. Backend Integration

**File to modify:** `backend/app/services.py`

Replace the `MockAzureAIService` with `RealAzureAIService`:

```python
# In backend/app/main.py
# Change from:
ai_service = MockAzureAIService()

# To:
ai_service = RealAzureAIService()
```

**Configuration needed in `.env`:**
```bash
# Azure AI Foundry
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_VERSION=2025-08-01
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5-deployment

# Medical Imaging Models
AZURE_ML_ENDPOINT=https://your-workspace.azureml.net
AZURE_ML_API_KEY=your-ml-api-key
MEDIMAGEINSIGHT_ENDPOINT=medimageinsight-endpoint
BIOMEDPARSE_ENDPOINT=biomedparse-endpoint
MEDIMAGEPARSE_ENDPOINT=medimageparse-endpoint
MEDIMAGEPARSE_3D_ENDPOINT=medimageparse-3d-endpoint
```

**Update `RealAzureAIService` class:**

The class skeleton already exists in `backend/app/services.py`. You need to:
1. Implement `_call_medimageinsight()` method
2. Implement `_call_biomedparse()` method  
3. Implement `_call_gpt5()` method
4. Add proper error handling and retries
5. Test with real endpoints

#### 3. Endpoint Implementation Details

**MedImageInsight (Embeddings):**
```python
async def _call_medimageinsight(self, image_b64: str, modality: str) -> dict:
    response = await self.ml_client.online_endpoints.invoke(
        endpoint_name=self.config.medimageinsight_endpoint,
        request_file={
            "input_data": {
                "columns": ["image", "text"],
                "data": [[image_b64, f"{modality} medical image"]]
            },
            "params": {"get_scaling_factor": True}
        }
    )
    return response
```

**BiomedParse (Segmentation):**
```python
async def _call_biomedparse(self, image_b64: str, prompt: str) -> dict:
    response = await self.ml_client.online_endpoints.invoke(
        endpoint_name=self.config.biomedparse_endpoint,
        request_file={
            "input_data": {
                "columns": ["image", "text"],
                "data": [[image_b64, prompt]]
            }
        }
    )
    return response
```

**GPT-5 (Clinical Analysis):**
```python
async def _call_gpt5(self, embeddings: dict, segmentation: dict, modality: str) -> str:
    response = await self.openai_client.chat.completions.create(
        model=self.config.gpt5_deployment,
        messages=[
            {
                "role": "system",
                "content": "You are an expert radiologist assistant."
            },
            {
                "role": "user",
                "content": f"""Analyze these liver imaging findings:
                
                Modality: {modality}
                Embeddings: {embeddings}
                Segmentation: {segmentation}
                
                Provide detailed clinical analysis including:
                1. Key findings
                2. Differential diagnosis
                3. Recommended follow-up
                4. Confidence levels"""
            }
        ],
        temperature=0.3
    )
    return response.choices[0].message.content
```

#### 4. Testing Strategy

1. **Unit Tests**: Test each AI service method independently
2. **Integration Tests**: Test full pipeline with sample images
3. **Performance Tests**: Measure response times and accuracy
4. **Error Handling**: Verify graceful degradation

#### 5. GitHub Repository (Completed October 5, 2025)

- [x] Repository created: https://github.com/gregnatkatz/Medimage
- [x] Code pushed to main branch with all implemented features
- [x] Screenshots captured and documented
- [x] Comprehensive README with Azure integration instructions

**Ready for Tomorrow:** All code and documentation pushed to GitHub. Next session will focus on Azure AI Foundry endpoint integration.

## 📁 Project Structure

```
medical-ai-demo/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI application
│   │   ├── services.py       # AI service implementations
│   │   └── config.py         # Configuration management
│   ├── pyproject.toml        # Python dependencies
│   └── .env                  # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.tsx           # Main application with navigation
│   │   ├── LandingPage.tsx   # Landing page component
│   │   ├── SpinningLiver.tsx # 3D spinning liver model
│   │   ├── Liver3DViewer.tsx # Interactive 2D image viewer
│   │   └── AnalyticsDashboard.tsx  # Analytics dashboard
│   ├── public/
│   │   └── logo.png          # Azure AI logo
│   └── package.json          # Node.js dependencies
├── data/
│   └── kaggle/               # Kaggle datasets (2.8GB)
└── scripts/
    └── create_logo.py        # Logo generation script
```

## 🔍 API Endpoints

### Backend (http://localhost:8000)

- `GET /health` - Health check
- `GET /api/config` - Get configuration
- `POST /api/analyze` - Analyze medical image
  - Accepts: `multipart/form-data` with image file and modality
  - Returns: Embeddings, segmentation, GPT-5 analysis, metrics, demographics
- `POST /api/upload-demo` - Load demo image
  - Accepts: `application/json` with modality
  - Returns: Demo image data
- `GET /api/analytics` - Get analytics data
  - Returns: Total images, accuracy, distributions, demographics

## 🧪 Implementation Notes

### ✅ Interactive 2D Image Viewer

**Approach:** Replaced complex WebGL-based 3D viewer with a simple, reliable 2D image viewer using standard HTML and CSS.

**Implementation:**
- Uses HTML `<img>` element with CSS transforms for zoom, rotate, and pan
- Interactive controls: Zoom In/Out, Rotate 90°, Reset View
- Drag-to-pan and scroll-to-zoom support
- Lucide React icons for control buttons
- Maintains dark/light mode support

**Benefits:**
- No WebGL context issues or browser compatibility problems
- Faster loading and better performance
- Simpler codebase, easier to maintain
- Works reliably with base64 image data

**Controls:**
```typescript
// Zoom: CSS scale() transform
// Rotate: CSS rotate() transform (90° increments)
// Pan: CSS translate() transform with drag handlers
// Reset: Returns all transforms to initial state
```

## 📸 Screenshots

### Landing Page
![Landing Page](/home/ubuntu/screenshots/localhost_5173_205311.png)
*Azure AI branded landing page with spinning 3D liver model and executive summary*

### Results - Liver Scan Visualization
![Results with Visible Liver Medical Imaging Scan](/home/ubuntu/screenshots/localhost_5173_205037.png)
*Results page showing **VISIBLE grayscale abdominal CT/MRI scan** displaying liver anatomy in the 3D Liver Visualization section, with processing metrics (2.3s, 92% accuracy, 3 AI models)*

### Results - Complete Clinical Analysis
![Clinical Analysis with Liver Scan](/home/ubuntu/screenshots/localhost_5173_205140.png)
*Complete clinical analysis showing patient demographics (P0591, 41 years old, Male, African American), liver feature classification (Hepatocellular Carcinoma - Segment VII), tumor segmentation results (liver parenchyma, 3.2cm hepatic tumor, portal vein, hepatic veins all detected), and detailed GPT-5 clinical findings with differential diagnosis and treatment recommendations*

### Analytics Dashboard
![Analytics Dashboard](/home/ubuntu/screenshots/localhost_5173_205226.png)
*Comprehensive analytics dashboard with modality distribution, disease types, accuracy over time, and demographics charts*

## ⚠️ Important Notes

### Research Use Only

This platform uses Kaggle medical imaging datasets for research and demonstration purposes only. All data is de-identified and contains no HIPAA-protected health information. **This system is NOT intended for clinical diagnosis or treatment decisions.**

### Security

- Never commit API keys or secrets to the repository
- Use environment variables for all sensitive configuration
- Follow Azure security best practices
- Implement proper authentication before production use

## 📚 References

- [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-services/)
- [MedImageInsight Model](https://azure.microsoft.com/en-us/products/ai-services/ai-foundry)
- [BiomedParse Paper](https://arxiv.org/abs/2405.12971)
- [Kaggle 3D Liver Tumor Dataset](https://www.kaggle.com/datasets/gauravduttakiit/3d-liver-and-liver-tumor-segmentation)
- [CHAOS Challenge](https://chaos.grand-challenge.org/)

## 👥 Team

Requested by: Gregory Katz (@gregorykatz_microsoft)  
Developed by: Devin AI

## 📝 License

This is a demonstration project. Check individual dataset licenses before use.

---

**Link to Devin run:** https://app.devin.ai/sessions/ec1278d34fd54c969f493ec2abaa1fb8

**Last Updated:** October 5, 2025
