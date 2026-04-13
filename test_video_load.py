import cv2
import os

# Test if videos can be loaded
videos = ["videos/north.mp4", "videos/south.mp4", "videos/east.mp4", "videos/west.mp4"]

print("🔍 Testing video loading...\n")

for video_path in videos:
    if os.path.exists(video_path):
        cap = cv2.VideoCapture(video_path)
        
        if cap.isOpened():
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            print(f"✅ {video_path}")
            print(f"   - Frames: {frame_count}")
            print(f"   - FPS: {fps}")
            print(f"   - Resolution: {width}x{height}\n")
            
            # Try to read first frame
            ret, frame = cap.read()
            if ret:
                print(f"   - First frame read: ✓")
            else:
                print(f"   - First frame read: ✗ FAILED")
            
            cap.release()
        else:
            print(f"❌ {video_path} - Could not open")
    else:
        print(f"❌ {video_path} - File not found")

print("\n✅ Test complete!")
