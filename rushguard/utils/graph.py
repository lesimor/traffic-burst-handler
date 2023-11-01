import datetime

import matplotlib.pyplot as plt


def generate_graph(times, values, output_file=None):
    # 그래프 생성
    plt.figure(figsize=(10, 6))

    # x축에는 시간, y축에는 값이 옵니다.
    plt.plot(times, values, marker="o", drawstyle="steps-post")

    # 그래프에 제목과 레이블을 붙입니다.
    plt.title("Scaling Over Time")
    plt.xlabel("Time")
    plt.ylabel("Scale")
    plt.grid(True)

    # x축 레이블을 더 읽기 쉽게 만듭니다.
    plt.gcf().autofmt_xdate()

    # # 각 꺾이는 지점에 시간을 표시합니다.
    # for time, value in zip(times, values):
    #     # 시간 포맷을 조정하고 어노테이션을 추가합니다.
    #     time_text = time.strftime("%H:%M:%S")  # 시간을 문자열로 변환
    #     plt.annotate(
    #         time_text,
    #         (mdates.date2num(time), value),
    #         textcoords="offset points",
    #         xytext=(0, 10),
    #         ha="center",
    #         fontsize=8,
    #     )

    plt.tight_layout()
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()


if __name__ == "__main__":
    time_series = [
        (datetime.datetime(2023, 10, 26, 10, 28, 29), 3),
        (datetime.datetime(2023, 10, 26, 10, 32, 36), 6),
        (datetime.datetime(2023, 10, 26, 10, 33, 7), 7),
        (datetime.datetime(2023, 10, 26, 10, 34, 39), 11),
        (datetime.datetime(2023, 10, 26, 10, 35, 40), 8),
        (datetime.datetime(2023, 10, 26, 10, 36, 11), 14),
        (datetime.datetime(2023, 10, 26, 10, 36, 41), 27),
        (datetime.datetime(2023, 10, 26, 10, 37, 12), 20),
        (datetime.datetime(2023, 10, 26, 10, 37, 43), 14),
        (datetime.datetime(2023, 10, 26, 10, 38, 14), 12),
        (datetime.datetime(2023, 10, 26, 10, 38, 44), 13),
        (datetime.datetime(2023, 10, 26, 10, 39, 15), 14),
        (datetime.datetime(2023, 10, 26, 10, 40, 7), 14),
    ]
    _times = [time[0] for time in time_series]
    _values = [time[1] for time in time_series]

    generate_graph(_times, _values)
