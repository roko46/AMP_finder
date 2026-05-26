"""
Sequence cleaning and validation helpers.

- clean_sequence: remove whitespace, non-letters, uppercase
- validate_sequence: ensures non-empty, minimal length, only standard 20 amino acids
"""

import re

VALID_AA = set(list("ACDEFGHIKLMNPQRSTVWY"))  # 20 standard amino acids


def clean_sequence(seq: str) -> str:
    if seq is None:
        return ""
    # remove whitespace and non-alpha characters, uppercase
    s = re.sub(r"\s+", "", seq).upper()
    s = re.sub(r"[^A-Z]", "", s)
    return s


def validate_sequence(seq: str) -> (bool, str):
    if not seq:
        return False, "Empty sequence."
    if len(seq) < 3:
        return False, "Sequence too short (minimum 3 residues)."
    bad = [c for c in seq if c not in VALID_AA]
    if bad:
        return False, f"Sequence contains non-standard residues: {sorted(set(bad))}"
    return True, "OK"
