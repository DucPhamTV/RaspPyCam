import logging
import shutil
import os

logger = logging.getLogger(__name__)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('circular.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


class Circular:
    """
    Clean base on total size of images
    threshold default is 2000MB
    """
    def __init__(self, threshold = 200000000):
        self.total_size = 0
        self.total_images = 0
        self.list_dir = []      # 0 is the oldest dir
        self.threshold = threshold

    def check_and_clean(self):
        if (self.total_size < self.threshold):
            logger.debug("total_size %s total_images %s"
                         % (self.total_size, self.total_images))
            return 0

        if (os.path.isdir(self.list_dir[0])):
            remove_size = self._calculate_dir_size(self.list_dir[0])
            shutil.rmtree(self.list_dir[0])
            self.total_size -= remove_size
            logger.warn("Circular is full, cleared %s, size %s"
                        % (self.list_dir[0], remove_size))
            return 0

        logger.error("%s does not exist" % self.list_dir[0])
        del self.list_dir[0]
        return 1

    def update(self, directory):
        self.total_size = self._calculate_dir_size("/tmp/temp-image/")
        self.total_images += 1
        if directory in self.list_dir:
            return 0
        self.list_dir.append(directory)
        logger.debug("add new dir to circular %s" % directory)

    def _calculate_dir_size(self, directory):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)

        return total_size