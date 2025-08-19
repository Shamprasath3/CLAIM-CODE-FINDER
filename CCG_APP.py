import streamlit as st
import pandas as pd
import os

# ---------------- File Paths ----------------
NEW_VRF_FILE = r"C:\Users\Sham prasath K\CARRIER_DATA\TOSHIBA_DATA\CALIM CODE GENERATOR\TOSHIBA VRF.xlsx"
OLD_VRF_FILE = r"C:\Users\Sham prasath K\CARRIER_DATA\TOSHIBA_DATA\CALIM CODE GENERATOR\TOSHIBA MODEL.xlsx"

# ---------------- Utility Functions ----------------
def load_excel(file_path):
    try:
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

# --------- Custom CSS for Premium Look ---------
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
    }
    .main-title {
        text-align: center;
        color: white;
        padding: 15px;
        background: linear-gradient(90deg, #0f4c75, #3282b8);
        border-radius: 12px;
        font-size: 30px !important;
    }
    .sub-section {
        font-size: 20px;
        margin-top: 25px;
        padding: 10px;
        background: #f1f1f1;
        border-radius: 10px;
        font-weight: bold;
        color: #222;
    }
    .result-box {
        background: #e8f5e9;
        padding: 15px;
        border-left: 6px solid #2e7d32;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 18px;
    }
    .warning-box {
        background: #fff3e0;
        padding: 15px;
        border-left: 6px solid #ef6c00;
        border-radius: 8px;
        margin-top: 10px;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# --------- Header ---------
st.markdown('<div class="main-title">⚙️ TOSHIBA VRF CLAIM CODE FINDER</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ---------------- File Selection ----------------
st.markdown('<div class="sub-section">📂 Select System Type</div>', unsafe_allow_html=True)
option = st.radio("", ["NEW VRF", "OLD VRF"], horizontal=True)
file_path = NEW_VRF_FILE if option == "NEW VRF" else OLD_VRF_FILE

df = load_excel(file_path)

if df is not None:
    st.success(f"✅ Loaded file: **{os.path.basename(file_path)}**")

    # Identify useful columns
    model_col = find_column(df, ["model"])
    part_col = find_column(df, ["part description", "part", "discrim"])
    sap_col = find_column(df, ["sap", "code"])

    if model_col and part_col and sap_col:
        # ---------------- Model Selection ----------------
        st.markdown('<div class="sub-section">🏷️ Select Model</div>', unsafe_allow_html=True)
        model_options = sorted(df[model_col].dropna().unique())
        selected_model = st.selectbox("Choose a model:", options=model_options)

        # ---------------- Part Description Selection ----------------
        st.markdown('<div class="sub-section">🔎 Select Part Description</div>', unsafe_allow_html=True)
        filtered_parts = df[df[model_col] == selected_model][part_col].dropna().unique()
        part_options = sorted(filtered_parts)
        selected_part = st.selectbox(
            "Start typing part description:",
            options=part_options,
            index=None,
            placeholder="🔍 Type or select part..."
        )

        # ---------------- SAP Code Lookup ----------------
        if selected_model and selected_part:
            st.markdown('<div class="sub-section">📜 CLAIM CODE</div>', unsafe_allow_html=True)
            filtered = df[(df[model_col] == selected_model) & (df[part_col] == selected_part)]

            if not filtered.empty:
                sap_codes = filtered[sap_col].dropna().unique()
                for code in sap_codes:
                    st.markdown(f'<div class="result-box">🔹 Code: <b>{code}</b></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-box">⚠️ No SAP Code found for this Model + Part Description.</div>', unsafe_allow_html=True)
    else:
        st.error("⚠️ Could not find Model / Part Description / SAP Code columns in this file.")
