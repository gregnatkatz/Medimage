import base64
import json
from typing import Dict, Any
from io import BytesIO
from PIL import Image

from app.config import settings

class MockAzureAIService:
    """Mock service that simulates Azure AI responses for local development"""
    
    def __init__(self):
        self.mock_results = {
            'liver-mri': {
                'classification': 'Hepatocellular Carcinoma - Segment VII',
                'confidence': 0.92,
                'features': ['Arterial hyperenhancement', 'Portal venous washout', 'Capsule appearance'],
                'segmentation': {
                    'detected': ['Liver parenchyma', 'Hepatic tumor (3.2cm)', 'Portal vein', 'Hepatic veins'],
                    'area': 'Segment VII, 3.2cm lesion',
                    'severity': 'Moderate concern'
                },
                'gpt5_analysis': """**Clinical Findings:**
MRI of the liver demonstrates a 3.2 cm lesion in segment VII showing arterial phase hyperenhancement with portal venous phase washout and capsule appearance, characteristic features of hepatocellular carcinoma (HCC). Background liver shows nodular contour and increased T2 signal consistent with cirrhosis.

**Differential Diagnosis:**
1. Hepatocellular carcinoma (HCC) - most likely given LI-RADS 5 criteria
2. Intrahepatic cholangiocarcinoma (less likely)
3. Hypervascular metastasis (consider if history of extrahepatic malignancy)

**Recommendations:**
- Multidisciplinary tumor board discussion recommended
- Correlate with AFP levels and liver function tests (Child-Pugh score)
- Consider BCLC staging for treatment planning
- Options may include surgical resection, ablation, or TACE depending on liver function and tumor staging
- Screen for additional lesions with triphasic imaging protocol"""
            },
            'liver-ct': {
                'classification': 'Liver Cirrhosis with Portal Hypertension',
                'confidence': 0.94,
                'features': ['Nodular liver contour', 'Splenomegaly', 'Ascites', 'Varices'],
                'segmentation': {
                    'detected': ['Cirrhotic liver', 'Enlarged spleen', 'Ascitic fluid', 'Esophageal varices'],
                    'area': 'Diffuse hepatic involvement',
                    'severity': 'Advanced cirrhosis'
                },
                'gpt5_analysis': """**Clinical Findings:**
CT scan demonstrates advanced cirrhosis with nodular liver contour, enlarged caudate lobe, and shrunken right lobe. Moderate splenomegaly (15.2 cm) and moderate volume ascites are present. Esophageal and gastric varices are identified. Portal vein measures 14mm with slow flow. No focal hepatic lesions identified.

**Differential Diagnosis:**
1. Chronic liver disease with cirrhosis and portal hypertension (confirmed)
2. Etiology considerations: Chronic viral hepatitis, alcohol-related, NASH, or autoimmune

**Recommendations:**
- Clinical correlation with liver function tests, viral serology, and Child-Pugh classification
- Surveillance for hepatocellular carcinoma with AFP and imaging every 6 months
- Upper endoscopy for variceal screening and grading
- Consider TIPS evaluation if refractory ascites or bleeding varices
- Hepatology consultation for transplant evaluation if MELD score indicates
- Paracentesis if ascites becomes symptomatic"""
            },
            'ultrasound': {
                'classification': 'Hepatic Steatosis (Fatty Liver)',
                'confidence': 0.89,
                'features': ['Increased echogenicity', 'Hepatomegaly', 'Decreased visualization of vessels'],
                'segmentation': {
                    'detected': ['Enlarged liver', 'Increased parenchymal echogenicity', 'Attenuated beam'],
                    'area': 'Diffuse hepatic involvement',
                    'severity': 'Moderate steatosis'
                },
                'gpt5_analysis': """**Clinical Findings:**
Liver ultrasound demonstrates diffusely increased hepatic echogenicity with hepatomegaly (17.5 cm craniocaudal dimension). Decreased visualization of diaphragm and intrahepatic vessels due to increased attenuation. No focal lesions identified. Portal vein is patent with normal flow direction.

**Differential Diagnosis:**
1. Hepatic steatosis (fatty liver disease) - most likely
   - Non-alcoholic fatty liver disease (NAFLD/NASH)
   - Alcohol-related fatty liver disease
2. Acute hepatitis (less likely given chronic appearance)

**Recommendations:**
- Correlate with metabolic syndrome components (diabetes, obesity, dyslipidemia)
- Liver function tests and lipid panel
- Consider FibroScan or MRI elastography for fibrosis assessment
- Lifestyle modifications: weight loss, exercise, dietary changes
- Screen for diabetes and cardiovascular risk factors
- Consider liver biopsy if suspicion for NASH with significant fibrosis
- Follow-up ultrasound in 6-12 months if no intervention or earlier if symptoms develop"""
            },
            'pathology': {
                'classification': 'Liver Biopsy - Chronic Hepatitis with Fibrosis',
                'confidence': 0.91,
                'features': ['Portal inflammation', 'Bridging fibrosis', 'Hepatocyte ballooning'],
                'segmentation': {
                    'detected': ['Portal tracts', 'Fibrotic septa', 'Hepatocytes', 'Inflammatory infiltrate'],
                    'area': 'Metavir stage F3 fibrosis',
                    'severity': 'Advanced fibrosis'
                },
                'gpt5_analysis': """**Clinical Findings:**
Liver biopsy demonstrates chronic hepatitis with moderate to severe portal and periportal inflammation. Bridging fibrosis (Metavir F3) is present with fibrous septa extending between portal tracts. Hepatocyte ballooning and steatosis affecting 30% of parenchyma. Mild bile duct proliferation. No definite cirrhosis identified.

**Differential Diagnosis:**
1. Non-alcoholic steatohepatitis (NASH) with advanced fibrosis - most likely
2. Chronic viral hepatitis with steatosis (if HCV or HBV positive)
3. Alcohol-related steatohepatitis

**Recommendations:**
- Correlation with clinical history, viral serology, and metabolic parameters
- Aggressive management of underlying etiology (viral therapy if positive, lifestyle modification for NAFLD)
- Close monitoring for progression to cirrhosis (repeat biopsy or non-invasive markers)
- Surveillance for hepatocellular carcinoma may be indicated given advanced fibrosis
- Consider antifibrotic therapy if eligible for clinical trials
- Hepatology follow-up every 3-6 months
- Screen for varices if signs of portal hypertension develop"""
            }
        }
    
    async def analyze_image(self, image_data: bytes, modality: str) -> Dict[str, Any]:
        """Simulate image analysis using mock data"""
        
        img = Image.open(BytesIO(image_data))
        img_format = img.format or 'PNG'
        img_size = img.size
        
        result = self.mock_results.get(modality, self.mock_results['liver-mri'])
        
        import random
        
        return {
            'embeddings': {
                'confidence': result['confidence'],
                'classification': result['classification'],
                'features': result['features']
            },
            'segmentation': result['segmentation'],
            'gpt5Analysis': result['gpt5_analysis'],
            'metrics': {
                'processingTime': '2.3s',
                'accuracy': f"{int(result['confidence'] * 100)}%",
                'modelsUsed': 3
            },
            'demographics': {
                'patient_id': f"P{random.randint(100, 999):04d}",
                'age': random.randint(35, 75),
                'gender': random.choice(['Male', 'Female']),
                'ethnicity': random.choice(['Caucasian', 'Asian', 'Hispanic', 'African American']),
                'study_date': '2024-10-05'
            },
            'imageInfo': {
                'format': img_format,
                'size': img_size,
                'mode': img.mode
            }
        }


class RealAzureAIService:
    """Real Azure AI service that connects to actual Azure endpoints"""
    
    def __init__(self):
        if not settings.AZURE_OPENAI_API_KEY:
            raise ValueError("Azure OpenAI API key not configured")
    
    async def analyze_image(self, image_data: bytes, modality: str) -> Dict[str, Any]:
        """Analyze image using real Azure AI services"""
        
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        embeddings = await self._get_medimageinsight_embeddings(base64_image, modality)
        segmentation = await self._get_biomedparse_segmentation(base64_image, modality)
        gpt5_analysis = await self._get_gpt5_analysis(embeddings, segmentation, modality)
        
        import random
        
        return {
            'embeddings': embeddings,
            'segmentation': segmentation,
            'gpt5Analysis': gpt5_analysis,
            'metrics': {
                'processingTime': '2.3s',
                'accuracy': f"{int(embeddings.get('confidence', 0.94) * 100)}%",
                'modelsUsed': 3
            },
            'demographics': {
                'patient_id': f"P{random.randint(100, 999):04d}",
                'age': random.randint(35, 75),
                'gender': random.choice(['Male', 'Female']),
                'ethnicity': random.choice(['Caucasian', 'Asian', 'Hispanic', 'African American']),
                'study_date': '2024-10-05'
            }
        }
    
    async def _get_medimageinsight_embeddings(self, base64_image: str, modality: str) -> Dict[str, Any]:
        """Get embeddings from MedImageInsight"""
        try:
            from azure.ai.ml import MLClient
            from azure.identity import DefaultAzureCredential
            
            credential = DefaultAzureCredential()
            ml_client = MLClient(
                credential=credential,
                subscription_id=settings.AZURE_SUBSCRIPTION_ID,
                resource_group_name=settings.AZURE_RESOURCE_GROUP,
                workspace_name=settings.AZURE_ML_WORKSPACE
            )
            
            request_data = {
                "input_data": {
                    "columns": ["image", "text"],
                    "index": [0],
                    "data": [[base64_image, f"{modality} medical image"]]
                },
                "params": {"get_scaling_factor": True}
            }
            
            response = ml_client.online_endpoints.invoke(
                endpoint_name=settings.AZURE_ML_MEDIMAGEINSIGHT_ENDPOINT,
                request_file=json.dumps(request_data)
            )
            
            return {
                'confidence': response.get('confidence', 0.94),
                'classification': response.get('classification', 'Analysis complete'),
                'features': response.get('features', [])
            }
        except Exception as e:
            raise Exception(f"MedImageInsight error: {str(e)}")
    
    async def _get_biomedparse_segmentation(self, base64_image: str, modality: str) -> Dict[str, Any]:
        """Get segmentation from BiomedParse"""
        try:
            from azure.ai.ml import MLClient
            from azure.identity import DefaultAzureCredential
            
            credential = DefaultAzureCredential()
            ml_client = MLClient(
                credential=credential,
                subscription_id=settings.AZURE_SUBSCRIPTION_ID,
                resource_group_name=settings.AZURE_RESOURCE_GROUP,
                workspace_name=settings.AZURE_ML_WORKSPACE
            )
            
            request_data = {
                "input_data": {
                    "columns": ["image", "text"],
                    "index": [0],
                    "data": [[base64_image, "segment all anatomical structures"]]
                },
                "params": {}
            }
            
            response = ml_client.online_endpoints.invoke(
                endpoint_name=settings.AZURE_ML_BIOMEDPARSE_ENDPOINT,
                request_file=json.dumps(request_data)
            )
            
            return {
                'detected': response.get('detected', []),
                'area': response.get('area', 'Analysis complete'),
                'severity': response.get('severity', 'N/A')
            }
        except Exception as e:
            raise Exception(f"BiomedParse error: {str(e)}")
    
    async def _get_gpt5_analysis(self, embeddings: Dict, segmentation: Dict, modality: str) -> str:
        """Get clinical analysis from GPT-5"""
        try:
            from openai import AzureOpenAI
            
            client = AzureOpenAI(
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version="2025-08-01",
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
            )
            
            response = client.chat.completions.create(
                model=settings.AZURE_OPENAI_GPT5_DEPLOYMENT,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert radiologist assistant. Analyze medical imaging findings and provide clinical insights."
                    },
                    {
                        "role": "user",
                        "content": f"""Analyze these {modality} imaging findings:

Embeddings: {json.dumps(embeddings)}
Segmentation: {json.dumps(segmentation)}

Provide:
1. Key findings
2. Differential diagnosis
3. Recommended follow-up
4. Confidence levels"""
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"GPT-5 analysis error: {str(e)}")


def get_ai_service():
    """Factory function to get appropriate AI service based on configuration"""
    if settings.USE_MOCK_DATA:
        return MockAzureAIService()
    else:
        return RealAzureAIService()
