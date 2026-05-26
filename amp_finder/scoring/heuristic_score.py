"""
Simple, transparent heuristic AMP-likeness score.

This is NOT a trained model — it's a pedagogical weighted sum that
combines charge, hydrophobicity, length, and stability into a 0..100 score.
"""


def compute(descriptors: dict) -> dict:
    """
    descriptors: dictionary with keys:
      - length
      - gravy
      - charge_at_pH7
      - instability_index
      - hydrophobic_fraction
    Returns a dict with component scores and final amp_score.
    """
    length = descriptors.get("length", 0)
    gravy = descriptors.get("gravy", 0.0)
    charge = descriptors.get("charge_at_pH7", 0.0)
    instability = descriptors.get("instability_index", 100.0)
    hydrophobic_fraction = descriptors.get("hydrophobic_fraction", 0.0)

    # length_score: reward peptides close to ~20 residues (this is arbitrary for demo)
    length_score = max(0.0, 1.0 - abs(length - 20) / 40.0)

    # charge_score: normalize roughly from -5..+10 -> 0..1
    charge_norm = (charge + 5.0) / 15.0
    charge_score = min(max(charge_norm, 0.0), 1.0)

    # hydrophobicity: reward moderate hydrophobic fraction (center 0.35)
    hydrophobic_score = max(0.0, 1.0 - abs(hydrophobic_fraction - 0.35) / 0.6)

    # stability: lower instability index is better (arbitrary scaling)
    stability_score = max(0.0, 1.0 - instability / 120.0)

    # weighted combination with conservative weights
    combined = (
        0.35 * charge_score
        + 0.30 * hydrophobic_score
        + 0.20 * length_score
        + 0.15 * stability_score
    )

    amp_score = round(100.0 * combined, 2)

    return {
        "length_score": round(length_score, 3),
        "charge_score": round(charge_score, 3),
        "hydrophobic_score": round(hydrophobic_score, 3),
        "stability_score": round(stability_score, 3),
        "combined_weighted": round(combined, 4),
        "amp_score": amp_score,
    }
