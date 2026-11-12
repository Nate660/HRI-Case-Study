from eyetrax import GazeEstimator, run_9_point_calibration
import cv2
import time
from pynput.keyboard import Key, Controller

# --- CONFIGURATION ---
NEUTRAL_OFFSET_UP = 600      # How far above neutral counts as "looking up"
NEUTRAL_OFFSET_DOWN = 600    # How far below neutral counts as "looking down"
TRIGGER_COOLDOWN = 1.5       # Seconds between scrolls
# ---------------------

keyboard = Controller()

estimator = GazeEstimator()
print("Starting 9-point calibration. Look at each dot.")
run_9_point_calibration(estimator)

cap = cv2.VideoCapture(0)

# --- Measure neutral gaze for 3 seconds ---
print("Now look straight ahead naturally for 3 seconds...")
neutral_samples = []
start = time.time()
while time.time() - start < 3.0:
    ret, frame = cap.read()
    if not ret:
        continue
    features, blink = estimator.extract_features(frame)
    if features is not None and not blink:
        _, y = estimator.predict([features])[0]
        neutral_samples.append(y)
    cv2.putText(frame, f"Calibrating neutral: {3.0 - (time.time() - start):.1f}s",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.imshow('Neutral Calibration', frame)
    cv2.waitKey(1)

if neutral_samples:
    neutral_y = sum(neutral_samples) / len(neutral_samples)
else:
    neutral_y = 700  # fallback
print(f"Neutral Y measured at: {neutral_y:.0f}")

GAZE_UP_THRESHOLD = neutral_y - NEUTRAL_OFFSET_UP
GAZE_DOWN_THRESHOLD = neutral_y + NEUTRAL_OFFSET_DOWN
print(f"UP threshold: {GAZE_UP_THRESHOLD:.0f}  |  DOWN threshold: {GAZE_DOWN_THRESHOLD:.0f}")

cv2.destroyWindow('Neutral Calibration')

# --- Main loop ---
last_trigger_time = 0
last_trigger_type = None

print("Ready. Look up/down to scroll. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    features, blink = estimator.extract_features(frame)

    if features is not None and not blink:
        x, y = estimator.predict([features])[0]

        # Determine zone
        if y < GAZE_UP_THRESHOLD:
            zone = "UP"
            zone_color = (0, 255, 0)
        elif y > GAZE_DOWN_THRESHOLD:
            zone = "DOWN"
            zone_color = (0, 0, 255)
        else:
            zone = "NEUTRAL"
            zone_color = (255, 255, 0)

        cv2.putText(frame, f"Y: {y:.0f}  Zone: {zone}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, zone_color, 2)

        # Trigger with cooldown
        current_time = time.time()
        if current_time - last_trigger_time > TRIGGER_COOLDOWN:
            trigger = None
            if zone == "UP":
                trigger = "PAGE_UP"
                keyboard.press(Key.page_up)
                keyboard.release(Key.page_up)
            elif zone == "DOWN":
                trigger = "PAGE_DOWN"
                keyboard.press(Key.page_down)
                keyboard.release(Key.page_down)

            if trigger:
                last_trigger_time = current_time
                last_trigger_type = trigger
                print(f"TRIGGER: {trigger} at Y={y:.0f}")

        if last_trigger_type:
            cv2.putText(frame, last_trigger_type, (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow('Eye Scroll', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()