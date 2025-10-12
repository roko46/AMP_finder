# app.py
"""
Streamlit UI for AMP Finder — enhanced with charts, session-state, and custom styling.
"""
import streamlit as st
import matplotlib.pyplot as plt

from amp_finder.utils.sequence_utils import clean_sequence, validate_sequence
from amp_finder.core.analysis import analyze_sequence

# Page config
st.set_page_config(page_title="AMP Finder", page_icon="🧬", layout="wide")

# --- Sidebar logo and info ---
with st.sidebar:
    st.image("assets/logo.png", width=350)  # Logo on the sidebar (margin)
    st.markdown("---")
    st.header("About")
    st.markdown(
        "- Educational heuristic AMP-likeness predictor.\n"
        "- Add new descriptors under `amp_finder/descriptors/` — they'll be discovered automatically."
    )
    st.markdown("---")
    st.write("Example sequences")
    st.code("KWKLFKKIGAVLKVL")
    st.code("GIGKFLHSAKKFGKAFVGEIMNS")

# Inject custom CSS
with open("assets/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main title
st.title("🧬 AMP Finder — enhanced demo")
st.markdown(
    """
This educational app computes physicochemical descriptors of peptide sequences and shows
a simple heuristic AMP-likeness score. Features:
- automatic descriptor discovery (drop-in modules)
- result caching for quick repeated queries
- residue composition bar chart
"""
)

# Input sequence
seq_input = st.text_area(
    "Peptide sequence (one-letter codes):",
    value="KWKLFKKIGAVLKVL",
    height=140
)

# Create two columns: results on left, controls on right
col_left, col_right = st.columns([2, 1])

# Initialize session state for results
if "result" not in st.session_state:
    st.session_state.result = None
    st.session_state.seq = ""

# Analysis button
with col_right:
    if st.button("Analyze"):
        seq = clean_sequence(seq_input)
        valid, msg = validate_sequence(seq)
        if not valid:
            st.error(msg)
        else:
            st.session_state.seq = seq
            st.session_state.result = analyze_sequence(seq)

# Display results if available
if st.session_state.result:
    result = st.session_state.result
    descriptors = result["descriptors"]
    score = result["score"]

    with col_right:
        st.success(f"Analyzed sequence: **{st.session_state.seq}**")
        st.metric("Heuristic AMP-likeness", f"{score['amp_score']} / 100")
        st.write("**Key descriptors**")
        st.write(f"- Length: {descriptors.get('length', len(st.session_state.seq))}")
        st.write(f"- Molecular weight: {descriptors.get('molecular_weight', 'N/A')}")
        st.write(f"- GRAVY (hydropathy): {descriptors.get('gravy', 'N/A')}")
        st.write(f"- Instability index: {descriptors.get('instability_index', 'N/A')}")
        st.write(f"- pI: {descriptors.get('isoelectric_point', 'N/A')}")
        st.write(f"- Charge at pH7: {descriptors.get('charge_at_pH7', descriptors.get('charge', 'N/A'))}")
        st.write(f"- Hydrophobic fraction: {descriptors.get('hydrophobic_fraction', 'N/A')}")

    with col_left:
        st.subheader("Descriptor details")
        st.json(descriptors)

        # Residue composition chart
        aa_counts = descriptors.get("amino_acid_counts", {})
        if aa_counts:
            st.subheader("Residue composition")
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