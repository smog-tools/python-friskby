from __future__ import print_function

import sys
import time
from datetime import datetime as dt

from .ts import TS

class FriskbySampler(object):
    """This class is initialized with a reader (a sensor of type SDS011), a dao and
    sample time.  The collect method collects data for `sample_time` amount of
    time, and then asks the FriskbyDao to persist this data.

    """

    def __init__(self, reader, dao, sample_time, sleep_time=0.10, accuracy=None):
        """
        Takes a reader (sensor) and a dao, and collects data and persists to dao.
        """
        self.reader = reader
        self.sample_time = sample_time
        self.sleep_time = sleep_time
        self.accuracy = accuracy
        self.dao = dao

    def collect(self):
        """Reads values from the sensor and writes to dao.
        """
        # reader/sds011 returns (PM10, PM25)
        data = (TS(accuracy=self.accuracy), TS(accuracy=self.accuracy))
        print('\tShh, I am collecting.')
        sys.stdout.flush()
        start = dt.now()
        while True:
            pm10, pm25 = self.reader.read()
            data[0].append(pm10)
            data[1].append(pm25)

            dt_now = dt.now() - start
            if dt_now.total_seconds() >= self.sample_time:
                break
            time.sleep(self.sleep_time)
        print('\tDone collecting, storing and returning.')
        sys.stdout.flush()
        samples = {'PM10': data[0], 'PM25': data[1]}
        self.dao.persist_ts(samples)
