import logging


def init_log(*, log_name, log_level):
    log = logging.getLogger(log_name)
    log.setLevel(log_level)
    file_handler = logging.FileHandler('temper.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    return log
