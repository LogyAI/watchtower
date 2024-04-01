import requests
import psutil
import threading
import time
import sys
import os

class ServerPinger:
    def __init__(self, server_id):
        self.server_url = "https://status.logy.ai"
        self.server_id = server_id

    def get_system_usage(self):
        """Retrieve the current system's CPU and RAM usage."""
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        return {'cpu': cpu_usage, 'ram': ram_usage}

    def send_ping(self):
        """Send a ping to the server along with the system's CPU and RAM usage."""
        system_usage = self.get_system_usage()

        try:
            response = requests.post(
                f"{self.server_url}/ping",
                json={
                    "server_id": self.server_id,
                    "cpu_usage": system_usage['cpu'],
                    "ram_usage": system_usage['ram']
                }
            )
            print(f"Ping response: {response.status_code}, {response.json()}")
        except Exception as e:
            print(f"Error pinging {self.server_url}: {e}")

    def start_pinging(self, interval=10):
        """Start pinging the server at regular intervals."""
        def run():
            while True:
                self.send_ping()
                time.sleep(interval)
        
        thread = threading.Thread(target=run)
        thread.daemon = True  # Daemonize thread
        thread.start()

os.system("cd watchtower; git pull")
