import pytest
from pydantic import ValidationError

from pdm.types import Estimate


def test_estimate_ordering_and_frozen_fields():
    estimate = Estimate(low=1, point=3, high=5, age_days=0, source='rule_fallback')
    with pytest.raises(ValidationError):
        estimate.point = 4
    with pytest.raises(ValidationError):
        Estimate(low=4, point=3, high=5, age_days=0, source='rule_fallback')


def test_nonfinite_estimate_rejected():
    with pytest.raises(ValidationError):
        Estimate(low=0, point=float('nan'), high=5, age_days=0, source='lightgbm')
