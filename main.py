from dotenv import load_dotenv
from src.app.agent_runner import start_agent_runner
from src.app.routes import app
from threading import Thread

load_dotenv()

if __name__ == "__main__":
    agent_thread = Thread(target=start_agent_runner, daemon=True)
    agent_thread.start()
    app.run(debug=True, host='0.0.0.0', port=5000)