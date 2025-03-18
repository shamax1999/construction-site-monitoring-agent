from pydantic import BaseModel, Field
from typing import Optional

class SensorReading(BaseModel):
    temperature: Optional[float] = Field(default=None, ge=0, le=100, description="Temperature in °C")
    vibration: Optional[float] = Field(default=None, ge=0, le=50, description="Vibration in Hz")
    noise: Optional[float] = Field(default=None, ge=0, le=150, description="Noise in dB")

class AgentResult(BaseModel):
    shut_down_equipment: bool = Field(description="Whether to shut down equipment due to high temperature")
    pause_machinery: bool = Field(description="Whether to pause machinery due to high vibration")
    alert_workers: bool = Field(description="Whether to alert workers due to prolonged high noise")
    message: str = Field(default="No message provided", description="Action message or status")