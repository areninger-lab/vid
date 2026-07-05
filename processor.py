import cv2
import numpy as np
import random

def process_frame(frame, thickness=1, brightness=1.0, random_line_color=False, random_splotches=False, splotch_size=20, splotch_frequency=5, fg_mask=None):
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

    # Apply foreground mask if provided (Background Removal)
    if fg_mask is not None:
        # Static parts (fg_mask == 0) should be white
        result[fg_mask == 0] = [255, 255, 255]

    # Add random splotches (paint drips)
    if random_splotches:
        # Treat splotch_frequency as percentage chance per frame (0-100)
        if random.randint(1, 100) <= splotch_frequency:
            center = (random.randint(0, width), random.randint(0, height))
            radius = random.randint(5, splotch_size)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            # Main splotch
            cv2.circle(result, center, radius, color, -1)

            # Draw 1 or 2 drip tails
            num_tails = random.randint(1, 2)
            for _ in range(num_tails):
                drip_len = random.randint(1, 4)
                curr_pos = list(center)
                curr_r = radius

                # Pick a random direction (angle) for this tail
                angle = random.uniform(0, 2 * np.pi)

                for _ in range(drip_len):
                    # Move in the chosen direction
                    curr_r = int(curr_r * 0.7)
                    if curr_r < 2: break

                    dist = int(curr_r * 1.5)
                    curr_pos[0] += int(dist * np.cos(angle))
                    curr_pos[1] += int(dist * np.sin(angle))

                    if 0 <= curr_pos[0] < width and 0 <= curr_pos[1] < height:
                        cv2.circle(result, (curr_pos[0], curr_pos[1]), curr_r, color, -1)
                    else:
                        break

    return result

from moviepy import VideoFileClip

def process_video(input_path, output_path, thickness=1, brightness=1.0,
                  random_line_color=False, random_splotches=False,
                  splotch_size=20, splotch_frequency=5,
                  remove_background=False, duration=None):
    """
    Processes a video file using moviepy for better codec compatibility.
    """
    clip = VideoFileClip(input_path)

    if duration:
        clip = clip.subclipped(0, duration)

    # Initialize background subtractor if requested
    bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False) if remove_background else None

    def transform(get_frame, t):
        frame = get_frame(t)
        # MoviePy uses RGB, but our processor uses BGR (OpenCV default)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        fg_mask = None
        if bg_subtractor is not None:
            # We need to apply the subtractor to all frames leading up to 't' to keep it synced
            # However, MoviePy's transform(get_frame, t) can be called out of order.
            # This is a limitation of using moviepy's transform for stateful OpenCV effects.
            # For a better result, we might need to process frame-by-frame manually or accept some jitter in the mask.
            fg_mask = bg_subtractor.apply(frame_bgr)
            # Simple noise removal on mask
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)

        processed_bgr = process_frame(frame_bgr, thickness, brightness,
                                      random_line_color, random_splotches,
                                      splotch_size, splotch_frequency, fg_mask=fg_mask)
        # Convert back to RGB for MoviePy
        return cv2.cvtColor(processed_bgr, cv2.COLOR_BGR2RGB)

    processed_clip = clip.transform(transform)

    # Use libx264 for wide browser compatibility
    processed_clip.write_videofile(output_path, codec="libx264", audio=False, logger=None)

    clip.close()
    processed_clip.close()

    return output_path
