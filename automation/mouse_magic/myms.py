import pyautogui
import time
import sys

# --- Configuration ---
STARTUP_DELAY_SECONDS = 5
MOVE_DISTANCE_PX = 50
MOVE_DURATION_SECONDS = 0.2
LOOP_INTERVAL_SECONDS = 3 # Time between each jiggle


def jiggle_mouse(x_start: int, y_start: int) -> bool:
    """
    Moves the mouse horizontally from (x_start, y_start) and returns to origin.
    Returns False if an external movement is detected during the jiggle.
    """
    pyautogui.moveTo(x_start + MOVE_DISTANCE_PX, y_start, duration=MOVE_DURATION_SECONDS)
    pyautogui.moveTo(x_start, y_start, duration=MOVE_DURATION_SECONDS)
    pyautogui.click()  # Optional: Click to ensure the system registers the movement
    # Check if something external moved the mouse during the jiggle
    x_final, y_final = pyautogui.position()
    if (x_final, y_final) != (x_start, y_start):
        print("External movement detected during jiggle! Stopping.")
        return False

    return True


def run() -> None:
    print(f"Program will start in {STARTUP_DELAY_SECONDS} seconds 😈")
    print("Move the mouse to a corner to trigger pyautogui's failsafe.")
    time.sleep(STARTUP_DELAY_SECONDS)

    iteration = 0
    try:
        while True:
            iteration += 1

            # Capture position before jiggle
            x_before, y_before = pyautogui.position()
            print(f"[{iteration}] Jiggling mouse at ({x_before}, {y_before})... ", end="", flush=True)

            if not jiggle_mouse(x_before, y_before):
                break

            print(f"OK. Waiting {LOOP_INTERVAL_SECONDS}s.")
            time.sleep(LOOP_INTERVAL_SECONDS)

            # Check if the user moved the mouse during the interval
            x_after, y_after = pyautogui.position()
            if (x_after, y_after) != (x_before, y_before):
                print("Mouse moved by user during interval. Stopping.")
                break

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
        sys.exit(0)


if __name__ == "__main__":
    run()
