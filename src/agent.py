from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
from src.config import AgentConfig
from src.models import SensorReading, AgentResult
from src.database import Database
from src.sensor import Sensor
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class AgentDependencies:
    config: AgentConfig
    db: Database
    temp_sensor: Sensor
    vib_sensor: Sensor
    noise_sensor: Sensor

construction_agent = Agent(
    'groq:llama3-8b-8192',
    deps_type=AgentDependencies,
    result_type=AgentResult,
    system_prompt=(
        "You are a monitoring agent for a construction site. "
        "The user prompt will provide sensor data in the format: 'Temperature: X°C, Vibration: Y Hz, Noise: Z dB'. "
        "Parse the numerical values for temperature (°C), vibration (Hz), and noise (dB) from the prompt. "
        "If a value is 'N/A' or cannot be parsed as a float, use defaults: 25°C for temperature, 0 Hz for vibration, 0 dB for noise. "
        "Compare each value against the following thresholds exactly as specified: "
        "- shut_down_equipment = True if temperature > {temp_threshold}°C, else False (e.g., 41°C > 40°C is True, 31°C > 40°C is False). "
        "- pause_machinery = True if vibration > {vib_threshold} Hz, else False (e.g., 11 Hz > 10 Hz is True, 8 Hz > 10 Hz is False). "
        "- alert_workers = True if noise > {noise_threshold} dB, else False (e.g., 90 dB > 85 dB is True, 80 dB > 85 dB is False). "
        "Construct a concise message summarizing only the actions to be taken: "
        "- If temperature exceeds threshold: 'Shut down equipment due to high temperature'. "
        "- If vibration exceeds threshold: 'Pause machinery due to high vibration'. "
        "- If noise exceeds threshold: 'Alert workers due to high noise'. "
        "- Combine multiple actions with ' and ' (e.g., 'Shut down equipment due to high temperature and alert workers due to high noise'). "
        "- If no actions are needed, use 'All conditions normal'. "
        "Return a JSON response with: 'shut_down_equipment' (bool), 'pause_machinery' (bool), 'alert_workers' (bool), and 'message' (str). "
        "Ensure 'message' is never empty or null and only lists actions or 'All conditions normal'. "
        "Do not use any tools or functions; directly return the JSON response."
    ),
)

def log_action(db: Database, message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    db.log_action(full_message)