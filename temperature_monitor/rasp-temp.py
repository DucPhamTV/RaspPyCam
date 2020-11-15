#!/usr/bin/python3
import os
import time

import settings as cfg
from log import init_log



if __name__ == "__main__":
    log = init_log(log_name="Main", log_level=cfg.LOG_LEVEL)
    counter = 0
    with open(cfg.RESULT_FILE, 'a') as writer:
        while True:
            time.sleep(cfg.READ_INTERVAL)
            with open("/sys/class/thermal/thermal_zone0/temp") as reader:
                try:
                    text = reader.read()
                    temperature = int(text.strip())
                except Exception as e:
                    log.error(f"Exception : {e}")

            writer.write(f"<h3>{temperature}<h3>")
            counter += 1
            if counter % (cfg.WRITE_INTERVAL // cfg.READ_INTERVAL) == 0:
                log.info(f"Write new report...{counter}")
                writer.flush()
