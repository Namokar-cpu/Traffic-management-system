import cv2
import numpy as np
from backend.paths import MODEL_PATH

model = None


def get_model():
    global model
    if model is None:
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise RuntimeError(
                "YOLO dependencies are not installed. Install requirements.txt "
                "before opening a camera feed."
            ) from exc
        model = YOLO(str(MODEL_PATH))
        model.fuse()
    return model

# COCO class names
classNames = [
"person","bicycle","car","motorbike","aeroplane","bus","train","truck","boat",
"traffic light","fire hydrant","stop sign","parking meter","bench","bird","cat",
"dog","horse","sheep","cow","elephant","bear","zebra","giraffe","backpack","umbrella",
"handbag","tie","suitcase","frisbee","skis","snowboard","sports ball","kite","baseball bat",
"baseball glove","skateboard","surfboard","tennis racket","bottle","wine glass","cup",
"fork","knife","spoon","bowl","banana","apple","sandwich","orange","broccoli",
"carrot","hot dog","pizza","donut","cake","chair","sofa","pottedplant","bed","grapes",
"diningtable","toilet","tvmonitor","laptop","mouse","remote","keyboard","cell phone",
"microwave","oven","toaster","sink","refrigerator","book","clock","vase","scissors",
"teddy bear","hair drier","toothbrush"
]

# ============================================
# MAIN FUNCTION
# ============================================
def process_frame(img, tracker, vehicleSet):

    try:
        # Resize for speed (aggressive downsampling for high-res videos)
        img = cv2.resize(img, (480, 320))

        # Counting line (adjust if needed)
        lineY = 160
        cv2.line(img, (0, lineY), (480, lineY), (0, 255, 0), 2)

        detections = []
        class_map = {}

        # ============================================
        # YOLO DETECTION
        # ============================================
        results = get_model()(img, stream=True, conf=0.5, iou=0.4)

        for r in results:
            for box in r.boxes:

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                currentClass = classNames[cls]

                if currentClass in ["car", "truck", "bus", "motorbike"] and conf > 0.4:

                    detections.append([x1, y1, x2, y2, conf])
                    class_map[(x1, y1, x2, y2)] = currentClass

        # Convert detections
        detections = np.array(detections) if len(detections) > 0 else np.empty((0, 5))
    except Exception as e:
        print(f"Error in YOLO detection: {e}")
        detections = np.empty((0, 5))
        class_map = {}

    # ============================================
    # TRACKING (SORT)
    # ============================================
    resultsTracker = tracker.update(detections)

    # Per-frame counts of NEW vehicles crossing line
    new_cars = 0
    new_trucks = 0
    new_bikes = 0

    # ============================================
    # COUNTING LOGIC (LINE CROSSING)
    # ============================================
    for result in resultsTracker:

        x1, y1, x2, y2, track_id = map(int, result)

        # Center point
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        # Draw bounding box and center
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(img, (cx, cy), 4, (0, 0, 255), -1)
        cv2.putText(img, str(track_id), (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Match with detected class
        matched_class = None
        for (dx1, dy1, dx2, dy2), objClass in class_map.items():
            if abs(x1 - dx1) < 25 and abs(y1 - dy1) < 25:
                matched_class = objClass
                break

        if matched_class:
            # 🔥 LINE CROSSING CONDITION - with hysteresis to prevent multiple counts
            # Only count if vehicle crosses AND hasn't been counted before
            if lineY - 20 < cy < lineY + 20:
                vehicle_key = (track_id, matched_class)
                
                if vehicle_key not in vehicleSet:
                    vehicleSet.add(vehicle_key)

                    if matched_class == "car":
                        new_cars += 1

                    elif matched_class in ["truck", "bus"]:
                        new_trucks += 1

                    elif matched_class == "motorbike":
                        new_bikes += 1

    # ============================================
    # RETURN VALUES
    # ============================================
    # Return cumulative counts from vehicleSet
    total_cars = len([v for v in vehicleSet if v[1] == "car"])
    total_trucks = len([v for v in vehicleSet if v[1] in ["truck", "bus"]])
    total_bikes = len([v for v in vehicleSet if v[1] == "motorbike"])

    return img, total_cars, total_trucks, total_bikes