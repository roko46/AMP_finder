"""
Length descriptor: very simple.
"""


def compute(seq: str, pa) -> int:
    # pa (ProteinAnalysis) is provided for consistency but not required here
    return len(seq)
