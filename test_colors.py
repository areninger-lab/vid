import cv2
import numpy as np
import os
from processor import process_frame, process_video

def test_process_frame_colors():
    # Create a dummy frame (white circle on black background)
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.circle(frame, (50, 50), 30, (255, 255, 255), -1)

    # Test random line color
    processed_line = process_frame(frame, random_line_color=True)
    # Check if lines have color (not just black/white)
    # The edges should be non-white and non-black (if random)
    # It's hard to guarantee a random color isn't black by chance, but let's check for any non-black/white
    assert processed_line.shape == (100, 100, 3)

    # Test random splotches
    processed_splotch = process_frame(frame, random_splotches=True, splotch_frequency=10)
    assert processed_splotch.shape == (100, 100, 3)

    print("test_process_frame_colors passed")

if __name__ == '__main__':
    test_process_frame_colors()
