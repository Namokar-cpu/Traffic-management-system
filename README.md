# Traffic Management System

A Flask dashboard that uses YOLOv8 and SORT tracking to count vehicles from four traffic-camera videos and adapt the intersection signals in real time.

## Project structure

```text
.
├── assets/
│   ├── models/                  # YOLO model weights
│   └── videos/                  # North, south, east, and west demo feeds
├── backend/
│   ├── app.py                   # Flask + Socket.IO application
│   ├── cameras.py               # Video capture and frame generation
│   ├── detector.py              # YOLO detection and vehicle counting
│   ├── paths.py                 # Project-relative paths
│   ├── sort.py                  # SORT tracker
│   └── __init__.py
├── frontend/
│   ├── static/                  # JavaScript and CSS
│   └── templates/               # Flask HTML templates
├── experiments/                 # Older standalone detection experiments
├── tests/                       # Small repository checks
├── requirements.txt
└── README.md
```

The application code is intentionally separate from experiments and large runtime assets so each part of the project is easy to find and maintain.

## Setup

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

The repository includes the YOLOv8 model and sample videos in `assets/`.

## Run the dashboard

From the repository root:

```bash
python -m backend.app
```

Open <http://127.0.0.1:5000> in a browser. The dashboard displays four camera feeds, vehicle counts, signal status, and a live traffic chart.

## Verify the sample videos

```bash
python tests/test_video_load.py
```

## Notes

- The detector processes cars, trucks, buses, and motorbikes.
- Counts reset when a demo video loops.
- Files under `experiments/` are retained for reference and are not required to run the dashboard.
