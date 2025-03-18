import os
import time
from threading import Lock
from src.config import AgentConfig, DatabaseConfig
from src.database import Database
from src.sensor import Sensor
from src.agent import AgentDependencies, construction_agent, log_action
from src.models import AgentResult, SensorReading

latest_data = {
    "temperature": None,
    "vibration": None,
    "noise": None,
    "agent_result": None,
    "timestamp": None
}
data_lock = Lock()

def start_agent_runner():
    try:
        db_config = DatabaseConfig(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432")
        )
        db = Database(db_config)

        config = AgentConfig(
            temp_threshold=float(os.getenv("TEMP_THRESHOLD", 40.0)),
            vib_threshold=float(os.getenv("VIB_THRESHOLD", 10.0)),
            noise_threshold=float(os.getenv("NOISE_THRESHOLD", 85.0)),
            noise_duration=float(os.getenv("NOISE_DURATION", 30.0)),
            check_interval=float(os.getenv("CHECK_INTERVAL", 5.0))
        )

        temp_sensor = Sensor(20, 50)
        vib_sensor = Sensor(0, 15)
        noise_sensor = Sensor(60, 100)

        deps = AgentDependencies(
            config=config,
            db=db,
            temp_sensor=temp_sensor,
            vib_sensor=vib_sensor,
            noise_sensor=noise_sensor
        )

        log_action(db, "Reactive Agent started")
        while True:
            try:
                sensor_reading = SensorReading(
                    temperature=deps.temp_sensor.read(),
                    vibration=deps.vib_sensor.read(),
                    noise=deps.noise_sensor.read()
                )
                print(f"Captured sensor data: {sensor_reading.model_dump()}")

                sensor_string = (
                    f"Temperature: {sensor_reading.temperature if sensor_reading.temperature is not None else 'N/A'}°C, "
                    f"Vibration: {sensor_reading.vibration if sensor_reading.vibration is not None else 'N/A'} Hz, "
                    f"Noise: {sensor_reading.noise if sensor_reading.noise is not None else 'N/A'} dB"
                )

                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        agent_response = construction_agent.run_sync(
                            f"Analyze these sensor readings and decide on actions: {sensor_string}",
                            deps=deps
                        )
                        print(f"Agent raw response: {agent_response}")
                        result = agent_response.data
                        break
                    except Exception as e:
                        if "tool_use_failed" in str(e) and attempt < max_retries - 1:
                            log_action(db, f"Retrying agent due to tool-use error: {str(e)}")
                            time.sleep(1)
                            continue
                        else:
                            raise

                with data_lock:
                    latest_data["temperature"] = sensor_reading.temperature
                    latest_data["vibration"] = sensor_reading.vibration
                    latest_data["noise"] = sensor_reading.noise
                    latest_data["agent_result"] = result.model_dump()
                    latest_data["timestamp"] = time.time()

                log_action(db, result.message)
                print("Latest data:", latest_data)

            except Exception as inner_e:
                error_msg = f"Agent error: {str(inner_e)}"
                log_action(db, error_msg)
                with data_lock:
                    error_result = AgentResult(
                        shut_down_equipment=False,
                        pause_machinery=False,
                        alert_workers=False,
                        message=error_msg
                    )
                    latest_data["temperature"] = None
                    latest_data["vibration"] = None
                    latest_data["noise"] = None
                    latest_data["agent_result"] = error_result.model_dump()
                    latest_data["timestamp"] = time.time()

            time.sleep(config.check_interval)

    except Exception as e:
        log_action(db, f"ERROR: Agent crashed - {str(e)}")
        db.close()

def get_latest_data():
    with data_lock:
        return latest_data.copy()