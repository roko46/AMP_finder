"""
Aromaticity: fraction of aromatic residues (F, W, Y)
"""

def compute(seq: str, pa) -> float:
    return pa.aromaticity()
