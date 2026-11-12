# Eye Scroll — Hands-Free Gaze-Controlled Scrolling for Mobile Devices

An assistive human-robot interaction prototype that lets users scroll a paired smartphone using only their gaze. A webcam tracks the user's eyes, a Python pipeline classifies their gaze into UP / NEUTRAL / DOWN zones, and a Raspberry Pi Zero W forwards Page Up / Page Down keystrokes to the phone over Bluetooth HID — no companion app required on the phone.

This project is built on top of [EyeTrax](https://github.com/ck-zhang/eyetrax), a webcam-based eye-tracking library. EyeTrax provides the vision pipeline (feature extraction, calibration, gaze prediction); this project adds the neutral-baseline logic, zone classification, cooldown gate, and Bluetooth HID bridge.

![System Architecture](docs/system_architecture.png)

---

## Motivation

Capacitive touchscreens are the dominant interface on modern smartphones, but they assume fine motor control and the ability to both hold and press the device. For users with motor impairments or temporary physical limitations, this is a significant barrier.

While voice control provides hands-free execution, it suffers from privacy issues in public spaces, is sensitive to environmental noise, and causes high cognitive fatigue during continuous use. Conversely, dedicated head-tracking hardware is expensive, rigid, and bulky, lacking the modular mounting required for a standard commercial smartphone.

Eye Scroll targets this gap: a low-cost, modular, gaze-driven interface that works with any phone that accepts a standard Bluetooth keyboard.

---

## How It Works

1. **9-point calibration** — The user looks at nine on-screen dots to train the gaze model and map iris position to screen coordinates. (Provided by EyeTrax via `run_9_point_calibration`.)
2. **Neutral baseline** — The user looks straight ahead for 3 seconds; the average Y-coordinate is recorded as their resting position.
3. **Live loop** — Each webcam frame is passed through EyeTrax's feature extraction and gaze prediction, then classified into UP / DOWN / NEUTRAL against the calibrated thresholds.
4. **Cooldown gate** — A 1.5-second cooldown prevents repeated triggers from a single sustained gaze, acting as a spam filter.
5. **HID emulation** — The host sends a Page Up / Page Down keystroke to a Raspberry Pi Zero W, which presents as a Bluetooth keyboard to the paired mobile device.

See `docs/system_architecture.png` for the full pipeline diagram.

---

## Repository Contents

| File / Folder | Purpose |
|------|---------|
| `eye_scroll.py` | Main vision processing and command loop |
| `start_eyescroll.bat` | Windows launcher (activates venv, runs script) |
| `requirements.txt` | Pinned Python dependencies |
| `docs/` | System architecture diagrams and hardware renders |
| `hardware/stl/` | Optional 3D-print files for clamp and joints |

---

## Requirements

- **Python 3.10+**
- A standard webcam
- (For the phone-facing deployment) A Raspberry Pi Zero W configured as a Bluetooth HID peripheral
- **OS:** Windows is the primary tested platform (the launcher is a `.bat`); the Python code itself is cross-platform.

### Key Dependencies

- [`eyetrax`](https://github.com/ck-zhang/eyetrax) — gaze estimation, calibration, and optional gaze filtering
- [`opencv-python`](https://pypi.org/project/opencv-python/) — webcam capture and preview overlay
- [`pynput`](https://pypi.org/project/pynput/) — keyboard emulation (Page Up / Page Down)

See `requirements.txt` for the full pinned list.

---

## Setup

```
# Clone the repository
git clone https://github.com/<your-username>/eye-scroll.git
cd eye-scroll

# Create and activate a virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

Running the System

On Windows, after completing the Setup steps above, simply double-click start_eyescroll.bat. It will activate your local venv and run the script.

Or run manually from the terminal:
bash

python eye_scroll.py

User Flow

    A window opens and asks you to look at 9 calibration dots.

    Next, look straight ahead for 3 seconds while the neutral baseline is captured.

    The preview window shows your live Y-coordinate, current zone (UP/DOWN/NEUTRAL), and the last fired command.

    Look up past the top threshold to scroll up; look down past the bottom threshold to scroll down. Stay in the neutral band to idle.

    Press q in the preview window to quit.

Tuning

If the system triggers too easily or feels sluggish, edit the configuration constants at the top of eye_scroll.py:
python

NEUTRAL_OFFSET_UP   = 600      # How far above neutral counts as "looking up"
NEUTRAL_OFFSET_DOWN = 600      # How far below neutral counts as "looking down"
TRIGGER_COOLDOWN    = 1.5      # Seconds between scrolls

    Increase the offsets if scrolls fire too easily (e.g., you look slightly up and it triggers).

    Increase TRIGGER_COOLDOWN if the scroll feels too fast or uncontrollable.

EyeTrax also exposes optional smoothing filters (kalman, kalman_ema, kde) — see the EyeTrax documentation if you want to enable them.
Hardware Overview

    Structural frame: Two 2020 T-slot aluminium extrusions on perpendicular sliding axes, joined with 3-D printed joints for adjustable height and pitch.

    Rotating base: Ball-bearing pivot with embedded magnets that index the arm at 90° — the arm can be swung out of the way and returned without recalibration.

    Clamp: Fully 3-D printed, designed as a controlled break point so that under load the clamp fails before the device falls onto the user.

    Phone holder: Jakub Lattenberg's Multifunctional Arm, licensed CC BY 4.0.

See docs/ for renders and photos of the physical assembly.
Status & Known Limitations

    The current build dispatches keystrokes to the host's active window for testing; wiring the same command stream to the Raspberry Pi Zero W's Bluetooth HID peripheral is the deployment step.

    The pipeline currently classifies on the vertical (Y) axis only.

    Calibration is one-shot per session; gradual eye-position drift over a long session is not corrected dynamically.

    Neutral baseline assumes the user is looking roughly straight ahead at the screen for the 3-second capture window.

Future Directions

    Near-Infrared Active Illumination: Adding an IR light source and compatible camera to remove dependence on ambient light.

    Dynamic Calibration: Updating thresholds automatically to adapt to slow gaze drift over time.

    Servo Tracking: Adding low-cost servos to the arm so it follows the user's head and maintains optimal screen placement.

    Multi-Axis Zones: Expanding the logic (left / right / select) to widen the command set.

Acknowledgements

This project is built on EyeTrax by Chenkai Zhang, which provides the underlying webcam gaze-estimation pipeline (feature extraction, 9-point calibration, and gaze prediction). EyeTrax is MIT-licensed.

If you use this project or EyeTrax in academic work, please cite EyeTrax:
bibtex

@software{Zhang2025_EyeTrax,
  author       = {Chenkai Zhang},
  title        = {EyeTrax},
  version      = {0.2.2},
  date         = {2025-04-23},
  url          = {https://pypi.org/project/eyetrax/},
  repository   = {https://github.com/ck-zhang/EyeTrax},
  doi          = {10.5281/zenodo.17188537},
  keywords     = {eye tracking, computer vision}
}

The physical phone holder is based on Jakub Lattenberg's Multifunctional Arm, licensed CC BY 4.0.
References

    [1] J. Lattenberg, "Multifunctional Arm (Phone Holder)," Printables.com, Aug. 17, 2025. [Online]. Available: https://www.printables.com/model/1153921-multifunctional-arm-phone-holder

    [2] C. Zhang, EyeTrax, version 0.2.2, 2025. [Online]. Available: https://github.com/ck-zhang/eyetrax

License

This project is licensed under the MIT License — see the LICENSE file for details.
