from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Enterprise AI Procurement Agent"
    environment: str = "development"
    anomaly_threshold_pct: float = 25.0


settings = Settings()
