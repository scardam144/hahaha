from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
import json
import subprocess
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)


def ping_ip(ip):
    try:
        ping_command = ["ping6", "-c", "4", ip]
        result = subprocess.run(ping_command, capture_output=True, text=True)

        if "100% packet loss" not in result.stdout:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def update_results():
    with open("ipv6.json", "r") as file:
        data = json.load(file)

    ipv6_array = data["ipv6"]

    results = {}
    for ip in ipv6_array:
        results[ip] = ping_ip(ip)

    return results


def update_loop():
    while True:
        results = update_results()
        socketio.emit('update', {'results': results})
        time.sleep(60)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    results = update_results()
    socketio.emit('update', {'results': results})


# Add a route to serve static files
@app.route('/lib/<path:filename>')
def serve_file(filename):
    return send_from_directory('lib', filename)


if __name__ == '__main__':
    update_thread = threading.Thread(target=update_loop)
    update_thread.daemon = True
    update_thread.start()

    socketio.run(app, host='0.0.0.0', port=8080)
