import pytest

from ml_project.two_numbers import TwoNumbers


def test_zero_zero(zero_zero):
    """Uses the fixture zero_zero defined in conftest.py."""
    assert zero_zero.add() == 0


@pytest.mark.parametrize(
    "num_1, num_2, add_result",
    [
        (-1, 1, 0),
        (-1, 0, -1),
        (-1, -1, -2),
        (0, 1, 1),
        (0, 0, 0),
        (0, -1, -1),
        (1, 1, 2),
    ],
)
def test_many_adds(num_1, num_2, add_result):
    assert TwoNumbers(num_1, num_2).add() == add_result


@pytest.mark.parametrize(
    "num_1, num_2",
    [
        (-1, 1),
        (-1, 0),
        (0, 1),
        (0, -1),
    ],
)
def test_swap_consistency(num_1, num_2):
    """Test consistency when swapping the order of the numbers."""
    assert TwoNumbers(num_1, num_2).add() == TwoNumbers(num_2, num_1).add()


@pytest.mark.xfail(raises=AssertionError)
def test_check_invalid():
    """Test if add() raises an AssertionError."""
    TwoNumbers(1, "a").add()


@pytest.mark.parametrize(
    "num_1, num_2",
    [
        ("a", 1),
        ("a", "b"),
        (1.1, 1),
        (0, -1.1),
    ],
)
@pytest.mark.xfail(raises=AssertionError)
def test_many_check_invalid(num_1, num_2):
    """Test if add() raises an AssertionError."""
    TwoNumbers(num_1, num_2).add()
