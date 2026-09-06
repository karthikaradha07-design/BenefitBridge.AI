from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    lyzr_api_key: str = ""
    lyzr_agent_id: str = ""
    lyzr_api_url: str = "https://agent.api.lyzr.app/v2/chat/"
    qdrant_url: str = ""
    qdrant_api_key: str = ""
    qdrant_collection: str = "benefitbridge_schemes"
    frontend_origin: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
