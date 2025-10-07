"""
Hydrophobic fraction: fraction of residues considered hydrophobic.

We use a simple set of hydrophobic residues (A, I, L, M, F, V, W, Y).
"""

HYDROPHOBIC = set("AILMFVWY")

def compute(seq: str, pa) -> float:
    counts = pa.count_amino_acids()
    length = len(seq)
    if length == 0:
        return 0.0
    hydrophobic_count = sum(counts.get(r, 0) for r in HYDROPHOBIC)
    return hydrophobic_count / length
