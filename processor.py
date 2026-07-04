import cv2
import numpy as np
import random

def process_frame(frame, thickness=1, brightness=1.0, random_line_color=False, random_splotches=False, splotch_size=20, splotch_frequency=5):
    """
    Processes a single frame to apply a 'Take On Me' style sketch effect.
    """
    # Adjust brightness
    if brightness != 1.0:
        frame = cv2.convertScaleAbs(frame, alpha=brightness, beta=0)

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Adjust thickness
    if thickness > 1:
        kernel = np.ones((thickness, thickness), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)

    # Create the result image
    height, width = edges.shape
    result = np.full((height, width, 3), 255, dtype=np.uint8)

    # Handle line coloring
    if random_line_color:
        line_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    else:
        line_color = (0, 0, 0) # Black

    result[edges > 0] = line_color

    # Add random splotches
    if random_splotches:
        for _ in range(splotch_frequency):
            center = (random.randint(0, width), random.randint(0, height))
            radius = random.randint(1, splotch_size)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            cv2.circle(result, center, radius, color, -1)

    return result

from moviepy import VideoFileClip

def process_video(input_path, output_path, thickness=1, brightness=1.0,
                  random_line_color=False, random_splotches=False,
                  splotch_size=20, splotch_frequency=5, duration=None):
    """
    Processes a video file using moviepy for better codec compatibility.
    """
    clip = VideoFileClip(input_path)

    if duration:
        clip = clip.subclipped(0, duration)

    def transform(get_frame, t):
        frame = get_frame(t)
        # MoviePy uses RGB, but our processor uses BGR (OpenCV default)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        processed_bgr = process_frame(frame_bgr, thickness, brightness,
                                      random_line_color, random_splotches,
                                      splotch_size, splotch_frequency)
        # Convert back to RGB for MoviePy
        return cv2.cvtColor(processed_bgr, cv2.COLOR_BGR2RGB)

    processed_clip = clip.transform(transform)

    # Use libx264 for wide browser compatibility
    processed_clip.write_videofile(output_path, codec="libx264", audio=False, logger=None)

    clip.close()
    processed_clip.close()

    return output_path
