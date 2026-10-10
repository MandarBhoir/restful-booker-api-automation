import pytest


@pytest.mark.skip(
    reason="Demonstration only: this test is intentionally skipped."
)
def test_skipped_example():
    """Demonstrate pytest's skip marker."""
    assert True


@pytest.mark.xfail(
    reason="Demonstration only: this assertion is intentionally expected to fail.",
    strict=True
)
def test_expected_failure_example():
    """Demonstrate pytest's expected-failure marker."""
    assert 1 == 2
