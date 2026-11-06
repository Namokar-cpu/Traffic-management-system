from pathlib import Path
from flask import Flask, render_template, Response
from backend.cameras import (
    capEast,
    capNorth,
    capSouth,
    capWest,
    eastVehicles,
    generate_frames,
    northVehicles,
    southVehicles,
    trackerEast,
    trackerNorth,
    trackerSouth,
    trackerWest,
    westVehicles,
)
from flask_socketio import SocketIO
import time

PROJECT_ROOT = Path(__file__).resolve().parents[1]
app = Flask(
    __name__,
    template_folder=str(PROJECT_ROOT / "frontend" / "templates"),
    static_folder=str(PROJECT_ROOT / "frontend" / "static"),
)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# ==============================
# SIGNAL MANAGEMENT
# ==============================
SIGNAL_DURATION = 15  # Duration each signal stays GREEN (in seconds)
FRAME_SKIP = 2  # Process every Nth frame to reduce load
last_switch_time = 0
signal_direction_order = ["north", "south", "east", "west"]
current_active_direction = 0

current_signal = {
    "north": "RED",
    "south": "RED",
    "east": "RED",
    "west": "RED"
}
traffic_data = {
    "north": 0,
    "south": 0,
    "east": 0,
    "west": 0
}

def decide_signal_adaptive(north, south, east, west):
    """
    Adaptive signal decision based on traffic volume
    """
    data = {
        "north": north,
        "south": south,
        "east": east,
        "west": west
    }
    
    # Find direction with most vehicles
    active = max(data, key=data.get)
    
    signals = {}
    for d in data:
        signals[d] = "GREEN" if d == active else "RED"
    
    return signals, active


def get_time_remaining(elapsed):
    """Calculate remaining time for current signal"""
    return max(0, SIGNAL_DURATION - elapsed)


def update_signals():
    """Centralized signal update logic - called from each camera feed"""
    global last_switch_time, current_signal, current_active_direction
    
    now = time.time()
    elapsed = now - last_switch_time
    
    # Switch signal when duration expires
    if elapsed > SIGNAL_DURATION:
        current_signal, active_dir = decide_signal_adaptive(
            traffic_data["north"],
            traffic_data["south"],
            traffic_data["east"],
            traffic_data["west"]
        )
        last_switch_time = now
    
    # Calculate time remaining
    time_remaining = get_time_remaining(elapsed)
    
    return current_signal, time_remaining
# Home page
@app.route('/')
def index():
    return render_template("index.html")


# ==============================
# NORTH CAMERA
# ==============================
@app.route('/video/north')
def video_north():

    def generate():
        for frame, cars, trucks, bikes in generate_frames(capNorth, trackerNorth, northVehicles):

            traffic_data["north"] = cars + trucks + bikes

            # Get updated signals and time remaining
            signals, time_remaining = update_signals()
            signal = signals["north"]

            socketio.emit('traffic_update', {
                "direction": "north",
                "cars": cars,
                "trucks": trucks,
                "bikes": bikes,
                "signal": signal,
                "time_remaining": int(time_remaining)
            })
            
            time.sleep(0.04)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# ==============================
# SOUTH CAMERA
# ==============================
@app.route('/video/south')
def video_south():

    def generate():
        for frame, cars, trucks, bikes in generate_frames(capSouth, trackerSouth, southVehicles):

            traffic_data["south"] = cars + trucks + bikes

            # Get updated signals and time remaining
            signals, time_remaining = update_signals()
            signal = signals["south"]

            socketio.emit('traffic_update', {
                "direction": "south",
                "cars": cars,
                "trucks": trucks,
                "bikes": bikes,
                "signal": signal,
                "time_remaining": int(time_remaining)
            })
            
            time.sleep(0.04)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# ==============================
# EAST CAMERA
# ==============================
@app.route('/video/east')
def video_east():

    def generate():
        for frame, cars, trucks, bikes in generate_frames(capEast, trackerEast, eastVehicles):

            traffic_data["east"] = cars + trucks + bikes

            # Get updated signals and time remaining
            signals, time_remaining = update_signals()
            signal = signals["east"]

            socketio.emit('traffic_update', {
                "direction": "east",
                "cars": cars,
                "trucks": trucks,
                "bikes": bikes,
                "signal": signal,
                "time_remaining": int(time_remaining)
            })
            
            time.sleep(0.04)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# ==============================
# WEST CAMERA
# ==============================
@app.route('/video/west')
def video_west():

    def generate():
        for frame, cars, trucks, bikes in generate_frames(capWest, trackerWest, westVehicles):

            traffic_data["west"] = cars + trucks + bikes

            # Get updated signals and time remaining
            signals, time_remaining = update_signals()
            signal = signals["west"]

            socketio.emit('traffic_update', {
                "direction": "west",
                "cars": cars,
                "trucks": trucks,
                "bikes": bikes,
                "signal": signal,
                "time_remaining": int(time_remaining)
            })
            
            time.sleep(0.04)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# ==============================
# RUN APP
# ==============================
if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)