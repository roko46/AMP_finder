"""
Instability index as implemented by ProtParam / Biopython.
Lower values typically indicate more stable proteins (but interpretation for short peptides is limited).
"""

def compute(seq: str, pa) -> float:
    return pa.instability_index()
