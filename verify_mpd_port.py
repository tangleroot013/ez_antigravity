#!/usr/bin/env python3
import subprocess
from pathlib import Path

def check_port():
    print("Checking for MPD listener on port 6600...")
    # ss -tulpn looks for TCP, UDP, Listening, Process info, Numeric ports
    res = subprocess.run(["ss", "-tulpn"], capture_output=True, text=True)
    if "6600" in res.stdout and "mpd" in res.stdout.lower():
        print("✅ SUCCESS: MPD is listening on port 6600.")
        return True
    else:
        print("❌ FAIL: No MPD listener found. Attempting service restart...")
        subprocess.run(["systemctl", "--user", "restart", "mpd.service"])
        # Give it a second to bind
        import time
        time.sleep(1)
        res_retry = subprocess.run(["ss", "-tulpn"], capture_output=True, text=True)
        if "6600" in res_retry.stdout:
            print("✅ SUCCESS: MPD started and is now listening.")
            return True
        print("❌ FAIL: MPD refuses to bind. Check 'journalctl --user -u mpd'.")
        return False

if __name__ == "__main__":
    if check_port():
        print("\nExecuting final health check...")
        doctor = Path.home() / "ez_jukebox_doctor.py"
        if doctor.is_file():
            subprocess.run(["python3", str(doctor)])
        else:
            print(f"Skipping final health check; missing {doctor}")
