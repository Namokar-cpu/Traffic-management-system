from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

results = model("operate.jpg")

# Get the plotted image (with bounding boxes)
for r in results:
    img = r.plot()   # this draws boxes on image
    cv2.imshow("Detection Result", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
