from amp_finder.scoring.heuristic_score import compute as score_compute


def test_score_output_shape():
    descriptors = {
        "length": 16,
        "gravy": 0.1,
        "charge_at_pH7": 3,
        "instability_index": 40,
        "hydrophobic_fraction": 0.3,
    }
    s = score_compute(descriptors)
    assert "amp_score" in s
    assert 0.0 <= s["amp_score"] <= 100.0
