import datetime  # datetime 모듈을 import

import numpy as np
import pandas as pd


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


def analyze_trend(series, short_period=5, long_period=20) -> float:
    """
    Analyze trend by comparing short-term and long-term averages.

    Parameters:
    - series: A pandas Series of time series values.
    - short_period: The period for the short-term average.
    - long_period: The period for the long-term average.

    Returns:
    - difference between short-term and long-term averages. \
        Positive values indicate an upward trend, negative \
        values indicate a downward trend.
    """

    short_avg = series[-short_period:].mean()
    long_avg = series[-long_period:].mean()

    return short_avg - long_avg


if __name__ == "__main__":
    # Example usage
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5]
    series = pd.Series(data)
    trend = analyze_trend(series, short_period=2)
    print(trend)
