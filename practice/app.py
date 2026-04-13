from flask import Flask, render_template
from flask_socketio import SocketIO #main websocket library for real-time communication
import time
import threading # run background tasks without blocking the main thread

app = Flask(__name__)
socketio = SocketIO(app)# attactch socket io to our flask app

@app.route('/')
def index():
    return render_template('index.html') # opens index.html when we access the root URL

# 🔥 Background task (runs continuously)
def send_data():
    count = 0
    while True:
        count += 1

        # Send data to frontend
        socketio.emit('update', {'count': count})

        time.sleep(1)

# Start background thread
threading.Thread(target=send_data).start()
# With thread:

# Flask runs normally
# Background task runs separately

if __name__ == '__main__':
    socketio.run(app, debug=True)