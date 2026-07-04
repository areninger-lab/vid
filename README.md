# Video Stylizer (Take On Me Style)

This application transforms YouTube videos into stylized pencil/charcoal sketches, inspired by the "Take On Me" music video. It is designed for personal use and runs locally on your CPU.

## Features
- **YouTube Integration**: Download videos directly from a URL.
- **Adjustable Parameters**:
  - **Line Thickness**: Adjust the boldness of the sketch lines.
  - **Brightness**: Lighten or darken the source video before processing.
  - **Jitteriness**: Simulate the hand-drawn "vibration" effect.
- **Workflow**: Generate a 5-second preview to fine-tune your settings before processing the full video.
- **Background Processing**: Jobs run in the background; you can return to a unique link to check status and download the result.

## Prerequisites
- **Python 3.8+**
- **FFmpeg**: Required by `yt-dlp` and `moviepy` for certain video operations.
  - *Ubuntu/Debian*: `sudo apt update && sudo apt install ffmpeg`
  - *macOS*: `brew install ffmpeg`
  - *Windows*: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to your PATH.

## Installation
1. Clone or download this repository.
2. Install the required Python packages:
   ```bash
   pip install flask yt-dlp opencv-python-headless numpy moviepy
   ```

## Running the Application
1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to:
   `http://localhost:5000`

## How it Works
1. **Downloader**: Uses `yt-dlp` to fetch the highest quality mp4 video stream.
2. **Processor**:
   - Converts frames to grayscale.
   - Applies Canny edge detection.
   - Inverts the result to get black lines on a white background.
   - Adds "jitter" by slightly shifting the image and varying edge detection thresholds frame-by-frame.
3. **Web UI**: Built with Flask and vanilla JavaScript for a simple, responsive experience.

## Technical Notes
- **CPU Heavy**: Processing 10 minutes of video on a CPU may take some time (roughly 2-5x real-time depending on your processor).
- **Storage**: Temporary files are stored in the `data/` directory.
