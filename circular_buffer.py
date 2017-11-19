import shutil
import os

class Circular:
    """
    Clean base on total size of images
    threshold default is 2000MB
    """
    def __init__(self, threshold = 2000):
        self.total_size = 0
        self.total_images = 0
        self.list_dir = []      # 0 is the oldest dir
        self.threshold = threshold

    def check_and_clean(self):
        if (self.total_size < self.threshold):
            return 0
        if (os.path.isdir(self.list_dir[0])):
            shutil.rmtree(self.list_dir[0])
            return 1
        print("Can't find any dir in list")
        del self.list_dir[0]
        return -1