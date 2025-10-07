import pytest
from amp_finder.utils.sequence_utils import clean_sequence, validate_sequence

def test_clean_sequence_basic():
    assert clean_sequence(" aC d e ") == "ACDE"

def test_validate_good():
    ok, msg = validate_sequence("ACDEFGHIK")
    assert ok

def test_validate_bad_chars():
    ok, msg = validate_sequence("ACDXZ")
    assert not ok
    assert "non-standard" in msg.lower() or "non-standard" in msg
