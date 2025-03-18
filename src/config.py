from pydantic import BaseModel, Field

class AgentConfig(BaseModel):
    temp_threshold: float = Field(default=40.0, ge=0, le=100, description="Max temperature in °C")
    vib_threshold: float = Field(default=10.0, ge=0, le=50, description="Max vibration in Hz")
    noise_threshold: float = Field(default=85.0, ge=0, le=150, description="Max noise in dB")
    noise_duration: float = Field(default=30.0, ge=0, description="Noise duration in seconds")
    check_interval: float = Field(default=5.0, gt=0, description="Interval between checks in seconds")

class DatabaseConfig(BaseModel):
    dbname: str = Field(..., description="Database name")
    user: str = Field(..., description="Database user")
    password: str = Field(..., description="Database password")
    host: str = Field(default="localhost", description="Database host")
    port: str = Field(default="5432", description="Database port")