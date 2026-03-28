import cv2
import os
import time
import json
import csv
import threading
from datetime import datetime
from PIL import Image, ImageDraw

IMAGE_DIR = "images"
LOG_DIR = "logs"
CSV_LOG = os.path.join(LOG_DIR, "capture_log.csv")
JSON_LOG = os.path.join(LOG_DIR, "capture_log.json")

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Create CSV log
if not os.path.exists(CSV_LOG):
    with open(CSV_LOG, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "camera_id", "image_path", "status"])

def load_camera_config():
    with open("camera_config.json") as f:
        return json.load(f)["cameras"]

def write_json_log(entry):
    if os.path.exists(JSON_LOG):
        try:
            with open(JSON_LOG, "r") as f:
                data = json.load(f)
        except:
            data = []
    else:
        data = []

    data.append(entry)

    with open(JSON_LOG, "w") as f:
        json.dump(data, f, indent=4)

def save_image(frame, camera_id):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        cam_folder = os.path.join(IMAGE_DIR, camera_id)
        os.makedirs(cam_folder, exist_ok=True)

        image_path = os.path.join(cam_folder, f"{timestamp}.jpg")

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)

        img = img.resize((640, 480))

        draw = ImageDraw.Draw(img)
        draw.text((10, 10), f"{camera_id} {timestamp}", fill=(255, 0, 0))

        img.save(image_path, quality=70)

        return image_path, timestamp

    except Exception as e:
        print("Image save error:", e)
        return None, None

def log_capture(timestamp, camera_id, image_path, status):
    with open(CSV_LOG, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, camera_id, image_path, status])

    write_json_log({
        "timestamp": timestamp,
        "camera_id": camera_id,
        "image_path": image_path,
        "status": status
    })

def camera_worker(camera):
    camera_id = camera["id"]
    source = camera["source"]
    interval = camera["interval"]

    print(f"Starting camera {camera_id}")

    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"{camera_id} failed to open")
        return

    while True:
        try:
            ret, frame = cap.read()

            if not ret:
                print(f"{camera_id} frame error, reconnecting...")
                cap.release()
                time.sleep(5)
                cap = cv2.VideoCapture(source)
                continue

            image_path, timestamp = save_image(frame, camera_id)

            if image_path:
                log_capture(timestamp, camera_id, image_path, "OK")
                print(f"{camera_id} captured at {timestamp}")
            else:
                log_capture("ERROR", camera_id, "None", "SAVE_FAILED")

            time.sleep(interval)

        except Exception as e:
            print(f"{camera_id} error:", e)
            log_capture("ERROR", camera_id, "None", "CAMERA_ERROR")
            time.sleep(10)

def start_system():
    cameras = load_camera_config()
    threads = []

    for cam in cameras:
        t = threading.Thread(target=camera_worker, args=(cam,))
        t.daemon = True
        t.start()
        threads.append(t)

    print("Occupancy Monitoring System Running...")

    while True:
        time.sleep(60)

if __name__ == "__main__":
    start_system()