from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import base64
from io import BytesIO

from app.config import settings
from app.services import get_ai_service

app = FastAPI(title="Medical Imaging AI Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def healthz():
    return {
        "status": "ok",
        "mode": "mock" if settings.USE_MOCK_DATA else "production",
        "version": "1.0.0"
    }

@app.get("/api/config")
async def get_config():
    """Get frontend configuration"""
    return {
        "useMockData": settings.USE_MOCK_DATA,
        "supportedModalities": ["liver-mri", "liver-ct", "ultrasound", "pathology"]
    }

@app.post("/api/analyze")
async def analyze_image(
    image: UploadFile = File(...),
    modality: str = Form(...)
):
    """Analyze medical image using Azure AI models"""
    try:
        if modality not in ["liver-mri", "liver-ct", "ultrasound", "pathology"]:
            raise HTTPException(status_code=400, detail="Invalid modality")
        
        image_data = await image.read()
        
        if len(image_data) > 50 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image too large (max 50MB)")
        
        ai_service = get_ai_service()
        result = await ai_service.analyze_image(image_data, modality)
        
        return {
            "success": True,
            "data": result
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/upload-demo")
async def upload_demo_image(modality: str = Form(...)):
    """Load a demo image for the specified modality"""
    try:
        if modality not in ["liver-mri", "liver-ct", "ultrasound", "pathology"]:
            raise HTTPException(status_code=400, detail="Invalid modality")
        
        from PIL import Image
        import nibabel as nib
        import numpy as np
        from pathlib import Path
        import random
        
        organized_data_path = Path(__file__).parent.parent.parent / "data" / "organized" / "demo"
        
        if modality == "liver-ct":
            ct_path = organized_data_path / "ct"
            patient_dirs = [d for d in ct_path.iterdir() if d.is_dir()]
            if not patient_dirs:
                raise HTTPException(status_code=404, detail="No CT demo data found")
            
            patient_dir = random.choice(patient_dirs)
            dicom_dir = patient_dir / "DICOM_anon"
            
            if dicom_dir.exists():
                dicom_files = list(dicom_dir.glob("*.dcm"))
                if dicom_files:
                    import pydicom
                    dcm = pydicom.dcmread(str(dicom_files[len(dicom_files)//2]))
                    slice_data = dcm.pixel_array
                    
                    slice_normalized = ((slice_data - slice_data.min()) / (slice_data.max() - slice_data.min()) * 255).astype(np.uint8)
                    img = Image.fromarray(slice_normalized, mode='L').convert('RGB')
                    img = img.resize((800, 600), Image.Resampling.LANCZOS)
                    
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    return {
                        "success": True,
                        "message": f"Demo CT scan loaded (Patient {patient_dir.name})",
                        "imageUrl": f"data:image/png;base64,{img_str}"
                    }
        
        elif modality == "liver-mri":
            mri_path = organized_data_path / "mri"
            patient_dirs = [d for d in mri_path.iterdir() if d.is_dir()]
            if not patient_dirs:
                raise HTTPException(status_code=404, detail="No MRI demo data found")
            
            patient_dir = random.choice(patient_dirs)
            t2spir_dir = patient_dir / "T2SPIR" / "DICOM_anon"
            
            if t2spir_dir.exists():
                dicom_files = list(t2spir_dir.glob("*.dcm"))
                if dicom_files:
                    import pydicom
                    dcm = pydicom.dcmread(str(dicom_files[len(dicom_files)//2]))
                    slice_data = dcm.pixel_array
                    
                    slice_normalized = ((slice_data - slice_data.min()) / (slice_data.max() - slice_data.min()) * 255).astype(np.uint8)
                    img = Image.fromarray(slice_normalized, mode='L').convert('RGB')
                    img = img.resize((800, 600), Image.Resampling.LANCZOS)
                    
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    return {
                        "success": True,
                        "message": f"Demo MRI scan loaded (Patient {patient_dir.name})",
                        "imageUrl": f"data:image/png;base64,{img_str}"
                    }
        
        elif modality == "ultrasound":
            ultrasound_path = organized_data_path / "ultrasound"
            categories = ["Benign", "Malignant", "Normal"]
            category = random.choice(categories)
            category_path = ultrasound_path / category
            
            if category_path.exists():
                image_files = list(category_path.glob("*.jpg"))
                if image_files:
                    img_file = random.choice(image_files)
                    img = Image.open(img_file).convert('RGB')
                    img = img.resize((800, 600), Image.Resampling.LANCZOS)
                    
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    return {
                        "success": True,
                        "message": f"Demo ultrasound image loaded ({category}: {img_file.name})",
                        "imageUrl": f"data:image/png;base64,{img_str}"
                    }
        
        elif modality == "pathology":
            raise HTTPException(status_code=404, detail="Pathology demo data not available (no suitable Kaggle datasets found)")
        
        raise HTTPException(status_code=404, detail=f"No demo data found for {modality}")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo load failed: {str(e)}")

@app.get("/api/analytics")
async def get_analytics():
    """Get analytics data for dashboard"""
    return {
        "total_images": 1000,
        "accuracy_rate": 96.5,
        "modality_distribution": {
            "liver-mri": 350,
            "liver-ct": 420,
            "ultrasound": 180,
            "pathology": 50
        },
        "disease_distribution": {
            "Hepatocellular Carcinoma": 280,
            "Liver Cirrhosis": 220,
            "Fatty Liver Disease": 180,
            "Liver Metastases": 150,
            "Healthy Control": 170
        },
        "accuracy_over_time": [
            {"month": "Jan", "accuracy": 92.3},
            {"month": "Feb", "accuracy": 93.1},
            {"month": "Mar", "accuracy": 94.2},
            {"month": "Apr", "accuracy": 95.1},
            {"month": "May", "accuracy": 95.8},
            {"month": "Jun", "accuracy": 96.5}
        ]
    }
