# app.py
"""
Streamlit UI for AMP Finder — enhanced with charts and caching guidance.
"""
import streamlit as st
import matplotlib.pyplot as plt

from amp_finder.utils.sequence_utils import clean_sequence, validate_sequence
from amp_finder.core.analysis import analyze_sequence

# Optional: if you'd rather use Streamlit's cache (instead of lru_cache in core),
# you can create a wrapper here:
# @st.cache_data(max_entries=128)
# def analyze_sequence_cached(seq: str):
#     return analyze_sequence(seq)
#
# then call analyze_sequence_cached(seq) below.
#
# I left the core caching implemented via functools.lru_cache; feel free to switch.

st.set_page_config(page_title="AMP Finder", page_icon="🧬", layout="wide")
st.title("🧬 AMP Finder — enhanced demo")

st.markdown(
    """
This educational app computes physicochemical descriptors of peptide sequences and shows
a simple heuristic AMP-likeness score. It now includes:
- automatic descriptor discovery (drop-in modules),
- result caching for quick repeated queries,
- a residue composition bar chart.
"""
)

with st.sidebar:
    st.header("About")
    st.markdown(
        "- The heuristic score is educational only and not a validated predictor.\n"
        "- Add new descriptor modules under `amp_finder/descriptors/` — they'll be discovered automatically."
    )
    st.markdown("---")
    st.write("Example sequences")
    st.code("KWKLFKKIGAVLKVL")
    st.code("GIGKFLHSAKKFGKAFVGEIMNS")

seq_input = st.text_area("Peptide sequence (one-letter codes):", value="KWKLFKKIGAVLKVL", height=140)

col_left, col_right = st.columns([2, 1])

with col_right:
    if st.button("Analyze"):
        seq = clean_sequence(seq_input)
        valid, msg = validate_sequence(seq)
        if not valid:
            st.error(msg)
        else:
            # Call analysis (cached internally)
            result = analyze_sequence(seq)
            descriptors = result["descriptors"]
            score = result["score"]

            st.success(f"Analyzed sequence: **{seq}**")
            st.metric("Heuristic AMP-likeness", f"{score['amp_score']} / 100")
            st.write("**Key descriptors**")
            st.write(f"- Length: {descriptors.get('length', len(seq))}")
            st.write(f"- Molecular weight: {descriptors.get('molecular_weight', 'N/A')}")
            st.write(f"- GRAVY (hydropathy): {descriptors.get('gravy', 'N/A')}")
            st.write(f"- Instability index: {descriptors.get('instability_index', 'N/A')}")
            st.write(f"- pI: {descriptors.get('isoelectric_point', 'N/A')}")
            st.write(f"- Charge at pH7: {descriptors.get('charge_at_pH7', descriptors.get('charge', 'N/A'))}")
            st.write(f"- Hydrophobic fraction: {descriptors.get('hydrophobic_fraction', 'N/A')}")

with col_left:
    # Detailed JSON
    st.subheader("Descriptor details")
    st.json(result["descriptors"])

    # Residue composition plot (if available)
    aa_counts = result["descriptors"].get("amino_acid_counts", {})
    if aa_counts:
        st.subheader("Residue composition")
        # Prepare bar chart via matplotlib for consistent appearance
        labels = sorted(aa_counts.keys())
        values = [aa_counts[a] for a in labels]

        fig, ax = plt.subplots(figsize=(10, 3))
        ax.bar(labels, values)
        ax.set_xlabel("Residue")
        ax.set_ylabel("Count")
        ax.set_title("Amino Acid Composition")
        ax.margins(x=0)

        st.pyplot(fig)
    else:
        st.info("Amino acid counts not available for this sequence.")
