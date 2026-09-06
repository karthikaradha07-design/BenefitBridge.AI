from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    demo_mode: bool = True
    lyzr_api_key: str = ""
    lyzr_agent_id: str = ""
    lyzr_api_url: str = "https://agent.api.lyzr.app/v2/chat/"
    enkrypt_api_key: str = ""
    enkrypt_api_url: str = ""
    qdrant_url: str = ""
    qdrant_api_key: str = ""
    qdrant_collection: str = "benefitbridge_schemes"
    database_url: str = "sqlite:///./govscheme.db"
    frontend_origin: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
