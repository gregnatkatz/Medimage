"""
Deploy MedImageParse and MedImageInsight to Azure AI Foundry

Before running this script, set your environment variables:
export FOUNDRY_ENDPOINT="https://rickwey-aifndry395948420204.services.ai.azure.com"
export FOUNDRY_API_KEY="your-foundry-api-key"
export AZURE_ML_ENDPOINT_NAME="medparse101-gnk"
export AZURE_ML_ENDPOINT="https://medparse101-gnk.eastus2.inference.ml.azure.com/score"
export AZURE_ML_API_KEY="your-ml-api-key"
"""

import os
import time
import json
import requests
from azure.ai.ml import MLClient
from azure.ai.ml.entities import ManagedOnlineDeployment, ManagedOnlineEndpoint
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError


FOUNDRY_ENDPOINT = os.getenv("FOUNDRY_ENDPOINT", "https://rickwey-aifndry395948420204.services.ai.azure.com")
FOUNDRY_API_KEY = os.getenv("FOUNDRY_API_KEY", "")

ML_ENDPOINT_NAME = os.getenv("AZURE_ML_ENDPOINT_NAME", "medparse101-gnk")
ML_ENDPOINT_URI = os.getenv("AZURE_ML_ENDPOINT", "https://medparse101-gnk.eastus2.inference.ml.azure.com/score")
ML_API_KEY = os.getenv("AZURE_ML_API_KEY", "")


MODELS_TO_DEPLOY = [
    {
        "name": "MedImageParse3D",
        "model_id": "azureml://registries/azureml/models/MedImageParse3D/versions/latest",
        "description": "3D medical image segmentation"
    },
    {
        "name": "MedImageParse",
        "model_id": "azureml://registries/azureml/models/MedImageParse/versions/latest",
        "description": "2D medical image segmentation"
    },
    {
        "name": "MedImageInsight",
        "model_id": "azureml://registries/azureml/models/MedImageInsight/versions/latest",
        "description": "Medical image embeddings"
    }
]

USE_SHARED_QUOTA = True  # Set to True for temporary testing (168 hours)
INSTANCE_TYPE = "Standard_NC6s_v3"  # GPU option
INSTANCE_COUNT = 1


def test_foundry_connection():
    """Test connection to Azure AI Foundry"""
    print("\n🧪 Testing Azure AI Foundry connection...")
    
    headers = {
        "Content-Type": "application/json",
        "api-key": FOUNDRY_API_KEY
    }
    
    try:
        models_url = f"{FOUNDRY_ENDPOINT}/models"
        response = requests.get(models_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Connection successful!")
            return True
        elif response.status_code == 401:
            print(f"❌ Authentication failed - check your API key")
            return False
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection failed: {str(e)}")
        return False


def deploy_model_foundry(model_config):
    """Deploy a model using Azure AI Foundry"""
    print(f"\n🚀 Deploying {model_config['name']} to Azure AI Foundry...")
    
    headers = {
        "Content-Type": "application/json",
        "api-key": FOUNDRY_API_KEY
    }
    
    deployment_data = {
        "model": model_config["model_id"],
        "sku": {
            "name": INSTANCE_TYPE,
            "capacity": INSTANCE_COUNT
        },
        "properties": {
            "description": model_config["description"]
        }
    }
    
    if USE_SHARED_QUOTA:
        deployment_data["properties"]["useSharedQuota"] = True
        print(f"   ⚠️ Using shared quota - endpoint will expire in 168 hours")
    
    try:
        deploy_url = f"{FOUNDRY_ENDPOINT}/models/deployments"
        response = requests.post(
            deploy_url,
            headers=headers,
            json=deployment_data,
            timeout=300
        )
        
        if response.status_code in [200, 201, 202]:
            print(f"✅ Deployment initiated for {model_config['name']}")
            result = response.json()
            return result
        else:
            print(f"❌ Deployment failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error deploying {model_config['name']}: {str(e)}")
        return None


def deploy_via_azure_ml():
    """Alternative: Deploy using Azure ML SDK"""
    print("\n" + "=" * 70)
    print("Deploying via Azure Machine Learning")
    print("=" * 70)
    
    try:
        credential = DefaultAzureCredential()
        ml_client = MLClient.from_config(credential)
        print("✅ Azure ML authentication successful!")
        
        endpoint = ManagedOnlineEndpoint(
            name=ML_ENDPOINT_NAME,
            description="Medical imaging models endpoint",
            auth_mode="key"
        )
        
        endpoint = ml_client.online_endpoints.begin_create_or_update(endpoint).result()
        print(f"✅ Endpoint ready: {ML_ENDPOINT_NAME}")
        
        for model in MODELS_TO_DEPLOY:
            deployment_name = f"{model['name'].lower()}-deployment"
            
            deployment = ManagedOnlineDeployment(
                name=deployment_name,
                endpoint_name=ML_ENDPOINT_NAME,
                model=model["model_id"],
                instance_type=INSTANCE_TYPE,
                instance_count=INSTANCE_COUNT,
                description=model["description"]
            )
            
            print(f"\n🚀 Deploying {deployment_name}...")
            ml_client.online_deployments.begin_create_or_update(deployment).result()
            print(f"✅ {deployment_name} deployed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Azure ML deployment failed: {str(e)}")
        return False


def list_foundry_deployments():
    """List all deployments in Azure AI Foundry"""
    print("\n📋 Checking Azure AI Foundry deployments...")
    
    headers = {
        "Content-Type": "application/json",
        "api-key": FOUNDRY_API_KEY
    }
    
    try:
        list_url = f"{FOUNDRY_ENDPOINT}/models/deployments"
        response = requests.get(list_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            deployments = response.json()
            if deployments:
                print(f"✅ Found {len(deployments)} deployment(s):")
                for dep in deployments:
                    print(f"   - {dep.get('name', 'unknown')}")
                return deployments
            else:
                print("   No deployments found")
                return []
        else:
            print(f"⚠️ Could not list deployments: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error listing deployments: {str(e)}")
        return []


def print_usage_instructions():
    """Print usage instructions"""
    print("\n" + "=" * 70)
    print("Usage Instructions")
    print("=" * 70)
    
    print("\n🐍 Python Example - Azure AI Foundry:")
    print(f"""
import requests
import json
import base64
import os

foundry_endpoint = os.getenv("FOUNDRY_ENDPOINT")
api_key = os.getenv("FOUNDRY_API_KEY")

with open("image.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

data = {{
    "input_data": {{
        "columns": ["image", "text"],
        "data": [[image_data, "segment liver"]]
    }}
}}

headers = {{
    "Content-Type": "application/json",
    "api-key": api_key
}}

response = requests.post(
    f"{{foundry_endpoint}}/models/MedImageParse/predict",
    headers=headers,
    json=data
)

print(response.json())
""")

    print("\n🐍 Python Example - Azure ML Endpoint:")
    print(f"""
import requests
import json
import os

ml_endpoint = os.getenv("AZURE_ML_ENDPOINT")
ml_api_key = os.getenv("AZURE_ML_API_KEY")

headers = {{
    "Content-Type": "application/json",
    "Authorization": f"Bearer {{ml_api_key}}",
    "azureml-model-deployment": "medimageparse-deployment"  # Specify which model
}}

response = requests.post(
    ml_endpoint,
    headers=headers,
    json=data
)
""")


def main():
    print("=" * 70)
    print("Azure AI Foundry - Medical Imaging Models Deployment")
    print("=" * 70)
    
    if not FOUNDRY_API_KEY or not ML_API_KEY:
        print("\n❌ Error: Required environment variables not set")
        print("\nPlease set the required environment variables:")
        print("  export FOUNDRY_ENDPOINT='https://rickwey-aifndry395948420204.services.ai.azure.com'")
        print("  export FOUNDRY_API_KEY='your-foundry-api-key'")
        print("  export AZURE_ML_ENDPOINT_NAME='medparse101-gnk'")
        print("  export AZURE_ML_ENDPOINT='https://medparse101-gnk.eastus2.inference.ml.azure.com/score'")
        print("  export AZURE_ML_API_KEY='your-ml-api-key'")
        return
    
    print(f"\n🎯 Azure AI Foundry Endpoint: {FOUNDRY_ENDPOINT}")
    print(f"🔑 API Key: {'*' * 50}...{FOUNDRY_API_KEY[-10:]}")
    print(f"\n💻 VM Type: {INSTANCE_TYPE}")
    print(f"📦 Shared Quota: {'Yes (168hr limit)' if USE_SHARED_QUOTA else 'No (dedicated)'}")
    
    if not test_foundry_connection():
        print("\n⚠️ Connection test failed. Trying Azure ML deployment instead...")
        deploy_via_azure_ml()
        return
    
    existing = list_foundry_deployments()
    
    print("\n" + "=" * 70)
    print("Deployment Options")
    print("=" * 70)
    print("\n1. Deploy via Azure AI Foundry Portal (Recommended)")
    print("2. Deploy via Azure ML SDK")
    print("3. Show usage instructions only")
    
    choice = input("\nSelect option (1/2/3): ").strip()
    
    if choice == "1":
        print("\n📖 To deploy via Azure AI Foundry Portal:")
        print("\n1. Go to: https://ai.azure.com")
        print("2. Navigate to: Model catalog")
        print("3. Search for: MedImageParse, MedImageParse3D, MedImageInsight")
        print("4. Click: Deploy")
        print("5. Choose: Managed compute")
        if USE_SHARED_QUOTA:
            print("6. Check: ☑️ 'I want to use shared quota (168 hours)'")
        print("7. Select VM size and deploy")
        
    elif choice == "2":
        deploy_via_azure_ml()
        
    elif choice == "3":
        print_usage_instructions()
    
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"\n✅ Azure AI Foundry endpoint is accessible")
    print(f"🌐 Endpoint: {FOUNDRY_ENDPOINT}")
    print(f"\n💡 Models to deploy:")
    for model in MODELS_TO_DEPLOY:
        print(f"   - {model['name']}: {model['description']}")
    
    print("\n⚠️ SECURITY REMINDER:")
    print("   - Don't share your API keys publicly")
    print("   - Rotate keys regularly")
    print("   - Use environment variables in production")
    
    print_usage_instructions()


if __name__ == "__main__":
    main()
