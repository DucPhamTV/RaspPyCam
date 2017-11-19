import cv2
import sys
import datetime
import time
from image import get_image, ImageCaptured
from circular_buffer import Circular

if __name__ == "__main__" :
    storage = sys.argv[1]
    port = sys.argv[2]
    ramp_frames = sys.argv[3]
    camera = cv2.VideoCapture(int(port))
    circular = Circular()
    while (cv2.waitKey(1) & 0xFF != ord('q')):
        time.sleep(1)
        image_data = get_image(camera, int(ramp_frames))
        time_now = time.time()
        image = ImageCaptured(image_data, time_now, storage)
        image.filename_from_time()
        image.save_image()
        circular.check_and_clean()

