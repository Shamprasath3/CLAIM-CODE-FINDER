import streamlit as st
import pandas as pd
import os

# ---------------- File Paths ----------------
NEW_VRF_FILE = "data/TOSHIBA_VRF.xlsx"
OLD_VRF_FILE = "data/TOSHIBA_MODEL.xlsx"

# ---------------- Utility Functions ----------------
def load_excel(file_path, uploaded_file=None):
    """Load Excel either from file path or uploaded file."""
    try:
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_excel(file_path)
        df.columns = df.columns.astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
        return None

def find_column(df, keywords):
    for col in df.columns:
        if any(k in col.lower() for k in keywords):
            return col
    return None

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Toshiba VRF SAP Finder", page_icon="⚙️", layout="wide")

# --------- Header ---------
st.markdown(
    """
    <div style="text-align:center; padding:15px; background:linear-gradient(90deg, #0f4c75, #3282b8);
                border-radius:12px; color:white; font-size:30px; font-weight:bold;">
        ⚙️ TOSHIBA VRF CLAIM CODE FINDER
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)

# ---------------- File Selection ----------------
st.markdown("### 📂 Select System Type")
option = st.radio("", ["CVRF", "TVRF"], horizontal=True)

# Pick file path
file_path = NEW_VRF_FILE if option == "CVRF" else NEW_VRF_FILE

# Check if file exists in repo
if os.path.exists(file_path):
    df = load_excel(file_path)
    st.success(f"✅ Loaded file: **{os.path.basename(file_path)}**")
else:
    st.warning(f"⚠️ {os.path.basename(file_path)} not found in repo. Please upload manually.")
    uploaded_file = st.file_uploader(f"Upload {option} Excel File", type=["xlsx"])
    df = load_excel(None, uploaded_file) if uploaded_file else None

# ---------------- Main Logic ----------------
if df is not None:
    model_col = find_column(df, ["model"])
    part_col = find_column(df, ["part description", "part", "discrim"])
    sap_col = find_column(df, ["sap", "code"])

    if model_col and part_col and sap_col:
        # --- Model Selection ---
        st.markdown("### 🏷️ Select Model")
        model_options = sorted(df[model_col].dropna().unique())
        selected_model = st.selectbox("Choose a model:", options=model_options)

        # --- Part Description Selection ---
        st.markdown("### 🔎 Select Part Description")
        filtered_parts = df[df[model_col] == selected_model][part_col].dropna().unique()
        part_options = sorted(filtered_parts)
        selected_part = st.selectbox(
            "Start typing part description:",
            options=part_options,
            index=None,
            placeholder="🔍 Type or select part..."
        )

        # --- SAP Code Lookup ---
        if selected_model and selected_part:
            st.markdown("### 📜 CLAIM CODE")
            filtered = df[(df[model_col] == selected_model) & (df[part_col] == selected_part)]
            if not filtered.empty:
                sap_codes = filtered[sap_col].dropna().unique()
                for code in sap_codes:
                    st.success(f"🔹 Code: **{code}**")
            else:
                st.warning("⚠️ No SAP Code found for this Model + Part Description.")
    else:
        st.error("⚠️ Could not find Model / Part Description / SAP Code columns in this file.")

