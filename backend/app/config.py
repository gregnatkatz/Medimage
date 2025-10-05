import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    USE_MOCK_DATA: bool = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
    
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_GPT5_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_GPT5_DEPLOYMENT", "gpt-5-deployment")
    
    AZURE_SUBSCRIPTION_ID: str = os.getenv("AZURE_SUBSCRIPTION_ID", "")
    AZURE_RESOURCE_GROUP: str = os.getenv("AZURE_RESOURCE_GROUP", "")
    AZURE_ML_WORKSPACE: str = os.getenv("AZURE_ML_WORKSPACE", "")
    AZURE_ML_MEDIMAGEINSIGHT_ENDPOINT: str = os.getenv("AZURE_ML_MEDIMAGEINSIGHT_ENDPOINT", "")
    AZURE_ML_BIOMEDPARSE_ENDPOINT: str = os.getenv("AZURE_ML_BIOMEDPARSE_ENDPOINT", "")
    
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

settings = Settings()
