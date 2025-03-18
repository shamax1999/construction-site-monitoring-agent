function updateData() {
    fetch('/data')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            console.log("Received data:", data);
            document.getElementById('temperature').textContent =
                data.temperature !== null && data.temperature !== undefined ? data.temperature.toFixed(2) : '--';
            document.getElementById('vibration').textContent =
                data.vibration !== null && data.vibration !== undefined ? data.vibration.toFixed(2) : '--';
            document.getElementById('noise').textContent =
                data.noise !== null && data.noise !== undefined ? data.noise.toFixed(2) : '--';

            const shutDown = document.getElementById('shut_down');
            const pause = document.getElementById('pause');
            const alert = document.getElementById('alert');
            const message = document.getElementById('message');

            if (data.agent_result && typeof data.agent_result === 'object') {
                shutDown.textContent = data.agent_result.shut_down_equipment ? 'Yes' : 'No';
                shutDown.className = 'status ' + (data.agent_result.shut_down_equipment ? 'yes' : 'no');
                pause.textContent = data.agent_result.pause_machinery ? 'Yes' : 'No';
                pause.className = 'status ' + (data.agent_result.pause_machinery ? 'yes' : 'no');
                alert.textContent = data.agent_result.alert_workers ? 'Yes' : 'No';
                alert.className = 'status ' + (data.agent_result.alert_workers ? 'yes' : 'no');
                message.textContent = data.agent_result.message || 'No message available';
            } else {
                shutDown.textContent = '--';
                shutDown.className = 'status';
                pause.textContent = '--';
                pause.className = 'status';
                alert.textContent = '--';
                alert.className = 'status';
                message.textContent = 'Awaiting agent response';
            }

            document.getElementById('last-updated').textContent = new Date().toLocaleTimeString();
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            document.getElementById('temperature').textContent = '--';
            document.getElementById('vibration').textContent = '--';
            document.getElementById('noise').textContent = '--';
            document.getElementById('shut_down').textContent = '--';
            document.getElementById('pause').textContent = '--';
            document.getElementById('alert').textContent = '--';
            document.getElementById('message').textContent = 'Error fetching data';
        });
}

updateData();
setInterval(updateData, 6000);