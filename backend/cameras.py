import cv2
from backend.detector import process_frame
from backend.paths import VIDEO_DIR
from backend.sort import Sort

# Open videos
capNorth = cv2.VideoCapture(str(VIDEO_DIR / "north.mp4"))
capSouth = cv2.VideoCapture(str(VIDEO_DIR / "south.mp4"))
capEast = cv2.VideoCapture(str(VIDEO_DIR / "east.mp4"))
capWest = cv2.VideoCapture(str(VIDEO_DIR / "west.mp4"))

# Create trackers
trackerNorth = Sort(max_age=30, min_hits=2, iou_threshold=0.25)
trackerSouth = Sort(max_age=30, min_hits=2, iou_threshold=0.25)
trackerEast = Sort(max_age=30, min_hits=2, iou_threshold=0.25)
trackerWest = Sort(max_age=30, min_hits=2, iou_threshold=0.25)

# Vehicle ID sets
northVehicles = set()
southVehicles = set()
eastVehicles = set()
westVehicles = set()


def generate_frames(cap, tracker, vehicleSet):

    frame_count = 0
    last_cars = last_trucks = last_bikes = 0

    while True:

        success, frame = cap.read()

        # 🔥 restart video when finished
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            vehicleSet.clear()   # reset count (optional but good)
            frame_count = 0
            continue

        frame_count += 1
        
        # Process every Nth frame for performance
        if frame_count % 2 == 0:
            # Send frame to detector
            frame, cars, trucks, bikes = process_frame(frame, tracker, vehicleSet)
            last_cars, last_trucks, last_bikes = cars, trucks, bikes
        else:
            # Skip detection, just encode
            cars, trucks, bikes = last_cars, last_trucks, last_bikes

        # Encode frame safely
        try:
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
            
            if not ret:
                print("Frame encoding failed")
                continue
                
            frame_bytes = buffer.tobytes()
        except Exception as e:
            print(f"Encoding error: {e}")
            continue

        yield frame_bytes, cars, trucks, bikes