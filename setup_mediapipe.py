import subprocess
import sys
import platform

def run_command(command):
    try:
        subprocess.check_call([sys.executable, "-m"] + command)
        return True
    except subprocess.CalledProcessError:
        return False

def setup():
    print("--- MediaPipe Installation Helper ---")
    print(f"Python Version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    print("-" * 40)

    print("Step 1: Upgrading pip...")
    if run_command(["pip", "install", "--upgrade", "pip"]):
        print("✓ pip upgraded successfully.")
    else:
        print("✗ Failed to upgrade pip. Continuing anyway...")

    print("\nStep 2: Attempting to install MediaPipe...")
    if run_command(["pip", "install", "mediapipe"]):
        print("\n✓ MediaPipe installed successfully!")
        print("You can now run 'python3 app.py' and the 'Glowing Footprints' feature will be enabled.")
        return

    print("\n✗ Standard installation failed.")
    print("\nCommon reasons for 'No matching distribution' errors:")
    print("1. Python Version: MediaPipe currently supports Python 3.8 to 3.11 (3.12 support is rolling out).")
    print("2. Architecture: If you are on an older iMac (Intel), ensure you are using a 64-bit Python.")
    print("3. macOS Version: MediaPipe requires macOS 10.15 or higher.")

    print("\nTry this alternative command:")
    print("python3 -m pip install mediapipe --user")

    print("\nIf you are on an Apple Silicon (M1/M2) Mac and still failing, try:")
    print("arch -arm64 python3 -m pip install mediapipe")

if __name__ == "__main__":
    setup()
