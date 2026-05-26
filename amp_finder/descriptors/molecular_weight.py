"""
Molecular weight descriptor using Biopython ProteinAnalysis.
"""


def compute(seq: str, pa) -> float:
    return pa.molecular_weight()
