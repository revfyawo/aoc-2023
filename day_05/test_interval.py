from day_05.main import Interval, IntervalMap


def test_interval_contains():
    interval = Interval(0, 10)
    for i in range(10):
        assert i in interval
    assert -1 not in interval
    assert 10 not in interval


def test_interval_intersection():
    cases = [
        {
            "first": Interval(0, 10),
            "second": Interval(1, 1),
            "expected": Interval(1, 1),
        },
        {
            "first": Interval(0, 10),
            "second": Interval(10, 10),
            "expected": Interval(0, 0),
        },
        {
            "first": Interval(0, 10),
            "second": Interval(5, 10),
            "expected": Interval(5, 5),
        },
        {
            "first": Interval(5, 10),
            "second": Interval(0, 10),
            "expected": Interval(5, 5),
        },
    ]
    for case in cases:
        assert case["first"] & case["second"] == case["expected"]


def test_interval_split_disjoint():
    cases = [
        {
            "first": Interval(0, 10),
            "second": Interval(5, 2),
            "expected": [Interval(0, 5), Interval(5, 2), Interval(7, 3)],
        },
        {
            "first": Interval(0, 10),
            "second": Interval(5, 10),
            "expected": [Interval(0, 5), Interval(5, 5), Interval(10, 5)],
        },
    ]
    for case in cases:
        assert case["first"].split_disjoint(case["second"]) == case["expected"]
        assert case["second"].split_disjoint(case["first"]) == case["expected"]


def test_interval_split_by():
    cases = [
        {
            "first": Interval(0, 10),
            "second": Interval(5, 2),
            "expected": [Interval(0, 5), Interval(5, 2), Interval(7, 3)],
        },
        {
            "first": Interval(0, 10),
            "second": Interval(5, 10),
            "expected": [Interval(0, 5), Interval(5, 5)],
        },
        {
            "first": Interval(5, 10),
            "second": Interval(5, 10),
            "expected": [Interval(5, 10)],
        },
        {
            "first": Interval(5, 10),
            "second": Interval(0, 10),
            "expected": [Interval(5, 5), Interval(10, 5)],
        },
        {
            "first": Interval(5, 2),
            "second": Interval(0, 10),
            "expected": [Interval(5, 2)],
        },
    ]
    for case in cases:
        assert case["first"].split_by(case["second"]) == case["expected"]
