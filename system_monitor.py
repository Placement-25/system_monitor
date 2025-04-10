import psutil
import time
import logging
from datetime import datetime
import argparse
import platform
import os

class SystemMonitor:
    def __init__(self, interval: int = 5, log_file: str = "system_monitor.log"):
        self.interval = interval
        self.log_file = log_file
        self.setup_logger()

    def setup_logger(self):
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logging.info("System Monitor Started")

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1, percpu=True)

    def get_memory_usage(self):
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "percent": mem.percent,
        }

    def get_disk_usage(self):
        disk = psutil.disk_usage('/')
        return {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent,
        }

    def get_system_info(self):
        return {
            "platform": platform.system(),
            "platform-release": platform.release(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
        }

    def display_metrics(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        cpu = self.get_cpu_usage()
        memory = self.get_memory_usage()
        disk = self.get_disk_usage()

        print("="*50)
        print(f"SYSTEM RESOURCE MONITOR  —  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
        print("\n CPU Usage per Core:")
        for i, core in enumerate(cpu):
            print(f"  - Core {i}: {core:.2f}%")

        print("\n Memory Usage:")
        print(f"  - Total     : {self.format_bytes(memory['total'])}")
        print(f"  - Available : {self.format_bytes(memory['available'])}")
        print(f"  - Used      : {self.format_bytes(memory['used'])}")
        print(f"  - Usage     : {memory['percent']}%")

        print("\n Disk Usage (/):")
        print(f"  - Total : {self.format_bytes(disk['total'])}")
        print(f"  - Used  : {self.format_bytes(disk['used'])}")
        print(f"  - Free  : {self.format_bytes(disk['free'])}")
        print(f"  - Usage : {disk['percent']}%")
        print("\n(Press Ctrl+C to exit)")

    def log_metrics(self):
        cpu = self.get_cpu_usage()
        memory = self.get_memory_usage()
        disk = self.get_disk_usage()

        logging.info(f"CPU Usage: {cpu}")
        logging.info(f"Memory Usage: {memory}")
        logging.info(f"Disk Usage: {disk}")

    @staticmethod
    def format_bytes(size):
        # Convert bytes to a human-readable format
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

    def run(self):
        try:
            system_info = self.get_system_info()
            logging.info(f"System Info: {system_info}")
            while True:
                self.display_metrics()
                self.log_metrics()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
            logging.info("System Monitor Stopped")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="System Resource Monitor")
    parser.add_argument("--interval", type=int, default=5, help="Monitoring interval in seconds")
    parser.add_argument("--log", type=str, default="system_monitor.log", help="Log file name")
    args = parser.parse_args()

    monitor = SystemMonitor(interval=args.interval, log_file=args.log)
    monitor.run()
