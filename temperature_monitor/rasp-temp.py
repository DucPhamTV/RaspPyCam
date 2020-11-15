import os
import time

import settings as cfg


# how often the script reads from temperature file
READ_INTERVAL = os.getenv("READ_INTERVAL", 2)
# how often the script updates to temperature result file
WRITE_INTERVAL = os.getenv("WRITE_INTERVAL", 10)
# teperature result file
RESULT_FILE = os.getenv("RESULT_FILE", "/var/www/html/temperature.html")


if __name__ == "__main__":
    counter = 0
    with open(cfg.RESULT_FILE, 'a') as writer:
        while True:
            time.sleep(cfg.READ_INTERVAL)
            with open("/sys/class/thermal/thermal_zone0/temp") as reader:
                try:
                    text = reader.read()
                    temperature = int(text.strip())
                except Exception as e:
                    print(f"Exception : {e}")

            writer.write(f"<h3>{temperature}<h3>")
            counter += 1
            if counter % (cfg.WRITE_INTERVAL // cfg.READ_INTERVAL) == 0:
                print(f"Flushing...{counter}")
                writer.flush()
