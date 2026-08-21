"""
File ini berisi konfigurasi halaman misal: set_page_config, CSS untuk styling (menampilkan yang menarik dan konsisten), mappings (MODEL_MAPPING, dll), dan pengaturan global lainnya. Ini memisahkan pengaturan dari logika utama agar mudah diubah (misalnya, jika ingin mengganti tema warna).
"""

import streamlit as st
import os

def set_page_config():
    st.set_page_config(
        page_title="RainPredict Semarang",
        page_icon="🌧️",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def local_css():
    # 1️⃣ Import font & icon Google di luar <style>
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    """, unsafe_allow_html=True)

    # 2️⃣ CSS styling lokal — fresh, cute, soft-dark theme + animasi header
    st.markdown("""
    <style>
    :root {
        --bg-primary: linear-gradient(135deg, #1A142F 0%, #2D1B4E 45%, #3D2A5C 100%);
        --bg-secondary: #2D1B4E;
        --accent-primary: #A78BFA;
        --accent-secondary: #7DD3FC;
        --accent-warm: #F472B6;
        --accent-glow: rgba(167, 139, 250, 0.35);
        --card-bg: rgba(45, 27, 78, 0.75);
        --text-primary: #F1F0F7;
        --text-muted: #B8B0D0;
        --border-soft: rgba(167, 139, 250, 0.15);
    }

    /* FIX: Menghilangkan space kosong di atas header */
    .block-container {
        padding: 0 !important;
    }

    /* App Background & Font */
    .stApp {
        background: var(--bg-primary);
        font-family: 'Poppins', sans-serif;
        color: var(--text-primary);
    }

    /* ===============================
       HERO HEADER — dengan animasi hujan & petir
       =============================== */
    .hero-header {
        background: var(--bg-primary);
        padding: 1.5rem 2rem;
        border-radius: 0;
        color: white;
        border-bottom: 1px solid var(--border-soft);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
        width: 100%;
        box-shadow: 0 4px 30px rgba(167, 139, 250, 0.08);
        animation: softGlow 4s ease-in-out infinite alternate;
        transition: box-shadow 0.3s ease;
        overflow: hidden;  /* agar efek hujan tidak keluar */
    }
    .hero-header:hover {
        box-shadow: 0 6px 40px rgba(167, 139, 250, 0.25);
    }

    /* Animasi glow header */
    @keyframes softGlow {
        0% { box-shadow: 0 4px 30px rgba(167, 139, 250, 0.08); }
        100% { box-shadow: 0 4px 50px rgba(167, 139, 250, 0.20); }
    }

    /* ----- Efek hujan lembut (background bergerak) ----- */
    .hero-header::before {
        content: '';
        position: absolute;
        top: -10%;
        left: -10%;
        width: 120%;
        height: 120%;
        pointer-events: none;
        background-image: 
            /* Garis-garis miring sebagai hujan */
            repeating-linear-gradient(
                45deg,
                transparent,
                transparent 8px,
                rgba(167, 139, 250, 0.03) 8px,
                rgba(167, 139, 250, 0.03) 9px
            ),
            repeating-linear-gradient(
                -45deg,
                transparent,
                transparent 12px,
                rgba(125, 211, 252, 0.02) 12px,
                rgba(125, 211, 252, 0.02) 13px
            );
        background-size: 30px 30px, 40px 40px;
        animation: rainFall 3s linear infinite;
        opacity: 0.6;
        z-index: 0;
    }

    @keyframes rainFall {
        0% { background-position: 0 0, 0 0; }
        100% { background-position: 30px 60px, 40px 80px; }
    }

    /* ----- Cloud icon melayang (tetap) ----- */
    .hero-header::after {
        content: 'cloudy_snowing';
        font-family: 'Material Symbols Rounded';
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 80px;
        color: rgba(167, 139, 250, 0.06);
        pointer-events: none;
        animation: floatCloud 6s ease-in-out infinite;
        z-index: 1;
    }

    @keyframes floatCloud {
        0% { transform: translateY(-50%) scale(1); }
        50% { transform: translateY(-60%) scale(1.05); }
        100% { transform: translateY(-50%) scale(1); }
    }

    /* ----- Konten header (di atas efek) ----- */
    .hero-content {
        position: relative;
        z-index: 2;
        display: flex;
        align-items: center;
        gap: 14px;
        flex-wrap: wrap;
    }

    /* Icon awan di kiri */
    .hero-icon {
        font-size: 48px;
        color: var(--accent-primary);
        animation: floatIcon 3s ease-in-out infinite;
        filter: drop-shadow(0 0 12px rgba(167, 139, 250, 0.3));
    }

    @keyframes floatIcon {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-6px) rotate(2deg); }
    }

    /* Judul utama */
    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #F1F0F7, #C4B0F8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gentleWobble 3s ease-in-out infinite;
        display: inline-block;
        margin: 0;
    }
    @keyframes gentleWobble {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(1deg); }
        75% { transform: rotate(-1deg); }
    }

    /* Subtitle dengan gradasi bergerak dan garis air */
    .header-subtitle {
        font-size: 1rem;
        font-weight: 400;
        background: linear-gradient(135deg, #C4B0F8, #7DD3FC, #F472B6);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 5s ease-in-out infinite;
        margin: 0 0 0 8px;
        position: relative;
        display: inline-block;
    }
    /* Garis bawah bergelombang (air mengalir) */
    .header-subtitle::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--accent-secondary), var(--accent-warm), transparent);
        background-size: 200% 100%;
        animation: waveFlow 2.5s linear infinite;
        border-radius: 2px;
        -webkit-text-fill-color: initial; /* reset untuk pseudo */
    }

    @keyframes waveFlow {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ----- Ikon petir di kanan (Thunderstorm) ----- */
    .hero-header > .material-symbols-rounded:last-child {
        position: relative;
        z-index: 2;
        font-size: 40px !important;
        opacity: 0.4 !important;
        animation: thunderPulse 3s ease-in-out infinite;
        transition: opacity 0.3s;
        filter: drop-shadow(0 0 8px rgba(244, 114, 182, 0.2));
    }
    /* Kilatan lembut (flash) menggunakan pseudo pada ikon */
    .hero-header > .material-symbols-rounded:last-child::after {
        content: '';
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
        border-radius: 50%;
        opacity: 0;
        animation: lightningFlash 4s ease-in-out infinite;
        pointer-events: none;
    }

    @keyframes thunderPulse {
        0%, 90%, 100% { transform: scale(1); opacity: 0.4; }
        95% { transform: scale(1.1); opacity: 0.8; }
    }
    @keyframes lightningFlash {
        0%, 80%, 100% { opacity: 0; }
        85% { opacity: 0.6; }
        90% { opacity: 0; }
    }

    /* ===============================
       NAVBAR / TABS (DIRAPIKAN)
       =============================== */

    .stTabs {
        margin-top: -0.75rem;
        padding: 0 2rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(167, 139, 250, 0.06);
        padding: 6px;
        border-radius: 14px;
        display: flex;
        gap: 6px;
        align-items: center;
        border-bottom: 1px solid var(--border-soft);
    }

    .stTabs [data-baseweb="tab"] {
        padding: 8px 18px;
        border-radius: 12px;
        font-weight: 500;
        color: var(--text-muted);
        background: transparent;
        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(167, 139, 250, 0.10);
        color: var(--text-primary);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--accent-primary), #8B6FE8);
        color: white !important;
        padding: 9px 20px;
        border-radius: 14px;
        box-shadow: 0 4px 20px rgba(167, 139, 250, 0.40);
        border: 1px solid rgba(255, 255, 255, 0.12);
    }

    /* ===============================
       SIDEBAR – kontras dengan nuansa ungu kebiruan
       =============================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E2A4A 0%, #3A4B7A 100%) !important;
        border-right: 1px solid rgba(167, 139, 250, 0.30) !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.2);
    }

    [data-testid="stSidebar"] * {
        color: #F1F0F7 !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5 {
        color: #C4B0F8 !important;
        font-weight: 600;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #D4CCE8 !important;
    }

    [data-testid="stSidebar"] a {
        color: #7DD3FC !important;
    }
    [data-testid="stSidebar"] a:hover {
        color: #BAE6FD !important;
    }

    /* ===============================
       SIDEBAR CARD — soft glass
       =============================== */
    .sidebar-card {
        background: linear-gradient(135deg, rgba(167, 139, 250, 0.12) 0%, rgba(125, 211, 252, 0.08) 100%) !important;
        border-left: 4px solid var(--accent-primary);
        border-radius: 12px;
        color: #F1F0F7;
        backdrop-filter: blur(4px);
    }
    .sidebar-card p {
        color: #D4CCE8 !important;
    }
    .sidebar-card h4, .sidebar-card h5 {
        color: #C4B0F8 !important;
    }

    /* ===============================
       ICON — lavender & sky
       =============================== */
    .material-icons-inline {
        color: var(--accent-primary);
    }

    /* Buttons — soft gradient lavender → pink */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-warm));
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 12px;
        font-weight: 500;
        box-shadow: 0 4px 20px rgba(167, 139, 250, 0.30);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 28px rgba(167, 139, 250, 0.50);
    }

    /* Small text muted */
    .small-muted {
        color: var(--text-muted);
        font-size: 14px;
        font-weight: 300;
    }

    /* ===============================
       FOOTER — soft lavender line
       =============================== */
    .site-footer {
        margin-top: 48px;
        padding: 18px;
        text-align: center;
        font-size: 0.75rem;
        color: var(--text-muted);
        border-top: 1px solid var(--border-soft);
    }

    .footer-note {
        margin-top: 4px;
        color: #C4B0F8;
        font-weight: 500;
        letter-spacing: 0.3px;
    }

    /* ===============================
       EXTRA — selectbox, slider, dll.
       =============================== */
    .stSelectbox [data-baseweb="select"] {
        background: rgba(45, 27, 78, 0.5);
        border-radius: 10px;
        border: 1px solid var(--border-soft);
    }

    .stSlider [data-baseweb="slider"] {
        accent-color: var(--accent-primary);
    }

    [data-testid="metric-container"] {
        background: rgba(45, 27, 78, 0.5);
        border-radius: 14px;
        padding: 12px 16px;
        border: 1px solid var(--border-soft);
        backdrop-filter: blur(4px);
    }

    .stDataFrame {
        background: rgba(45, 27, 78, 0.4);
        border-radius: 14px;
        border: 1px solid var(--border-soft);
    }

    .streamlit-expanderHeader {
        background: rgba(45, 27, 78, 0.4);
        border-radius: 12px;
        border: 1px solid var(--border-soft);
        color: var(--text-primary);
    }
    .streamlit-expanderHeader:hover {
        background: rgba(167, 139, 250, 0.08);
    }

    .stFileUploader {
        background: rgba(45, 27, 78, 0.4);
        border-radius: 14px;
        border: 2px dashed var(--border-soft);
        padding: 8px;
    }
    .stFileUploader:hover {
        border-color: var(--accent-primary);
    }

    .stAlert {
        background: rgba(45, 27, 78, 0.5) !important;
        border-radius: 12px !important;
        border-left: 4px solid var(--accent-primary) !important;
        color: var(--text-primary) !important;
    }
    .stAlert svg {
        fill: var(--accent-primary) !important;
    }

    .stCheckbox label {
        color: var(--text-primary);
    }
    .stCheckbox input:checked + div {
        background: var(--accent-primary) !important;
        border-color: var(--accent-primary) !important;
    }

    .stRadio label {
        color: var(--text-primary);
    }
    .stRadio input:checked + div {
        accent-color: var(--accent-primary);
    }

    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    if 'mode' not in st.session_state:
        st.session_state.mode = "Harian"
    # Tambahkan inisialisasi state lainnya jika diperlukan

# Mappings
MODEL_MAPPING = {
    "Harian": {
        "Iterasi 1": "stacking_model_harian_iter1.pkl",
        "Iterasi 2": "stacking_model_harian_iter2.pkl",
        "Iterasi 3": "stacking_model_harian_iter3.pkl"
    },
    "Bulanan": {
        "Iterasi 1": "stacking_model_bulanan_iter1.pkl",
        "Iterasi 2": "stacking_model_bulanan_iter2.pkl",
        "Iterasi 3": "stacking_model_bulanan_iter3.pkl"
    }
}
FEATURE_NAMES_MAP = {
    "Harian": "model_feature_names_harian.pkl",
    "Bulanan": "model_feature_names_bulanan.pkl"
}
SHAP_PATH_MAP = {
    "Harian": {
        "Iterasi 1": "shap_explainer_harian_iter1.pkl",
        "Iterasi 2": "shap_explainer_harian_iter2.pkl",
        "Iterasi 3": "shap_explainer_harian_iter3.pkl"
    },
    "Bulanan": {
        "Iterasi 1": "shap_explainer_bulanan_iter1.pkl",
        "Iterasi 2": "shap_explainer_bulanan_iter2.pkl",
        "Iterasi 3": "shap_explainer_bulanan_iter3.pkl"
    }
}
EVAL_PATH_MAP = {
    "Harian": {
        "Iterasi 1": "eval_harian_iter1.pkl",
        "Iterasi 2": "eval_harian_iter2.pkl",
        "Iterasi 3": "eval_harian_iter3.pkl",
    },
    "Bulanan": {
        "Iterasi 1": "eval_bulanan_iter1.pkl",
        "Iterasi 2": "eval_bulanan_iter2.pkl",
        "Iterasi 3": "eval_bulanan_iter3.pkl",
    }
}

DATA_DEFAULT = "data iklim harian - Semarang (2020-2023).xlsx"
PREPROCESSOR_PATH = "preprocessor.pkl"

def initialize_session_state():
    if 'mode' not in st.session_state:
        st.session_state.mode = "Harian"
    if 'models' not in st.session_state:
        st.session_state.models = {}
    if 'metrics' not in st.session_state:
        st.session_state.metrics = {}
    if 'feature_names' not in st.session_state:
        st.session_state.feature_names = None
    if 'preprocessor' not in st.session_state:
        st.session_state.preprocessor = None
    if 'last_loaded_mode' not in st.session_state:
        st.session_state.last_loaded_mode = None
    if 'detected_mode' not in st.session_state:
        st.session_state.detected_mode = None
    if 'df_raw' not in st.session_state:
        st.session_state.df_raw = None
    if 'df_idx' not in st.session_state:
        st.session_state.df_idx = None
    if 'total_rain' not in st.session_state:
        st.session_state.total_rain = 0.0
    if 'avg_rain' not in st.session_state:
        st.session_state.avg_rain = 0.0
    if 'dataset_info' not in st.session_state:
        st.session_state.dataset_info = '<span style="color:#F472B6;">Tidak ada dataset yang diunggah, mohon unggah terlebih dahulu pada sidebar.</span>'
    if 'narration' not in st.session_state:
        st.session_state.narration = ""
    os.makedirs("predictions", exist_ok=True)

# config.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREDICTIONS_DIR = os.path.join(BASE_DIR, "predictions")
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")
os.makedirs(PREDICTIONS_DIR, exist_ok=True)
os.makedirs(ARTIFACTS_DIR, exist_ok=True)
PKL_NAME = os.path.join(ARTIFACTS_DIR, "implementasi_penelitian.pkl")


# Default names that are commonly present. The loader will try to pick a date column.
DATE_CANDIDATES = ["date","tanggal","time","waktu","tgl"]
RR_CANDIDATES = ["rr","curah","precip","precipitation","rain","rainfall"]


# Training defaults
RANDOM_STATE = 42
