import pytest

from ml_project.two_numbers import TwoNumbers


@pytest.fixture(scope="session")
def zero_zero():
    return TwoNumbers(0, 0)
