import datetime

import numpy as np

START_TIME = datetime.datetime(2021, 1, 1, 0, 0, 0)


def calculate_buffer(y0=100, k=0.1, t_start=datetime.datetime.now(), default=0):
    now = datetime.datetime.now()
    if now < t_start:
        return default
    elapsed = now - t_start
    return y0 * np.exp(-k * elapsed.total_seconds())
