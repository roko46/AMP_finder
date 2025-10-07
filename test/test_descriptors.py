from Bio.SeqUtils.ProtParam import ProteinAnalysis
from amp_finder.descriptors import length, molecular_weight, hydrophobicity, charge, instability, aromaticity, isoelectric_point

SEQ = "KWKLFKKIGAVLKVL"  # example peptide

def test_length():
    assert length.compute(SEQ, None) == len(SEQ)

def test_proteinanalysis_present():
    pa = ProteinAnalysis(SEQ)
    assert isinstance(pa.count_amino_acids(), dict)

def test_molecular_weight():
    pa = ProteinAnalysis(SEQ)
    mw = molecular_weight.compute(SEQ, pa)
    assert mw > 0

def test_hydrophobic_fraction():
    pa = ProteinAnalysis(SEQ)
    hf = hydrophobicity.compute(SEQ, pa)
    assert 0.0 <= hf <= 1.0

def test_charge():
    pa = ProteinAnalysis(SEQ)
    c = charge.compute(SEQ, pa)
    assert isinstance(c, (int, float))
