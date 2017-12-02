import datetime
import time
import cv2
import os

def get_image(camera, ramp_frames=10):
    for i in range(ramp_frames):
        camera.read()

    retval, im = camera.read()
    if retval == False:
        return -1
    print(len(im))
    return im

class ImageCaptured:

    def __init__(self, data, storage):
        self.data = data
        self.timestamp = time.time()
        self.storage = storage
        self.date_path = ""
        self.hour_path = ""
        self.image_name = ""

    def save_image(self):
        self._filename_from_time()
        file_location = os.path.join(self.storage, self.date_path, self.hour_path)
        file_name = os.path.join(file_location, self.image_name)
        print(file_name)
        if not os.path.isdir(file_location):
            print("haven't created this path yet")
            os.makedirs(file_location)
        return cv2.imwrite(file_name, self.data)

    def _filename_from_time(self):
        ''' timestamp to date and time
            A date with 1 dir, in a day, we seperate to 24 hours is 24 dirs
            date directory: dd_mm_yy
            time directory: <hour> (in 24 hours)
            file-name format: hh_mm_ss.png
        :return: retval
        '''
        print(self.timestamp)
        date_time = datetime.datetime.fromtimestamp(self.timestamp)
        hour = date_time.hour
        date_time_str = date_time.strftime('%Y_%m_%d %H_%M_%S')
        self.date_path = date_time_str.split(" ")[0]
        self.image_name = date_time_str.split(" ")[1] + ".png"
        self.hour_path = str(hour)
