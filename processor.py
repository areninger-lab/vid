import cv2
import numpy as np
import random

def process_frame(frame, thickness=1, brightness=1.0, jitter=0):
    """
    Processes a single frame to apply a 'Take On Me' style sketch effect.
    """
    # Adjust brightness
    if brightness != 1.0:
        frame = cv2.convertScaleAbs(frame, alpha=brightness, beta=0)

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply jitter to the source image if jitter > 0
    if jitter > 0:
        # Randomly shift the image slightly
        tx = random.uniform(-jitter, jitter)
        ty = random.uniform(-jitter, jitter)
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        gray = cv2.warpAffine(gray, M, (gray.shape[1], gray.shape[0]), borderMode=cv2.BORDER_REPLICATE)

        # Also vary the noise a bit
        noise = np.random.normal(0, jitter * 2, gray.shape).astype(np.uint8)
        gray = cv2.add(gray, noise)

    # Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge detection
    # Vary thresholds slightly if jitter is high to get that "re-drawn" feel
    low_threshold = 50 + random.randint(-jitter*5, jitter*5) if jitter > 0 else 50
    high_threshold = 150 + random.randint(-jitter*5, jitter*5) if jitter > 0 else 150
    edges = cv2.Canny(blurred, max(10, low_threshold), max(20, high_threshold))

    # Invert edges: black lines on white background
    inverted_edges = cv2.bitwise_not(edges)

    # Adjust thickness
    if thickness > 1:
        kernel = np.ones((thickness, thickness), np.uint8)
        # Erode because we have black lines on white background
        inverted_edges = cv2.erode(inverted_edges, kernel, iterations=1)

    # Convert back to BGR for video writer compatibility
    result = cv2.cvtColor(inverted_edges, cv2.COLOR_GRAY2BGR)

    return result

from moviepy import VideoFileClip

def process_video(input_path, output_path, thickness=1, brightness=1.0, jitter=0, duration=None):
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
        processed_bgr = process_frame(frame_bgr, thickness, brightness, jitter)
        # Convert back to RGB for MoviePy
        return cv2.cvtColor(processed_bgr, cv2.COLOR_BGR2RGB)

    processed_clip = clip.transform(transform)

    # Use libx264 for wide browser compatibility
    processed_clip.write_videofile(output_path, codec="libx264", audio=False, logger=None)

    clip.close()
    processed_clip.close()

    return output_path
