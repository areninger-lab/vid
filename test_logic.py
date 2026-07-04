import cv2
import numpy as np
import os
from processor import process_frame, process_video

def test_process_frame():
    # Create a dummy frame (white circle on black background)
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.circle(frame, (50, 50), 30, (255, 255, 255), -1)

    processed = process_frame(frame, thickness=1, brightness=1.0)

    assert processed.shape == (100, 100, 3)
    # The output should have some lines (non-white pixels)
    assert np.any(processed != 255)
    print("test_process_frame passed")

def test_process_video():
    # Create a dummy video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    input_path = 'test_input.mp4'
    output_path = 'test_output.mp4'
    out = cv2.VideoWriter(input_path, fourcc, 20.0, (100, 100))

    for i in range(20):
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.circle(frame, (50 + i, 50), 20, (255, 255, 255), -1)
        out.write(frame)
    out.release()

    process_video(input_path, output_path, duration=0.5) # 10 frames

    assert os.path.exists(output_path)
    cap = cv2.VideoCapture(output_path)
    ret, _ = cap.read()
    assert ret
    cap.release()

    os.remove(input_path)
    os.remove(output_path)
    print("test_process_video passed")

if __name__ == '__main__':
    test_process_frame()
    test_process_video()
