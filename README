# Eye Scroll — Hands-Free Gaze-Controlled Scrolling for Mobile Devices

An assistive human-robot interaction prototype that lets users scroll a
paired smartphone using only their gaze. A webcam tracks the user's eyes,
a Python pipeline classifies their gaze into UP / NEUTRAL / DOWN zones, and
a Raspberry Pi Zero W forwards Page Up / Page Down keystrokes to the phone
over Bluetooth HID — no companion app required on the phone.

![System Architecture](docs/system_architecture.png)

---

## Motivation

Capacitive touchscreens are the dominant interface on modern smartphones,
but they assume fine motor control and the ability to both hold and press
the device. For users with motor impairments, this is a barrier. Voice
control exists but is noisy, privacy-sensitive in public, and tiring over
long sessions; dedicated head-tracking hardware is expensive and bulky.
Eye Scroll targets the gap: a low-cost, modular, gaze-driven interface that
works with any phone that accepts a Bluetooth keyboard.

---

## How It Works

1. **9-point calibration** — the user looks at nine on-screen dots to train
   the gaze model.
2. **Neutral baseline** — the user looks straight ahead for 3 seconds; the
   average Y-coordinate becomes their resting position.
3. **Live loop** — each frame is passed through feature extraction and gaze
   prediction, then classified into UP / DOWN / NEUTRAL against the
   calibrated thresholds.
4. **Cooldown gate** — a 1.5 s cooldown prevents repeated triggers from a
   single sustained gaze.
5. **HID emulation** — the host sends a Page Up / Page Down keystroke to a
   Raspberry Pi Zero W, which presents as a Bluetooth keyboard to the phone.

See `docs/system_architecture.png` for the full pipeline.

---

## Repository Contents

| File | Purpose |
|------|---------|
| `eye_scroll.py` | Main vision + command loop |
| `start_eyescroll.bat` | Windows launcher (activates venv, runs script) |
| `requirements.txt` | Pinned Python dependencies |
| `docs/` | Diagrams and renders |
| `hardware/stl/` | Optional 3D-print files for clamp / joints |

---

## Requirements

- Python 3.10+
- A webcam
- (For the phone-facing deployment) a Raspberry Pi Zero W configured as a
  Bluetooth HID peripheral
- Windows is the primary tested platform (the launcher is a `.bat`); the
  Python code itself is cross-platform.

---

## Setup

```bash
# Clone
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
