from collections import deque

from log import init_log


TEMPLATE = """
<!DOCTYPE html>
<html>
<body>

<h2>Temperature report</h2>

<p>Max temperature: {_max}</p>
<p>Min temperature: {_min}</p>
<p>Samples: {_samples}</p>
<p>Average temperature: {_avg}</p>

<h2>Detail:</h2>
{detail}
</body>
</html>
"""


class Statistic:
    """ Receive temperatures values over the time
        Calculate the average, max, min value
    """
    def __init__(self, *, maxlen, log_level):
        self.queue = deque(maxlen=maxlen)
        self.log = init_log(log_name="Statistic", log_level=log_level)
        self.__min = None
        self.__max = None
        self.__avg = None
        self.__sum = 0
        self.__len = 0

    def add(self, value, time):
        """ Add a dic {"time": str, "value": int}"""
        self.__len = min(self.__len + 1, self.queue.maxlen)
        if self.__len == self.queue.maxlen:
            self.__sum -= self.queue[-1]['value']
        self.queue.append({"value": value, "time": time})
        self.__sum += value
        self.__avg = self.__sum / self.__len
        self.__min = min(self.__min, value) if self.__min else value
        self.__max = max(self.__max, value) if self.__max else value
        self.log.debug(f"Added new value: {value}. Queue: {self.queue}")

    def report(self):
        detail = [f"<h6>{v['time']}: {v['value']}<h6>" \
                  for v in list(self.queue)]
        detail_str = '\n'.join(detail)
        return TEMPLATE.format(
            _max=self.__max,
            _min=self.__min,
            _avg=self.__avg,
            _samples=self.__len,
            detail=detail_str,
        )
