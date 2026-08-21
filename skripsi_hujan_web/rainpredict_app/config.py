# config.py
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
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    :root {
        --bg-primary: linear-gradient(135deg, #0a1e2f 0%, #1b3a5c 45%, #2a4f73 100%);
        --bg-secondary: #1a334a;
        --accent-primary: #4a8db7;
        --accent-secondary: #6baed6;
        --card-bg: rgba(20, 40, 60, 0.8);
        --text-primary: #e8f0f8;
        --text-muted: #b0c8dd;
    }

    .block-container {
        padding: 0 !important;
    }

    .stApp {
        background: var(--bg-primary);
        font-family: 'Poppins', sans-serif;
        color: var(--text-primary);
    }

    .hero-header {
        background: var(--bg-primary);
        padding: 1.5rem 2rem;
        border-radius: 0;
        color: white;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
        width: 100%;
    }

    .hero-header::after {
        content: 'cloudy_snowing';
        font-family: 'Material Symbols Rounded';
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 80px;
        color: rgba(255,255,255,0.05);
        pointer-events: none;
    }

    .stTabs {
        margin-top: -0.75rem;
        padding: 0 2rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.05);
        padding: 6px;
        border-radius: 14px;
        display: flex;
        gap: 6px;
        align-items: center;
        border-bottom: 1px solid rgba(255,255,255,0.08);
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
        background: rgba(255,255,255,0.06);
        color: var(--text-primary);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        color: white !important;
        padding: 9px 20px;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(74, 141, 183, 0.35);
        border: 1px solid rgba(255,255,255,0.15);
    }

    /* Sidebar – biru tua pekat agar kontras dengan konten */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1a2a 0%, #1a3550 100%) !important;
        border-right: 1px solid #2a4a6a !important;
    }

    [data-testid="stSidebar"] * {
        color: #d0e2f2 !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5 {
        color: #8fc4e8 !important;  /* biru langit soft */
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #d0e2f2 !important;
    }

    [data-testid="stSidebar"] a {
        color: #a8d0f0 !important;
    }
    [data-testid="stSidebar"] a:hover {
        color: #c5e2ff !important;
    }

    .sidebar-card {
        background: linear-gradient(135deg, #1a3550 0%, #2a4a6a 100%) !important;
        border-left: 5px solid #8fc4e8;
        color: #d0e2f2;
    }
    .sidebar-card p {
        color: #d0e2f2 !important;
    }
    .sidebar-card h4,
    .sidebar-card h5 {
        color: #8fc4e8 !important;
    }

    .material-icons-inline {
        color: #8fc4e8;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 12px;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(74, 141, 183, 0.3);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(74, 141, 183, 0.5);
    }

    .small-muted {
        color: var(--text-muted);
        font-size: 14px;
        font-weight: 300;
    }

    .site-footer {
        margin-top: 48px;
        padding: 18px;
        text-align: center;
        font-size: 0.75rem;
        color: var(--text-muted);
        border-top: 1px solid rgba(255,255,255,0.08);
    }

    .footer-note {
        margin-top: 4px;
        color: #8fc4e8;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

# Hanya satu definisi initialize_session_state (yang lengkap)
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
        st.session_state.dataset_info = '<span style="color:#FF6B6B;">Tidak ada dataset yang diunggah, mohon unggah terlebih dahulu pada sidebar.</span>'
    if 'narration' not in st.session_state:
        st.session_state.narration = ""
    os.makedirs("predictions", exist_ok=True)

# Mapping dan konstanta (tidak diubah)
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREDICTIONS_DIR = os.path.join(BASE_DIR, "predictions")
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")
os.makedirs(PREDICTIONS_DIR, exist_ok=True)
os.makedirs(ARTIFACTS_DIR, exist_ok=True)
PKL_NAME = os.path.join(ARTIFACTS_DIR, "implementasi_penelitian.pkl")

DATE_CANDIDATES = ["date","tanggal","time","waktu","tgl"]
RR_CANDIDATES = ["rr","curah","precip","precipitation","rain","rainfall"]
RANDOM_STATE = 42
