"File ini berisi komponen UI seperti sidebar, tabs, dan elemen interaktif (misalnya form input, grafik, dll). Memisahkan tampilan dari logika sehingga memudahkan utnuk menambahkan fitur UI tanpa mengganggu kode lain"

import streamlit as st
from config import set_page_config, local_css, initialize_session_state, MODEL_MAPPING, ...
from loaders import load_all_for_mode
from ui_components import sidebar, tabs

# Inisialisasi halaman dan session state
set_page_config()
local_css()
initialize_session_state()

# Load resources berdasarkan mode
if st.session_state.last_loaded_mode != st.session_state.mode:
    st.session_state.models, st.session_state.metrics, st.session_state.feature_names, st.session_state.preprocessor = load_all_for_mode(st.session_state.mode)
    st.session_state.last_loaded_mode = st.session_state.mode

# Header
# Link icon material
st.markdown(
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20,400,0,0" />',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="hero-header">
        <div class="hero-content">
            <span class="material-symbols-rounded hero-icon">cloud</span>
            <h1 class="header-title">RainPredict Semarang</h1>
            <p class="header-subtitle">
                Sistem Prediksi Curah Hujan Berbasis Data Historis Deret Waktu
            </p>
        </div>
        <span class="material-symbols-rounded" style="font-size: 40px; opacity: 0.3;">
            Thunderstorm
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# Render sidebar dan tabs
sidebar()
tabs()


# Footer
st.markdown('''
<div class="site-footer">
    <div class="footer-left">
        <span>© 2026 RainPredict Semarang</span>
        <span class="footer-divider">·</span>
        <span>Implementasi Skripsi & Media Edukasi</span>
    </div>
    <div class="footer-right">
        <span class="footer-note">Stacking Ensemble · XGBoostRegressor · SHAP Explainability</span>
    </div>
</div>
''', unsafe_allow_html=True)
