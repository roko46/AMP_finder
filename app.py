import base64
import os

import matplotlib.pyplot as plt
import streamlit as st

from amp_finder.core.analysis import analyze_sequence
from amp_finder.utils.sequence_utils import clean_sequence, validate_sequence

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="AMP Finder", page_icon="🧬", layout="wide")

# ------------------------------------------------------------
# LOAD CSS AND EMBED LOGO BACKGROUND
# ------------------------------------------------------------
css_path = os.path.join(os.path.dirname(__file__), "assets", "custom.css")
logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

base64_logo = ""
if os.path.exists(logo_path):
    with open(logo_path, "rb") as image_file:
        base64_logo = base64.b64encode(image_file.read()).decode("utf-8")

if os.path.exists(css_path):
    with open(css_path) as f:
        css = f.read()
        # Inject the base64 logo dynamically into CSS placeholder
        css = css.replace("BASE64_LOGO_PLACEHOLDER", base64_logo)
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
else:
    st.warning("⚠️ Could not find custom.css in assets/")

# ------------------------------------------------------------
# SIDEBAR CONTENT
# ------------------------------------------------------------
with st.sidebar:
    st.header("About")
    st.markdown("""
        **Educational heuristic AMP-likeness predictor**

        - Computes physicochemical descriptors.
        - Displays a heuristic AMP-likeness score.
        - You can add new descriptors under `amp_finder/descriptors/`
          — they load automatically.
        """)
    st.markdown("---")
    st.subheader("Example sequences")
    st.code("KWKLFKKIGAVLKVL")
    st.code("GIGKFLHSAKKFGKAFVGEIMNS")


# ------------------------------------------------------------
# MAIN PAGE
# ------------------------------------------------------------
st.title("🧬 AMP Finder — enhanced demo")

st.markdown("""
This educational app computes physicochemical descriptors of peptide sequences and
estimates a heuristic AMP-likeness score.

**Features:**
- Automatic descriptor discovery (drop-in modules)
- Caching for faster repeated queries
- Residue composition bar chart
- Full-screen translucent background logo
    """)

# ------------------------------------------------------------
# INPUT + ANALYSIS
# ------------------------------------------------------------
seq_input = st.text_area(
    "Peptide sequence (one-letter codes):", value="KWKLFKKIGAVLKVL", height=140
)

col_left, col_right = st.columns([2, 1])

with col_right:
    if st.button("Analyze"):
        seq = clean_sequence(seq_input)
        valid, msg = validate_sequence(seq)

        if not valid:
            st.error(msg)
        else:
            result = analyze_sequence(seq)
            descriptors = result.get("descriptors", {})
            score = result.get("score", {})

            st.success(f"Analyzed sequence: **{seq}**")
            st.metric("Heuristic AMP-likeness", f"{score.get('amp_score', 0)} / 100")

            st.markdown("### Key Descriptors")
            st.write(f"- **Length:** {descriptors.get('length', len(seq))}")
            st.write(
                f"- **Molecular weight:** {descriptors.get('molecular_weight', 'N/A')}"
            )
            st.write(f"- **GRAVY (hydropathy):** {descriptors.get('gravy', 'N/A')}")
            st.write(
                "- **Instability index:** "
                f"{descriptors.get('instability_index', 'N/A')}"
            )
            st.write(f"- **pI:** {descriptors.get('isoelectric_point', 'N/A')}")
            st.write(
                "- **Charge at pH7:** "
                f"{descriptors.get('charge_at_pH7', descriptors.get('charge', 'N/A'))}"
            )
            st.write(
                "- **Hydrophobic fraction:** "
                f"{descriptors.get('hydrophobic_fraction', 'N/A')}"
            )

            with col_left:
                st.subheader("Descriptor details")
                st.json(result["descriptors"])

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
