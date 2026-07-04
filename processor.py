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

def process_video(input_path, output_path, thickness=1, brightness=1.0, jitter=0, duration=None):
    """
    Processes a video file.
    If duration is set, only processes the first 'duration' seconds.
    """
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise Exception(f"Error opening video file: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if duration:
        frames_to_process = int(fps * duration)
    else:
        frames_to_process = total_frames

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    count = 0
    while cap.isOpened() and count < frames_to_process:
        ret, frame = cap.read()
        if not ret:
            break

        processed = process_frame(frame, thickness, brightness, jitter)
        out.write(processed)
        count += 1

    cap.release()
    out.release()
    return output_path
