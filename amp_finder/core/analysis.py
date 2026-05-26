"""
Orchestration layer: compute all descriptors (re-using a single ProteinAnalysis object)
and call the scoring function.

This centralizes logic so UI code remains simple and testable.
"""

from Bio.SeqUtils.ProtParam import ProteinAnalysis

from amp_finder.descriptors import (
    aromaticity,
    charge,
    hydrophobicity,
    instability,
    isoelectric_point,
    length,
    molecular_weight,
)
from amp_finder.scoring.heuristic_score import compute as compute_score


def analyze_sequence(seq: str) -> dict:
    pa = ProteinAnalysis(seq)  # compute once and pass to modules
    descriptors = {
        "length": length.compute(seq, pa),
        "molecular_weight": molecular_weight.compute(seq, pa),
        "hydrophobic_fraction": hydrophobicity.compute(seq, pa),
        "charge_at_pH7": charge.compute(seq, pa),
        "instability_index": instability.compute(seq, pa),
        "aromaticity": aromaticity.compute(seq, pa),
        "isoelectric_point": isoelectric_point.compute(seq, pa),
        "gravy": pa.gravy(),
        "amino_acid_counts": pa.count_amino_acids(),
        "amino_acid_percent": pa.amino_acids_percent,
    }
    score = compute_score(descriptors)
    return {"descriptors": descriptors, "score": score}
