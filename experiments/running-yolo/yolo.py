from ultralytics import YOLO
import cv2
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
model = YOLO(PROJECT_ROOT / "assets" / "models" / "yolov8n.pt")

results = model(Path(__file__).with_name("operate.jpg"))

# Get the plotted image (with bounding boxes)
for r in results:
    img = r.plot()   # this draws boxes on image
    cv2.imshow("Detection Result", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
