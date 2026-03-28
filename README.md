# Multi-Camera Occupancy Monitoring System

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/opencv-4.x-green.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/github-palnirupam/occupancy__system-blue.svg)](https://github.com/palnirupam/occupancy_system)

A production-ready, multi-threaded camera monitoring system designed for real-time occupancy tracking and surveillance. Built with Python, OpenCV, and PIL, this system provides enterprise-grade reliability with automatic failover, comprehensive logging, and flexible configuration.

## ⚠️ Important Warnings

### Legal and Privacy Considerations

**BEFORE USING THIS SYSTEM, PLEASE NOTE:**

- 🔒 **Privacy Laws**: Recording people without consent may be illegal in your jurisdiction. Check local laws before deployment.
- 📋 **Signage Required**: Post visible notices informing people they are being monitored.
- 🏢 **Workplace Monitoring**: Obtain proper authorization and inform employees before monitoring workspaces.
- 🔐 **Data Protection**: Captured images may contain personal data. Implement proper security measures.
- 🗑️ **Data Retention**: Establish and follow a clear data retention and deletion policy.
- 👤 **Access Control**: Restrict access to captured images and logs to authorized personnel only.

### Technical Warnings

- ⚡ **Camera Access**: Ensure no other application is using the camera before running this system.
- 💾 **Storage Space**: Monitor disk space regularly. System will fail if disk is full.
- 🔌 **Power Supply**: Use reliable power source. Sudden shutdown may corrupt log files.
- 🌐 **Network Cameras**: Use secure credentials. Never expose camera streams to public internet.
- 🔄 **Long Running Process**: This system runs indefinitely. Use `Ctrl+C` to stop gracefully.

### Responsible Use

This tool is intended for:
- ✅ Occupancy monitoring in authorized spaces
- ✅ Security surveillance with proper authorization
- ✅ Research and development purposes
- ✅ Personal property monitoring

This tool should NOT be used for:
- ❌ Unauthorized surveillance
- ❌ Invasion of privacy
- ❌ Illegal monitoring activities
- ❌ Harassment or stalking

**By using this system, you agree to comply with all applicable laws and regulations.**

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Output Structure](#output-structure)
- [Advanced Configuration](#advanced-configuration)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting](#troubleshooting)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Features

### Core Capabilities

- **Multi-Camera Support**: Monitor unlimited cameras simultaneously using multi-threaded architecture
- **Configurable Intervals**: Independent capture intervals for each camera (1-3600 seconds)
- **Image Processing Pipeline**: Automatic resizing, format conversion, and timestamp overlay
- **Dual Logging System**: Maintains both CSV and JSON logs for analytics and debugging
- **Auto-Reconnection**: Intelligent reconnection with exponential backoff on camera failures
- **Organized Storage**: Hierarchical storage with camera-specific directories
- **Real-Time Monitoring**: Console output with status updates and error reporting
- **Resource Efficient**: Optimized memory usage with JPEG compression

### Technical Highlights

- Thread-safe logging operations
- Graceful error handling and recovery
- Support for USB webcams and IP cameras (RTSP/HTTP)
- Cross-platform compatibility (Windows/Linux/macOS)
- Zero-dependency configuration (JSON-based)
- Production-ready daemon mode

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                     Main Process                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Configuration Loader (camera_config.json)             │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │                                  │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           Thread Manager (start_system)                │ │
│  └────────────────────────────────────────────────────────┘ │
│         │                  │                  │              │
│         ▼                  ▼                  ▼              │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐          │
│  │ Camera 1 │      │ Camera 2 │      │ Camera N │          │
│  │  Thread  │      │  Thread  │      │  Thread  │          │
│  └──────────┘      └──────────┘      └──────────┘          │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                           │                                  │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Image Processing Pipeline                      │ │
│  │  • Frame Capture → Color Conversion → Resize →        │ │
│  │    Timestamp Overlay → JPEG Compression → Save        │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │                                  │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Logging System                            │ │
│  │         CSV Logger  │  JSON Logger                     │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Component Overview

| Component | Responsibility | Thread-Safe |
|-----------|---------------|-------------|
| `load_camera_config()` | Parse JSON configuration | N/A |
| `camera_worker()` | Capture loop for individual camera | Yes |
| `save_image()` | Image processing and storage | Yes |
| `log_capture()` | Write to CSV/JSON logs | Yes |
| `write_json_log()` | JSON log management | Yes |
| `start_system()` | Thread orchestration | Yes |

## Prerequisites

### System Requirements

- **Python**: 3.7 or higher (3.9+ recommended)
- **Operating System**: Windows 10/11, Linux (Ubuntu 18.04+), macOS 10.14+
- **RAM**: 2GB minimum, 4GB+ recommended for 4+ cameras
- **Storage**: 10GB+ recommended (depends on retention policy)
- **CPU**: Multi-core processor recommended for concurrent camera processing

### Hardware Requirements

- USB Webcam(s) with UVC support
- IP Camera(s) with RTSP/HTTP streaming capability
- Adequate USB bandwidth for multiple USB cameras
- Network bandwidth: 2-8 Mbps per IP camera

## Installation

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/palnirupam/occupancy_system.git
cd occupancy_system

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure cameras (edit camera_config.json)

# 4. Run the system
python main.py
```

### Detailed Installation Steps

#### Step 1: Clone the Repository

```bash
# Clone from GitHub
git clone https://github.com/palnirupam/occupancy_system.git

# Navigate to project directory
cd occupancy_system
```

#### Step 2: Set Up Python Environment (Optional)

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Verify Installation:**

```bash
python -c "import cv2; print(f'OpenCV: {cv2.__version__}')"
python -c "import PIL; print(f'Pillow: {PIL.__version__}')"
```

#### Step 4: Test Camera Access (Optional)

Test if your camera is accessible:

```bash
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera 0:', 'OK' if cap.isOpened() else 'FAILED'); cap.release()"
```

## Configuration

### Basic Configuration

Edit `camera_config.json` to define your camera setup:

```json
{
  "cameras": [
    {
      "id": "room_101",
      "source": 0,
      "interval": 30
    },
    {
      "id": "room_102",
      "source": 1,
      "interval": 60
    }
  ]
}
```

### Configuration Parameters

| Parameter | Type | Description | Example Values |
|-----------|------|-------------|----------------|
| `id` | string | Unique camera identifier (alphanumeric, underscores, hyphens) | `"room_101"`, `"entrance_cam"` |
| `source` | int/string | Camera source index or stream URL | `0`, `1`, `"rtsp://..."` |
| `interval` | int | Capture interval in seconds (1-3600) | `30`, `60`, `300` |

### Camera Source Examples

**USB Webcams:**
```json
{
  "id": "webcam_primary",
  "source": 0,
  "interval": 30
}
```

**IP Cameras (RTSP):**
```json
{
  "id": "ip_cam_lobby",
  "source": "rtsp://admin:password@192.168.1.100:554/stream1",
  "interval": 60
}
```

⚠️ **Security Warning**: Never commit credentials to version control. Use environment variables for production.

**IP Cameras (HTTP/MJPEG):**
```json
{
  "id": "ip_cam_parking",
  "source": "http://192.168.1.101:8080/video",
  "interval": 45
}
```

**Video File (for testing):**
```json
{
  "id": "test_video",
  "source": "test_footage.mp4",
  "interval": 5
}
```

### Configuration Best Practices

1. **Naming Convention**: Use descriptive IDs that indicate location or purpose
2. **Interval Selection**: 
   - High-traffic areas: 15-30 seconds
   - Low-traffic areas: 60-300 seconds
   - Storage-constrained: 300+ seconds
3. **Camera Ordering**: List cameras in priority order (critical cameras first)
4. **Testing**: Start with one camera, then scale up

## Usage

### Running the System

⚠️ **Before running**: Ensure you have legal authorization to monitor the area and cameras are not in use by other applications.

Run with console output:

```bash
python main.py
```

**Expected Output:**
```
Starting camera room_101
Starting camera room_102
Occupancy Monitoring System Running...
room_101 captured at 2026-03-28_10-30-15
room_102 captured at 2026-03-28_10-31-20
```

### Stopping the System

Press `Ctrl+C` in the terminal to stop.

## Output Structure

### Directory Layout

```
project-root/
├── images/                          # Captured images
│   ├── room_101/
│   │   ├── 2026-03-28_10-30-15.jpg
│   │   ├── 2026-03-28_10-30-45.jpg
│   │   └── 2026-03-28_10-31-15.jpg
│   └── room_102/
│       ├── 2026-03-28_10-31-20.jpg
│       └── 2026-03-28_10-32-20.jpg
├── logs/                            # System logs
│   ├── capture_log.csv
│   └── capture_log.json
├── camera_config.json               # Configuration
├── main.py                          # Main application
├── requirements.txt                 # Dependencies
└── README.md                        # Documentation
```

### Image Files

**Naming Convention:** `YYYY-MM-DD_HH-MM-SS.jpg`

**Image Properties:**
- Format: JPEG
- Resolution: 640x480 pixels (configurable)
- Quality: 70% compression (configurable)
- Color Space: RGB
- Overlay: Camera ID + timestamp (top-left corner)

**Example Image Metadata:**
```
Filename: 2026-03-28_10-30-15.jpg
Size: ~50-150 KB (depends on content and quality)
Dimensions: 640x480
Text Overlay: "room_101 2026-03-28_10-30-15"
```

### Log Files

#### CSV Log Format (`logs/capture_log.csv`)

**Schema:**
```csv
timestamp,camera_id,image_path,status
```

**Example Data:**
```csv
timestamp,camera_id,image_path,status
2026-03-28_10-30-15,room_101,images/room_101/2026-03-28_10-30-15.jpg,OK
2026-03-28_10-30-45,room_101,images/room_101/2026-03-28_10-30-45.jpg,OK
ERROR,room_102,None,CAMERA_ERROR
2026-03-28_10-31-20,room_102,images/room_102/2026-03-28_10-31-20.jpg,OK
```

**Status Values:**
- `OK`: Successful capture and save
- `SAVE_FAILED`: Image capture succeeded but save failed
- `CAMERA_ERROR`: Camera access or frame capture error

**Use Cases:**
- Import into Excel/Google Sheets for analysis
- Process with pandas for data science workflows
- Generate reports and statistics

#### JSON Log Format (`logs/capture_log.json`)

**Schema:**
```json
[
  {
    "timestamp": "string (YYYY-MM-DD_HH-MM-SS)",
    "camera_id": "string",
    "image_path": "string",
    "status": "string (OK|SAVE_FAILED|CAMERA_ERROR)"
  }
]
```

**Example Data:**
```json
[
  {
    "timestamp": "2026-03-28_10-30-15",
    "camera_id": "room_101",
    "image_path": "images/room_101/2026-03-28_10-30-15.jpg",
    "status": "OK"
  },
  {
    "timestamp": "2026-03-28_10-30-45",
    "camera_id": "room_101",
    "image_path": "images/room_101/2026-03-28_10-30-45.jpg",
    "status": "OK"
  }
]
```

**Use Cases:**
- Parse with `jq` for command-line analysis
- Import into NoSQL databases
- Process with JavaScript/Node.js applications
- API integration

### Log Analysis Examples

#### Using Command Line (Windows PowerShell)

```powershell
# Count total captures
(Get-Content logs/capture_log.csv).Count - 1

# Count captures for specific camera
(Select-String -Path logs/capture_log.csv -Pattern "room_101").Count

# Check for errors
Select-String -Path logs/capture_log.csv -Pattern "ERROR|FAILED"
```

## Advanced Configuration

### Change Image Resolution

Edit line 52 in `main.py`:

```python
# Current
img = img.resize((640, 480))

# High resolution
img = img.resize((1920, 1080))

# Low resolution (storage-efficient)
img = img.resize((320, 240))
```

### Change Image Quality

Edit line 57 in `main.py`:

```python
# Current (balanced)
img.save(image_path, quality=70)

# High quality (larger files)
img.save(image_path, quality=95)

# Low quality (smaller files)
img.save(image_path, quality=40)
```

### Change Timestamp Format

Edit line 44 in `main.py`:

```python
# Current format: 2026-03-28_10-30-15
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Unix timestamp: 1711619415
timestamp = str(int(time.time()))

# ISO 8601: 2026-03-28T10:30:15
timestamp = datetime.now().isoformat()
```



## Performance Optimization

### Storage Optimization

**Estimated Storage Requirements:**

| Cameras | Interval | Quality | Daily Storage | Monthly Storage |
|---------|----------|---------|---------------|-----------------|
| 1 | 30s | 70% | ~100 MB | ~3 GB |
| 4 | 30s | 70% | ~400 MB | ~12 GB |
| 10 | 60s | 50% | ~500 MB | ~15 GB |



## Troubleshooting

### Common Issues

#### 1. Camera Not Opening

**Symptoms:**
```
room_101 failed to open
```

**Diagnosis:**
```bash
# Test camera access
python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened()); cap.release()"
```

**Solutions:**
- Verify camera is connected via Device Manager (Windows)
- Check if another application is using the camera
- Try different source indices (0, 1, 2)
- For IP cameras, verify network connectivity

#### 2. Frame Capture Errors

**Symptoms:**
```
room_101 frame error, reconnecting...
```

**Solutions:**
- Check USB cable quality and connection
- Reduce capture interval to avoid overwhelming the camera
- Check system resources via Task Manager
- Update camera drivers

#### 3. Image Save Failures

**Symptoms:**
```
Image save error: [Errno 28] No space left on device
```

**Solutions:**
- Check disk space via File Explorer or `Get-PSDrive` (PowerShell)
- Verify write permissions for the `images` directory
- Reduce image quality or resolution

#### 4. High CPU Usage

**Symptoms:**
- System slowdown
- Dropped frames

**Solutions:**
- Increase capture intervals
- Reduce image resolution
- Limit number of concurrent cameras

#### 5. Memory Issues

**Symptoms:**
- System becomes slow over time

**Solutions:**
- Restart the system periodically
- Reduce number of cameras or increase intervals
- Check Task Manager for memory usage

### Debug Mode

Add print statements in `main.py` for more detailed output:

```python
# In camera_worker function, add more logging
print(f"{camera_id} - Frame captured successfully")
print(f"{camera_id} - Processing image...")
print(f"{camera_id} - Image saved to {image_path}")
```

## API Reference

### Core Functions

#### `load_camera_config()`

Loads camera configuration from JSON file.

**Returns:** `list[dict]` - List of camera configuration objects

**Raises:** 
- `FileNotFoundError` - If camera_config.json doesn't exist
- `JSONDecodeError` - If JSON is malformed

**Example:**
```python
cameras = load_camera_config()
# [{'id': 'room_101', 'source': 0, 'interval': 30}, ...]
```

---

#### `save_image(frame, camera_id)`

Processes and saves a camera frame with timestamp overlay.

**Parameters:**
- `frame` (numpy.ndarray): OpenCV frame in BGR format
- `camera_id` (str): Camera identifier for folder organization

**Returns:** `tuple[str|None, str|None]`
- `image_path` (str): Path to saved image, or None on failure
- `timestamp` (str): Formatted timestamp string, or None on failure

**Processing Pipeline:**
1. Convert BGR to RGB color space
2. Resize to 640x480 pixels
3. Add text overlay with camera ID and timestamp
4. Compress and save as JPEG (70% quality)

**Example:**
```python
ret, frame = cap.read()
image_path, timestamp = save_image(frame, "room_101")
```

---

#### `log_capture(timestamp, camera_id, image_path, status)`

Writes capture event to both CSV and JSON logs.

**Parameters:**
- `timestamp` (str): Capture timestamp or "ERROR"
- `camera_id` (str): Camera identifier
- `image_path` (str): Path to saved image or "None"
- `status` (str): Capture status ("OK", "SAVE_FAILED", "CAMERA_ERROR")

**Side Effects:**
- Appends row to CSV log
- Appends entry to JSON log array

**Thread Safety:** Uses file locking (implicit via Python's file operations)

---

#### `camera_worker(camera)`

Main worker function for individual camera thread.

**Parameters:**
- `camera` (dict): Camera configuration object with keys: `id`, `source`, `interval`

**Behavior:**
- Infinite loop capturing frames at specified interval
- Automatic reconnection on failure (5-second delay)
- Error logging for all failure modes
- Graceful degradation on persistent errors

**Example:**
```python
camera = {"id": "room_101", "source": 0, "interval": 30}
thread = threading.Thread(target=camera_worker, args=(camera,))
thread.start()
```

---

#### `start_system()`

Initializes and starts all camera threads.

**Behavior:**
- Loads configuration
- Spawns daemon thread for each camera
- Enters infinite monitoring loop
- Blocks until interrupted (Ctrl+C)

**Thread Management:**
- All threads are daemon threads (exit when main thread exits)
- No explicit thread joining required

## Customization

### Change Image Resolution

**Location:** `main.py`, line 52

```python
# Current
img = img.resize((640, 480))

# High resolution
img = img.resize((1920, 1080))

# Low resolution (storage-efficient)
img = img.resize((320, 240))
```

### Change Image Quality

**Location:** `main.py`, line 57

```python
# Current (balanced)
img.save(image_path, quality=70)

# High quality (larger files)
img.save(image_path, quality=95)

# Low quality (smaller files)
img.save(image_path, quality=40)
```

### Change Timestamp Format

**Location:** `main.py`, line 44

```python
# Current format: 2026-03-28_10-30-15
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Unix timestamp: 1711619415
timestamp = str(int(time.time()))

# ISO 8601: 2026-03-28T10:30:15
timestamp = datetime.now().isoformat()

# Custom: 28-Mar-2026_10h30m15s
timestamp = datetime.now().strftime("%d-%b-%Y_%Hh%Mm%Ss")
```

### Customize Text Overlay

Edit line 54-55 in `main.py`:

```python
# Current
draw = ImageDraw.Draw(img)
draw.text((10, 10), f"{camera_id} {timestamp}", fill=(255, 0, 0))

# Change color to white
draw.text((10, 10), f"{camera_id} {timestamp}", fill=(255, 255, 255))

# Change position
draw.text((10, 450), f"{camera_id} {timestamp}", fill=(255, 0, 0))  # Bottom left
```



## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Open a Pull Request

## License

MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Nirupam Pal**  
GitHub: [@palnirupam](https://github.com/palnirupam)

## Support

For issues or questions, open an issue on [GitHub Issues](https://github.com/palnirupam/occupancy_system/issues).

---

Made with ❤️ by [Nirupam Pal](https://github.com/palnirupam)
