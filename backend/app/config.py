import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    USE_MOCK_DATA: bool = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
    
    AZURE_TENANT_ID: str = os.getenv("AZURE_TENANT_ID", "")
    AZURE_CLIENT_ID: str = os.getenv("AZURE_CLIENT_ID", "")
    AZURE_CLIENT_SECRET: str = os.getenv("AZURE_CLIENT_SECRET", "")
    
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")
    AZURE_OPENAI_DEPLOYMENT_NAME: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4.1")
    
    AZURE_ML_ENDPOINT: str = os.getenv("AZURE_ML_ENDPOINT", "")
    AZURE_ML_API_KEY: str = os.getenv("AZURE_ML_API_KEY", "")
    
    MEDIMAGEPARSE_DEPLOYMENT: str = os.getenv("MEDIMAGEPARSE_DEPLOYMENT", "medimageparse-deployment")
    MEDIMAGEINSIGHT_DEPLOYMENT: str = os.getenv("MEDIMAGEINSIGHT_DEPLOYMENT", "medimageinsight-deployment")
    MEDIMAGEPARSE3D_DEPLOYMENT: str = os.getenv("MEDIMAGEPARSE3D_DEPLOYMENT", "medimageparse3d")
    
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

settings = Settings()
