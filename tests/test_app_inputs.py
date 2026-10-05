"""Four-silo/story alignment and quality firewall for the Streamlit adapter."""
import pytest

from vayu.quality import planning_state_from_fleet, validate_fleet_pack
from vayu.sim import story_silos, whatif_demo_state


def test_story_silos_describe_the_planning_resources_and_rates() -> None:
    state = whatif_demo_state()
    frames = story_silos(state)
    report = validate_fleet_pack(frames)
    assert not report.planning_hold and report.quarantine.empty
    predictions = {f'E-{i:02d}': {'rul_point': t.rul_point, 'lower': t.lower, 'upper': t.upper}
                   for i, t in enumerate(sorted(state.tails, key=lambda t: t.tail_id), start=1)}
    reconstructed = planning_state_from_fleet(report, predictions, safety_buffer=0)
    assert {t.tail_id: t.rate for t in reconstructed.tails} == {t.tail_id: t.rate for t in state.tails}
    assert len(reconstructed.bays) == len(state.bays) and len(reconstructed.crews) == len(state.crews)
    assert {s.spare_id: s.available_day for s in reconstructed.spares} == {s.spare_id: s.available_day for s in state.spares}
    assert frames['tech_records.csv'].equals(story_silos(state)['tech_records.csv'])


def test_adapter_refuses_hold_or_missing_prediction() -> None:
    frames = story_silos(whatif_demo_state())
    clean = validate_fleet_pack(frames)
    with pytest.raises(ValueError, match='prediction'):
        planning_state_from_fleet(clean, {})
    frames['tails.csv'].loc[3, 'utilisation_cycles_per_day'] = 0
    held = validate_fleet_pack(frames)
    with pytest.raises(ValueError, match='hold'):
        planning_state_from_fleet(held, {})
