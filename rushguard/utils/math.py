def decay_function(current, _max, _min, span):
    b = _max
    a = b / span
    return max(-a * current + b, _min)


if __name__ == "__main__":
    assert decay_function(0, 100, 0, 100) == 100
    assert decay_function(50, 100, 0, 100) == 50
