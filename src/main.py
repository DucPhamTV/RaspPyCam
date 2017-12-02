import argparse
import cv2
import datetime
import logging
import time

from image import get_image, ImageCaptured
from circular_buffer import Circular

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('main.log')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(prog='RaspPyCam',
                                     description="RaspPyCam project version 1.0.0",
                                     epilog="Any issue realtive please contact "
                                            "phamcongduc1994@gmail.com. Thank you")
    parser.add_argument('-o', dest='storage', type=str, nargs='?', default='.',
                        help="Storage path, default is pwd")
    parser.add_argument('-p', dest='port', type=int, nargs='?', default=0,
                        help="Webcam port, default is 0")
    parser.add_argument('-r', dest='ramp', type=int, nargs='?', default=1,
                        help="ramp frames before getting final frame")
    parser.add_argument('-t', dest='interval_time', type=float, nargs='?', default=1,
                        help="time between 2 frames, unit is second")
    parser.add_argument('-c', dest='circular', type=int, nargs='?', default=2000,
                        help="circular size, unit is MB")
    parser.add_argument('-l', dest='log_level', type=int, nargs='?', default=3,
                        help="Log level: 1-Error, 2-Warning, 3-Info, 4-Debug")
    args = parser.parse_args()

    storage = args.storage
    port = args.port
    ramp_frames = args.ramp
    interval = args.interval_time
    circular_size = args.circular

    logger.setLevel(logging.INFO)
    logger.info(args)
    camera = cv2.VideoCapture(port)
    circular = Circular(threshold=circular_size)

    while (cv2.waitKey(1) & 0xFF != ord('q')):
        time.sleep(interval)
        image_data = get_image(camera, ramp_frames)
        image = ImageCaptured(image_data, storage)
        image.save_image(circular)
        circular.check_and_clean()

