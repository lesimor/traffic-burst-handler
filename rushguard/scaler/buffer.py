import datetime

import numpy as np


def calculate_buffer(
    y0=100,
    k=0.001,
    t_start=datetime.datetime.now(),
    default=0,
) -> int:
    now = datetime.datetime.now()
    if now < t_start:
        return default
    elapsed = now - t_start
    return int(y0 * np.exp(-k * elapsed.total_seconds()))
