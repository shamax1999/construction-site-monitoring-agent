## Reactive AI Agent - Construction Site Monitoring
![screencapture-127-0-0-1-5000-2025-03-17-13_49_08](https://github.com/user-attachments/assets/9aa2b3a4-0d15-4dfb-8d24-b7337dd2b6fc)

A Python-based Reactive AI Agent designed to monitor construction sites in real-time using sensor data (temperature, vibration, noise). Powered by Groq Cloud API and Flask, it detects hazards, triggers actions, and displays results on a web interface.

## Features

- **Real-Time Monitoring:** Tracks temperature (°C), vibration (Hz), and noise (dB) via simulated or real sensors.
- **Hazard Detection:** Flags risks (e.g., Temp > 40°C, Noise > 85 dB) with configurable thresholds.
- **AI-Driven Actions:** Decides to shut down equipment, pause machinery, or alert workers.
- **Web Dashboard:** Displays live sensor data and agent decisions.

## Prerequisites
- **Python 3.8+**
- **PostgreSQL** 
- **Groq Cloud API Key** (set in `.env`)
- **Dependencies:** `flask`, `psycopg2`, `pydantic`, `groq` (see `requirements.txt`)

## Setup
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/shamax1999/construction-site-monitoring-agent.git
   cd construction-site-monitoring-agent
   ```

2. **Create Virtual Environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the root directory:
   ```
   DB_NAME=construction_site_db
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   TEMP_THRESHOLD=40.0
   VIB_THRESHOLD=10.0
   NOISE_THRESHOLD=85.0
   NOISE_DURATION=30.0
   CHECK_INTERVAL=5.0
   GROQ_API_KEY=your_groq_api_key
   ```

5. **Run the Application:**
   ```bash
   python main.py
   ```
   - The agent runs in a thread, and the Flask server starts at `http://localhost:5000`.

## Usage
- **Web Interface:** Open `http://localhost:5000` to view real-time sensor data and agent actions.
- **Sample Output:** 
  - "Temperature: 31.31°C, Vibration: 8.36 Hz, Noise: 89.08 dB - Alert workers due to high noise."
- **Logs:** Check `agent_log.txt` or the PostgreSQL database for event history.
