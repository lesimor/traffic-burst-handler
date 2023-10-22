import datetime  # datetime 모듈을 import

import numpy as np  # numpy 모듈을 import


def calculate_buffer(
    y0=100,  # 초기값 y0를 100으로 설정
    k=0.001,  # 상수 k를 0.001로 설정
    t_start=datetime.datetime.now(),  # t_start를 현재 시간으로 설정
    default=0,  # default 값을 0으로 설정
) -> int:  # 함수의 반환값은 정수형
    now = datetime.datetime.now()  # 현재 시간을 now 변수에 저장
    if now < t_start:  # 현재 시간이 t_start보다 작으면
        return default  # default 값을 반환
    elapsed = now - t_start  # 현재 시간과 t_start의 차이를 elapsed 변수에 저장
    return int(
        y0 * np.exp(-k * elapsed.total_seconds())
    )  # y0에 np.exp(-k * elapsed.total_seconds())를 곱한 후 정수형으로 반환
