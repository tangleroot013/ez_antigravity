import subprocess
import psutil
import time
import sys
import argparse


def monitor_command(cmd, threshold_mb):
    print(f"🦆 Sentry: Monitoring command: {cmd} (Threshold: {threshold_mb}MB)")
    try:
        # Start the process
        proc = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        p = psutil.Process(proc.pid)

        max_rss = 0
        # Sample aggressively until the process finishes
        while proc.poll() is None:
            try:
                current_rss = p.memory_info().rss / (1024 * 1024)
                if current_rss > max_rss:
                    max_rss = current_rss
            except psutil.NoSuchProcess:
                break
            time.sleep(0.01)

        # Final check if it finished extremely quickly
        try:
            final_rss = p.memory_info().rss / (1024 * 1024)
            max_rss = max(max_rss, final_rss)
        except psutil.NoSuchProcess:
            # If it's gone and max_rss is still 0, it finished faster than our first sample
            if max_rss == 0:
                print("⚡ Process finished too fast to sample. Assuming no leak.")
                return True

        print(f"✅ Peak Memory Footprint: {max_rss:.2f} MB")
        if max_rss > threshold_mb:
            print(f"🚩 LEAK DETECTED: {max_rss:.2f} MB exceeds {threshold_mb} MB!")
            return False
        return True

    except Exception as e:
        print(f"❌ Sentry Error: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="The command to monitor")
    parser.add_argument(
        "--threshold", type=float, default=100.0, help="Memory threshold in MB"
    )
    args = parser.parse_args()

    if monitor_command(args.command, args.threshold):
        sys.exit(0)
    else:
        sys.exit(1)
