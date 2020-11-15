#!/usr/bin/python3
import os
import time
from datetime import datetime

import settings as cfg
from log import init_log
from statistic import Statistic



if __name__ == "__main__":
    log = init_log(log_name="Main", log_level=cfg.LOG_LEVEL)
    counter = 0
    stat = Statistic(maxlen=20, log_level=cfg.LOG_LEVEL)
    while True:
        with open("/sys/class/thermal/thermal_zone0/temp") as reader:
            try:
                text = reader.read()
                temperature = int(text.strip())
            except Exception as e:
                log.error(f"Exception : {e}")
        sample_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        stat.add(temperature, sample_time)
        counter += 1
        if counter % (cfg.WRITE_INTERVAL // cfg.READ_INTERVAL) == 0:
            log.info(f"Write new report...{counter}")
            report = stat.report()
            with open(cfg.RESULT_FILE, 'w') as writer:
                writer.write(report)
        time.sleep(cfg.READ_INTERVAL)
