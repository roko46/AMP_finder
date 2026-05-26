"""
Approximate net charge at pH 7.

We attempt to use ProteinAnalysis. If it fails, fall back to crude
basic-minus-acidic count.
"""


def compute(seq: str, pa) -> float:
    try:
        return pa.charge_at_pH(7.0)
    except Exception:
        counts = pa.count_amino_acids()
        basic = counts.get("K", 0) + counts.get("R", 0) + counts.get("H", 0)
        acidic = counts.get("D", 0) + counts.get("E", 0)
        return basic - acidic
