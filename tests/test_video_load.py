import cv2
from pathlib import Path

# Test if videos can be loaded
VIDEO_DIR = Path(__file__).resolve().parents[1] / "assets" / "videos"
videos = [VIDEO_DIR / f"{direction}.mp4" for direction in ("north", "south", "east", "west")]

print("🔍 Testing video loading...\n")

for video_path in videos:
    if video_path.exists():
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
