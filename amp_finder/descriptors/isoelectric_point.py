"""
Theoretical isoelectric point using Biopython.
"""


def compute(seq: str, pa):
    try:
        return pa.isoelectric_point()
    except Exception:
        return None
