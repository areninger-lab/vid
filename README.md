# Video Stylizer (Take On Me Style)

This application transforms YouTube videos into stylized pencil/charcoal sketches, inspired by the "Take On Me" music video. It is designed for personal use and runs locally on your CPU.

## Features
- **YouTube Integration**: Download videos directly from a URL (supports SSL bypass for restricted environments).
- **Adjustable Parameters**:
  - **Line Thickness**: Adjust the boldness of the sketch lines.
  - **Brightness**: Lighten or darken the source video.
  - **Random Line Colors**: Toggle to make sketch lines colorful.
  - **Random Color Splotches**: Add "paint drip" splatters with adjustable size and frequency.
  - **Remove Static Background**: Remove anything that doesn't move, rendering it as plain white.
  - **Glowing Footprints**: Track feet using AI and leave a glowing, color-fading trail (Red -> Purple -> Blue).
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
   python3 -m pip install -r requirements.txt
   ```
3. If you encounter errors installing `mediapipe` (required for Glowing Footprints), run the helper script:
   ```bash
   python3 setup_mediapipe.py
   ```

## Running the Application
1. Start the Flask server:
   ```bash
   python3 app.py
   ```
2. Open your web browser and navigate to:
   `http://localhost:5005`

## How it Works
1. **Downloader**: Uses `yt-dlp` to fetch the highest quality mp4 video stream.
2. **Processor**:
   - Uses OpenCV for grayscale conversion, Canny edge detection, and background subtraction.
   - Uses **MediaPipe** for pose estimation to track foot movements.
   - Uses **MoviePy** with the `libx264` codec to ensure videos play correctly in all web browsers.
3. **Web UI**: Built with Flask and vanilla JavaScript for a simple, responsive experience.

## Technical Notes
- **CPU Heavy**: Processing video with AI pose detection on a CPU is intensive. Previews are recommended.
- **Storage**: Temporary files are stored in the `data/` directory and are ignored by git via `.gitignore`.
