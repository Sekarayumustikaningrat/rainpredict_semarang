# config.py
# jangan ubah apapun kecuali ganti warna — plus animasi header biar cute ✨
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
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20,400,0,0" rel="stylesheet">
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
        --drop-color-1: rgba(167, 139, 250, 0.25);
        --drop-color-2: rgba(125, 211, 252, 0.20);
        --drop-color-3: rgba(244, 114, 182, 0.15);
    }

    /* ============================================
       CONTAINER UTAMA — padding kiri/kanan untuk konten
       ============================================ */
    .block-container {
        padding: 0 2rem !important;   /* beri jarak kiri-kanan */
        padding-bottom: 4rem !important;
    }

    /* App Background & Font */
    .stApp {
        background: var(--bg-primary);
        font-family: 'Poppins', sans-serif;
        color: var(--text-primary);
    }

    /* ===============================
       HERO HEADER — full-width dengan margin negatif
       =============================== */
    .hero-header {
        background: var(--bg-primary);
        padding: 1.5rem 2rem;
        border-radius: 0;
        color: white;
        border-bottom: none;
        margin: 0 -2rem 1rem -2rem;   /* full-width melewati padding container */
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
        box-shadow: 0 4px 30px rgba(167, 139, 250, 0.08);
        animation: softGlow 4s ease-in-out infinite alternate;
        transition: box-shadow 0.3s ease;
        overflow: hidden;
        min-height: 120px;
        width: auto; /* biar mengikuti lebar container */
    }
    .hero-header:hover {
        box-shadow: 0 6px 40px rgba(167, 139, 250, 0.25);
    }

    @keyframes softGlow {
        0% { box-shadow: 0 4px 30px rgba(167, 139, 250, 0.08); }
        100% { box-shadow: 0 4px 50px rgba(167, 139, 250, 0.20); }
    }

    /* ===== LAYER 1: Efek hujan (tetesan air detail) ===== */
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        background-image:
            radial-gradient(ellipse at 5% 10%, var(--drop-color-1) 0%, transparent 6px),
            radial-gradient(ellipse at 15% 30%, var(--drop-color-2) 0%, transparent 4px),
            radial-gradient(ellipse at 25% 5%, var(--drop-color-3) 0%, transparent 5px),
            radial-gradient(ellipse at 35% 50%, var(--drop-color-1) 0%, transparent 7px),
            radial-gradient(ellipse at 45% 15%, var(--drop-color-2) 0%, transparent 4px),
            radial-gradient(ellipse at 55% 70%, var(--drop-color-3) 0%, transparent 5px),
            radial-gradient(ellipse at 65% 8%, var(--drop-color-1) 0%, transparent 6px),
            radial-gradient(ellipse at 75% 40%, var(--drop-color-2) 0%, transparent 4px),
            radial-gradient(ellipse at 85% 25%, var(--drop-color-3) 0%, transparent 7px),
            radial-gradient(ellipse at 95% 60%, var(--drop-color-1) 0%, transparent 5px),
            radial-gradient(ellipse at 8% 55%, var(--drop-color-2) 0%, transparent 4px),
            radial-gradient(ellipse at 18% 80%, var(--drop-color-3) 0%, transparent 3px),
            radial-gradient(ellipse at 28% 45%, var(--drop-color-1) 0%, transparent 4px),
            radial-gradient(ellipse at 38% 85%, var(--drop-color-2) 0%, transparent 3px),
            radial-gradient(ellipse at 48% 35%, var(--drop-color-3) 0%, transparent 4px),
            radial-gradient(ellipse at 58% 95%, var(--drop-color-1) 0%, transparent 4px),
            radial-gradient(ellipse at 68% 55%, var(--drop-color-2) 0%, transparent 3px),
            radial-gradient(ellipse at 78% 75%, var(--drop-color-3) 0%, transparent 4px),
            radial-gradient(ellipse at 88% 45%, var(--drop-color-1) 0%, transparent 3px),
            radial-gradient(ellipse at 98% 85%, var(--drop-color-2) 0%, transparent 4px),
            radial-gradient(ellipse at 3% 90%, var(--drop-color-3) 0%, transparent 2px),
            radial-gradient(ellipse at 12% 20%, var(--drop-color-1) 0%, transparent 3px),
            radial-gradient(ellipse at 22% 65%, var(--drop-color-2) 0%, transparent 2px),
            radial-gradient(ellipse at 32% 40%, var(--drop-color-3) 0%, transparent 3px),
            radial-gradient(ellipse at 42% 10%, var(--drop-color-1) 0%, transparent 2px),
            radial-gradient(ellipse at 52% 50%, var(--drop-color-2) 0%, transparent 3px),
            radial-gradient(ellipse at 62% 30%, var(--drop-color-3) 0%, transparent 2px),
            radial-gradient(ellipse at 72% 90%, var(--drop-color-1) 0%, transparent 3px),
            radial-gradient(ellipse at 82% 70%, var(--drop-color-2) 0%, transparent 2px),
            radial-gradient(ellipse at 92% 15%, var(--drop-color-3) 0%, transparent 3px);
        background-size: 100% 100%;
        background-repeat: no-repeat;
        animation: rainDrops 2.8s linear infinite;
        opacity: 0.9;
    }

    @keyframes rainDrops {
        0% { background-position: 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0,
                             0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0,
                             0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0; }
        100% { background-position: 0 40px, 0 35px, 0 45px, 0 30px, 0 40px, 0 35px,
                                   0 42px, 0 38px, 0 30px, 0 45px,
                                   0 40px, 0 35px, 0 42px, 0 38px, 0 45px,
                                   0 30px, 0 40px, 0 35px, 0 42px, 0 38px,
                                   0 45px, 0 30px, 0 40px, 0 35px, 0 42px,
                                   0 38px, 0 45px, 0 30px, 0 40px, 0 35px; }
    }

    /* ===== LAYER 2: Daun/bunga berjatuhan ===== */
    .hero-header::after {
        content: '🌸 🍃 🌸 🍃 🌸 🍃 🌸 🍃 🌸 🍃';
        position: absolute;
        top: -10%;
        left: 0;
        width: 100%;
        height: 120%;
        pointer-events: none;
        z-index: 1;
        font-size: 18px;
        letter-spacing: 80px;
        text-align: center;
        opacity: 0.25;
        animation: floatingLeaves 12s linear infinite;
        white-space: nowrap;
        filter: drop-shadow(0 0 4px rgba(244, 114, 182, 0.15));
    }

    @keyframes floatingLeaves {
        0% { transform: translateY(0) translateX(0) rotate(0deg); opacity: 0.15; }
        10% { opacity: 0.30; }
        50% { transform: translateY(60px) translateX(-30px) rotate(15deg); opacity: 0.35; }
        90% { opacity: 0.20; }
        100% { transform: translateY(120px) translateX(30px) rotate(-10deg); opacity: 0.10; }
    }

    /* ===== LAYER 3: Elemen tambahan (glow) ===== */
    .hero-header .rain-glow {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 60%;
        height: 80%;
        background: radial-gradient(ellipse at center, rgba(167, 139, 250, 0.04) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
        animation: glowPulse 4s ease-in-out infinite alternate;
    }

    @keyframes glowPulse {
        0% { opacity: 0.3; transform: translate(-50%, -50%) scale(0.9); }
        100% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); }
    }

    /* ===== Konten header (di atas efek) ===== */
    .hero-content {
        position: relative;
        z-index: 2;
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        flex-wrap: wrap;
        gap: 16px;
    }

    .hero-text {
        display: flex;
        flex-direction: column;
        gap: 2px;
        flex: 1;
        min-width: 200px;
    }

    .hero-visual {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-left: auto;
        flex-shrink: 0;
    }

    .hero-icon {
        font-size: 42px;
        color: var(--accent-primary);
        animation: floatIcon 3s ease-in-out infinite;
        filter: drop-shadow(0 0 16px rgba(167, 139, 250, 0.3));
        flex-shrink: 0;
        margin-right: 8px;
        display: inline-block;
    }

    @keyframes floatIcon {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-6px) rotate(2deg); }
    }

    .header-title {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #F1F0F7, #C4B0F8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gentleWobble 3s ease-in-out infinite;
        display: inline-block;
        margin: 0;
        line-height: 1.2;
    }
    @keyframes gentleWobble {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(0.8deg); }
        75% { transform: rotate(-0.8deg); }
    }

    .header-subtitle {
        font-size: 0.95rem;
        font-weight: 400;
        background: linear-gradient(135deg, #C4B0F8, #7DD3FC, #F472B6);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 5s ease-in-out infinite;
        margin: 0;
        position: relative;
        display: inline-block;
        padding-bottom: 4px;
    }
    .header-subtitle::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent-secondary), var(--accent-warm), transparent);
        background-size: 200% 100%;
        animation: waveFlow 2.5s linear infinite;
        border-radius: 2px;
        -webkit-text-fill-color: initial;
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

    .hero-visual .material-symbols-rounded {
        font-size: 32px;
        transition: transform 0.3s;
    }

    .hero-visual .cloud-big {
        color: rgba(167, 139, 250, 0.30);
        font-size: 52px;
        animation: floatCloudBig 5s ease-in-out infinite;
        filter: drop-shadow(0 0 20px rgba(167, 139, 250, 0.10));
    }
    @keyframes floatCloudBig {
        0%, 100% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-6px) scale(1.04); }
    }

    .hero-visual .thunder-icon {
        color: rgba(244, 114, 182, 0.5);
        animation: thunderPulse 3s ease-in-out infinite;
        filter: drop-shadow(0 0 12px rgba(244, 114, 182, 0.15));
        position: relative;
    }
    .hero-visual .thunder-icon::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
        opacity: 0;
        animation: lightningFlash 4s ease-in-out infinite;
        pointer-events: none;
        border-radius: 50%;
    }
    @keyframes thunderPulse {
        0%, 90%, 100% { transform: scale(1); opacity: 0.5; }
        95% { transform: scale(1.15); opacity: 1; }
    }
    @keyframes lightningFlash {
        0%, 80%, 100% { opacity: 0; }
        85% { opacity: 1; }
        90% { opacity: 0; }
    }

    .hero-visual .rain-drop-icon {
        color: rgba(125, 211, 252, 0.35);
        font-size: 20px;
        animation: rainDropIcon 1.8s linear infinite;
    }
    .hero-visual .rain-drop-icon:nth-child(2) { animation-delay: 0.6s; }
    .hero-visual .rain-drop-icon:nth-child(3) { animation-delay: 1.2s; }

    @keyframes rainDropIcon {
        0% { transform: translateY(-16px) scale(0.5); opacity: 0; }
        40% { opacity: 1; }
        100% { transform: translateY(16px) scale(1); opacity: 0; }
    }

    /* ===============================
       NAVBAR / TABS — sticky hanya tab-list, full-width
       =============================== */
    .stTabs {
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
        border-bottom: none !important;
        box-shadow: none !important;
        overflow: visible !important;
    }

    /* Tab list — sticky dengan margin negatif untuk full-width */
    .stTabs [data-baseweb="tab-list"] {
        position: -webkit-sticky !important;
        position: sticky !important;
        top: 0 !important;
        z-index: 999 !important;
        background: rgba(26, 20, 47, 0.80) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        padding: 6px 2rem !important;
        border-radius: 0 !important;
        display: flex !important;
        gap: 6px !important;
        align-items: center !important;
        border-bottom: 1px solid var(--border-soft) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
        width: auto !important;
        margin: 0 -2rem !important;   /* full-width melewati padding */
        transition: box-shadow 0.3s;
    }
    .stTabs [data-baseweb="tab-list"]:hover {
        box-shadow: 0 4px 30px rgba(167, 139, 250, 0.15) !important;
    }

    /* Tab buttons */
    .stTabs [data-baseweb="tab"] {
        padding: 8px 18px !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        color: var(--text-muted) !important;
        background: transparent !important;
        transition: all 0.2s ease !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(167, 139, 250, 0.10) !important;
        color: var(--text-primary) !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--accent-primary), #8B6FE8) !important;
        color: white !important;
        padding: 9px 20px !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 20px rgba(167, 139, 250, 0.40) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
    }

    /* ===============================
       SIDEBAR
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
       SIDEBAR CARD
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
       ICON
       =============================== */
    .material-icons-inline {
        color: var(--accent-primary);
    }

    /* Buttons */
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

    .small-muted {
        color: var(--text-muted);
        font-size: 14px;
        font-weight: 300;
    }

    /* ===============================
       FOOTER — rapi dengan padding dan margin
       =============================== */
    .site-footer {
        margin: 48px -2rem 0 -2rem;   /* full-width, melewati padding */
        padding: 1.5rem 2rem;
        text-align: center;
        font-size: 0.8rem;
        color: var(--text-muted) !important;
        border-top: 1px solid var(--border-soft);
        background: rgba(26, 20, 47, 0.3);
        backdrop-filter: blur(4px);
        clear: both;
    }

    .footer-note {
        margin-top: 6px;
        color: #7DD3FC !important;
        font-weight: 500;
        letter-spacing: 0.5px;
    }

    /* ===============================
       ELEMEN LAINNYA
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
