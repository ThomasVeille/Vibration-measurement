"""
Vibration capture & spectral analysis
--------------------------------------
1. Connects to the ESP32 over serial
2. Sends 'r' to trigger a capture (see matching Arduino sketch)
3. Reads the CSV block sent back (index,time_us,ax,ay,az)
4. Saves it to a timestamped .csv file
5. Computes and plots the FFT amplitude spectrum for X, Y and Z

Requirements:
    pip install pyserial numpy scipy matplotlib
"""

import csv
import sys
import time
import datetime

import serial
import numpy as np
from scipy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt

# ---------------- Configuration ----------------
SERIAL_PORT = "COM9"      # change to your ESP32 port (e.g. "/dev/ttyUSB0" on Linux/Mac)
BAUD_RATE = 115200
SERIAL_TIMEOUT = 2        # seconds, per-line read timeout
MAX_WAIT_READY = 10       # seconds to wait for the board to say READY


def wait_for_line(ser, expected, timeout):
    """Read lines until one matches `expected` or timeout is reached."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        line = ser.readline().decode(errors="ignore").strip()
        if line == expected:
            return True
        if line:
            print(f"[board] {line}")
    return False


def capture_to_csv(port=SERIAL_PORT, baud=BAUD_RATE):
    print(f"Opening {port} @ {baud} baud...")
    with serial.Serial(port, baud, timeout=SERIAL_TIMEOUT) as ser:
        ser.reset_input_buffer()  # clear immediately, before any reset-triggered boot output arrives
        time.sleep(2.5)  # safety margin: covers a possible reboot if the port open triggered one

        # The board only prints READY once at boot and once after each capture, so a fresh
        # READY is not guaranteed to be visible here if no reset happened this time. Instead
        # of requiring it, just send the trigger: the board is either idle waiting for 'r'
        # (no reset happened) or has just finished booting and is also waiting for 'r'.
        ser.reset_input_buffer()
        print("Triggering capture ('r')...")
        ser.write(b"r")

        if not wait_for_line(ser, "BEGIN_CSV", timeout=15):
            print("Did not receive BEGIN_CSV marker. Check wiring/port, "
                  "or that the recording sketch is the one currently flashed.")
            sys.exit(1)

        header = ser.readline().decode(errors="ignore").strip()
        rows = []
        while True:
            line = ser.readline().decode(errors="ignore").strip()
            if line == "END_CSV":
                break
            if line:
                rows.append(line.split(","))

        print(f"Received {len(rows)} samples.")

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vibration_{timestamp}.csv"
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header.split(","))
            writer.writerows(rows)

        print(f"Saved to {filename}")
        return filename


def analyze_csv(filename):
    data = np.genfromtxt(filename, delimiter=",", names=True)

    t_us = data["time_us"]
    ax = data["ax"]
    ay = data["ay"]
    az = data["az"]

    n = len(t_us)
    duration_s = (t_us[-1] - t_us[0]) / 1e6
    fs = (n - 1) / duration_s  # actual measured sampling rate, not assumed
    print(f"Samples: {n} | Duration: {duration_s:.3f} s | Actual sampling rate: {fs:.1f} Hz")

    freqs = rfftfreq(n, d=1.0 / fs)

    fig, axes = plt.subplots(3, 2, figsize=(12, 9))
    axis_data = [("X", ax), ("Y", ay), ("Z", az)]

    for row, (label, values) in enumerate(axis_data):
        values_centered = values - np.mean(values)
        rms = np.sqrt(np.mean(values_centered ** 2))

        window = np.hanning(n)
        spectrum = np.abs(rfft(values_centered * window)) * 2 / n

        axes[row][0].plot(t_us / 1000.0, values)
        axes[row][0].set_title(f"Axis {label} - time domain (RMS = {rms:.3f} m/s2)")
        axes[row][0].set_xlabel("Time (ms)")
        axes[row][0].set_ylabel("Acceleration (m/s2)")

        axes[row][1].plot(freqs, spectrum)
        axes[row][1].set_title(f"Axis {label} - amplitude spectrum")
        axes[row][1].set_xlabel("Frequency (Hz)")
        axes[row][1].set_ylabel("Amplitude (m/s2)")
        axes[row][1].set_xlim(0, fs / 2)

        peak_idx = np.argmax(spectrum[2:]) + 2  # skip DC/very-low bins
        print(f"Axis {label}: dominant peak at {freqs[peak_idx]:.1f} Hz, "
              f"amplitude {spectrum[peak_idx]:.4f} m/s2")

    plt.tight_layout()
    png_name = filename.replace(".csv", "_spectrum.png")
    plt.savefig(png_name, dpi=150)
    print(f"Plot saved to {png_name}")
    plt.show()


if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else SERIAL_PORT
    csv_file = capture_to_csv(port=port)
    analyze_csv(csv_file)
