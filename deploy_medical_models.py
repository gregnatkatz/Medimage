"""
Script to add MedImageParse and MedImageInsight deployments 
to an existing Azure ML endpoint with MedImageParse3D
"""

import time
import json
import os
import requests
from azure.ai.ml import MLClient
from azure.ai.ml.entities import ManagedOnlineDeployment
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError


ENDPOINT_NAME = os.getenv("AZURE_ML_ENDPOINT_NAME", "medparse101-gnk")
ENDPOINT_URI = os.getenv("AZURE_ML_ENDPOINT", "https://medparse101-gnk.eastus2.inference.ml.azure.com/score")
API_KEY = os.getenv("AZURE_ML_API_KEY", "")

EXISTING_DEPLOYMENT_NAME = "medimageparse3d"

DEPLOYMENTS_TO_ADD = [
    {
        "name": "medimageparse-deployment",
        "model": "azureml://registries/azureml/models/MedImageParse/versions/latest",
        "description": "MedImageParse 2D segmentation model"
    },
    {
        "name": "medimageinsight-deployment", 
        "model": "azureml://registries/azureml/models/MedImageInsight/versions/latest",
        "description": "MedImageInsight embedding model"
    }
]

INSTANCE_TYPE = "Standard_NC24ads_A100_v4"
INSTANCE_COUNT = 1


def check_deployment_status(ml_client, endpoint_name, deployment_name):
    """Check if a deployment is ready"""
    try:
        deployment = ml_client.online_deployments.get(
            name=deployment_name,
            endpoint_name=endpoint_name
        )
        return deployment.provisioning_state
    except ResourceNotFoundError:
        return "NotFound"


def wait_for_deployment(ml_client, endpoint_name, deployment_name, timeout=1800):
    """Wait for a deployment to complete (default 30 min timeout)"""
    print(f"⏳ Waiting for deployment '{deployment_name}' to complete...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        status = check_deployment_status(ml_client, endpoint_name, deployment_name)
        
        if status == "Succeeded":
            print(f"✅ Deployment '{deployment_name}' completed successfully!")
            return True
        elif status == "Failed":
            print(f"❌ Deployment '{deployment_name}' failed!")
            return False
        elif status == "NotFound":
            print(f"❌ Deployment '{deployment_name}' not found!")
            return False
        else:
            elapsed = int(time.time() - start_time)
            print(f"   Status: {status} - Elapsed: {elapsed}s / {timeout}s")
            time.sleep(30)
    
    print(f"⏱️ Timeout waiting for deployment '{deployment_name}'")
    return False


def create_deployment(ml_client, endpoint_name, deployment_config):
    """Create a new deployment"""
    print(f"\n🚀 Creating deployment: {deployment_config['name']}")
    print(f"   Model: {deployment_config['model']}")
    print(f"   Instance: {INSTANCE_TYPE} x {INSTANCE_COUNT}")
    
    deployment = ManagedOnlineDeployment(
        name=deployment_config["name"],
        endpoint_name=endpoint_name,
        model=deployment_config["model"],
        instance_type=INSTANCE_TYPE,
        instance_count=INSTANCE_COUNT,
        description=deployment_config.get("description", "")
    )
    
    try:
        poller = ml_client.online_deployments.begin_create_or_update(deployment)
        result = poller.result()
        print(f"✅ Deployment '{deployment_config['name']}' created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating deployment '{deployment_config['name']}': {str(e)}")
        return False


def update_traffic(ml_client, endpoint_name, traffic_config):
    """Update traffic allocation across deployments"""
    print(f"\n🔄 Updating traffic allocation...")
    
    try:
        endpoint = ml_client.online_endpoints.get(name=endpoint_name)
        endpoint.traffic = traffic_config
        
        ml_client.online_endpoints.begin_create_or_update(endpoint).result()
        print(f"✅ Traffic updated successfully!")
        print(f"   Traffic allocation:")
        for name, percent in traffic_config.items():
            print(f"      {name}: {percent}%")
        return True
    except Exception as e:
        print(f"❌ Error updating traffic: {str(e)}")
        return False


def list_endpoint_deployments(ml_client, endpoint_name):
    """List all deployments for an endpoint"""
    print(f"\n📋 Current deployments for endpoint '{endpoint_name}':")
    try:
        deployments = ml_client.online_deployments.list(endpoint_name=endpoint_name)
        deployment_list = []
        for deployment in deployments:
            print(f"   - {deployment.name}")
            print(f"     Status: {deployment.provisioning_state}")
            print(f"     Instance: {deployment.instance_type} x {deployment.instance_count}")
            deployment_list.append(deployment.name)
        return deployment_list
    except Exception as e:
        print(f"❌ Error listing deployments: {str(e)}")
        return []


def test_endpoint_connection(endpoint_uri, api_key, deployment_name=None):
    """Test endpoint connectivity"""
    print(f"\n🧪 Testing endpoint connection...")
    print(f"   URI: {endpoint_uri}")
    if deployment_name:
        print(f"   Target deployment: {deployment_name}")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    if deployment_name:
        headers["azureml-model-deployment"] = deployment_name
    
    test_data = {
        "input_data": {
            "columns": ["image", "text"],
            "index": [0],
            "data": [["", "test"]]
        }
    }
    
    try:
        response = requests.post(
            endpoint_uri,
            headers=headers,
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"✅ Endpoint is responding (200 OK)")
            return True
        else:
            print(f"⚠️ Endpoint returned status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection test failed: {str(e)}")
        return False


def main():
    print("=" * 70)
    print("Azure ML Medical Imaging Models - Multi-Deployment Setup")
    print("=" * 70)
    print(f"\n🎯 Endpoint: {ENDPOINT_NAME}")
    print(f"🌐 URI: {ENDPOINT_URI}")
    print(f"🔑 API Key: {'*' * 40}...{API_KEY[-10:]}")
    
    print("\n🔐 Authenticating with Azure...")
    try:
        credential = DefaultAzureCredential()
        ml_client = MLClient.from_config(credential)
        print("✅ Authentication successful!")
    except Exception as e:
        print(f"❌ Authentication failed: {str(e)}")
        print("\n💡 Tip: Run 'az login' in your terminal first")
        return
    
    print(f"\n" + "=" * 70)
    print(f"Step 1: Checking Existing Deployment")
    print("=" * 70)
    print(f"\n📊 Checking status of '{EXISTING_DEPLOYMENT_NAME}'...")
    existing_status = check_deployment_status(ml_client, ENDPOINT_NAME, EXISTING_DEPLOYMENT_NAME)
    print(f"   Current status: {existing_status}")
    
    if existing_status not in ["Succeeded", "Creating", "Updating"]:
        print(f"❌ Existing deployment is in unexpected state: {existing_status}")
        print("   Please check your deployment in Azure Portal.")
        return
    
    if existing_status != "Succeeded":
        if not wait_for_deployment(ml_client, ENDPOINT_NAME, EXISTING_DEPLOYMENT_NAME):
            print("❌ Existing deployment did not complete successfully. Exiting.")
            return
    
    print(f"\n" + "=" * 70)
    print(f"Step 2: Current Deployment Status")
    print("=" * 70)
    list_endpoint_deployments(ml_client, ENDPOINT_NAME)
    
    print(f"\n" + "=" * 70)
    print(f"Step 3: Testing Endpoint Connectivity")
    print("=" * 70)
    test_endpoint_connection(ENDPOINT_URI, API_KEY, EXISTING_DEPLOYMENT_NAME)
    
    print("\n" + "=" * 70)
    print("Step 4: Adding New Deployments")
    print("=" * 70)
    
    successful_deployments = [EXISTING_DEPLOYMENT_NAME]
    
    for i, deployment_config in enumerate(DEPLOYMENTS_TO_ADD, 1):
        print(f"\n[{i}/{len(DEPLOYMENTS_TO_ADD)}] Processing: {deployment_config['name']}")
        
        if create_deployment(ml_client, ENDPOINT_NAME, deployment_config):
            if wait_for_deployment(ml_client, ENDPOINT_NAME, deployment_config["name"]):
                successful_deployments.append(deployment_config["name"])
                test_endpoint_connection(ENDPOINT_URI, API_KEY, deployment_config["name"])
            else:
                print(f"⚠️ Warning: Deployment '{deployment_config['name']}' may not be ready")
        else:
            print(f"⚠️ Skipping wait for '{deployment_config['name']}' due to creation error")
    
    print("\n" + "=" * 70)
    print("Step 5: Configuring Traffic Routing")
    print("=" * 70)
    
    if len(successful_deployments) > 1:
        print(f"\n✅ Successfully deployed {len(successful_deployments)} models:")
        for name in successful_deployments:
            print(f"   - {name}")
        
        equal_split = {name: int(100 / len(successful_deployments)) 
                      for name in successful_deployments}
        
        total = sum(equal_split.values())
        if total != 100:
            equal_split[successful_deployments[0]] += (100 - total)
        
        print(f"\n📊 Traffic allocation options:")
        print(f"\n   Option 1 - Equal split:")
        for name, percent in equal_split.items():
            print(f"      {name}: {percent}%")
        
        print(f"\n   Option 2 - Keep original 100%, new at 0%:")
        print(f"      {EXISTING_DEPLOYMENT_NAME}: 100%")
        for name in successful_deployments[1:]:
            print(f"      {name}: 0%")
        
        print(f"\n   Option 3 - Skip traffic configuration (manual setup)")
        
        choice = input("\nSelect option (1/2/3): ").strip()
        
        if choice == "1":
            update_traffic(ml_client, ENDPOINT_NAME, equal_split)
        elif choice == "2":
            traffic_split = {EXISTING_DEPLOYMENT_NAME: 100}
            for name in successful_deployments[1:]:
                traffic_split[name] = 0
            update_traffic(ml_client, ENDPOINT_NAME, traffic_split)
        else:
            print("⏭️ Skipping traffic configuration. You can set this manually later.")
    
    print("\n" + "=" * 70)
    print("Final Deployment Summary")
    print("=" * 70)
    
    final_deployments = list_endpoint_deployments(ml_client, ENDPOINT_NAME)
    
    print("\n" + "=" * 70)
    print("Usage Examples")
    print("=" * 70)
    
    print(f"\n🐍 Python Example:")
    print(f"""
import requests
import json

endpoint_uri = "{ENDPOINT_URI}"
api_key = "{API_KEY[:20]}...{API_KEY[-10:]}"

headers = {{
    "Content-Type": "application/json",
    "Authorization": f"Bearer {{api_key}}",
    "azureml-model-deployment": "<deployment-name>"
}}

data = {{
    "input_data": {{
        "columns": ["image", "text"],
        "data": [[image_base64, "prompt"]]
    }}
}}

response = requests.post(endpoint_uri, headers=headers, json=data)
print(response.json())
""")
    
    print(f"\n📦 Available deployments to route to:")
    for name in final_deployments:
        print(f"   - {name}")
    
    print(f"\n⚠️ SECURITY NOTE: Keep your API key secure and don't share it publicly!")
    print("\n✅ Script completed successfully!")


if __name__ == "__main__":
    main()
