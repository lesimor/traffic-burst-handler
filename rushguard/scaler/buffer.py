import datetime  # datetime 모듈을 import

import numpy as np
import pandas as pd

from rushguard.settings import Settings


def buffer_pod_number(
    traffic_series: pd.Series,
    settings: Settings,
) -> int:
    tb_start_timestamp = datetime.datetime.fromtimestamp(
        settings.traffic_burst_start_timestamp
    )
    pod_elapsed = pod_number_by_elapsed_time_after_traffic_burst_started(
        settings,
        t_start=tb_start_timestamp,
    )
    pod_volatility = pod_number_by_volatility(traffic_series, settings)

    return pod_elapsed + pod_volatility


def pod_number_by_elapsed_time_after_traffic_burst_started(
    settings: Settings,
    t_start=datetime.datetime.now(),
) -> int:
    now = datetime.datetime.now()
    if now < t_start:
        return settings.max_pod_number_by_elapsed_time
    elapsed = now - t_start
    return int(
        settings.max_pod_number_by_elapsed_time
        * np.exp(-settings.buffer_exponential_decay_rate * elapsed.total_seconds())
    )


def pod_number_by_volatility(traffic_series, settings: Settings) -> int:
    buffer_pod_by_trend = int(
        traffic_trend(traffic_series) / settings.qps_capacity_per_pod
    )
    buffer_pod_by_volatility = int(
        volatility_trend(traffic_series) * settings.qps_capacity_per_pod
    )

    return max(buffer_pod_by_trend + buffer_pod_by_volatility, 0)


def traffic_trend(series, short_period=5, long_period=20) -> float:
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


def volatility_trend(time_series_data, window_size=3):
    # 이동평균과 이동표준편차 계산
    rolling_std = time_series_data.rolling(window=window_size).std()

    return traffic_trend(rolling_std)


if __name__ == "__main__":
    # Example usage
    data = [
        1,
        2,
        1,
        2,
        4,
        2,
        6,
        2,
        8,
        10,
    ]
    series = pd.Series(data)
    _traffic_trend = traffic_trend(series, short_period=2)
    _volatility_trend = volatility_trend(series)
    print(_traffic_trend)
    print(_volatility_trend)
