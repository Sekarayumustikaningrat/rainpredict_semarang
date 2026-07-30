"""
File ini berisi semua fungsi loading (models, data, metrics, SHAP, processor).
Memisahkan logika pemuatan data agar kode utama lebih bersih dan efisien,
dengan caching untuk performa yang lebih baik.
"""

import os
import pickle
import importlib
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import OneHotEncoder

# =====================================================
# 🔹 FIXED ROBUST PATCH (No NameError, No Recursion)
# =====================================================

# 1. Patch np.isnan agar aman untuk data campuran (string/object)
if not hasattr(np, '_is_patched_v4'):
    _orig_isnan = np.isnan
    def _safe_isnan(x):
        try:
            return _orig_isnan(x)
        except (TypeError, ValueError):
            return pd.isna(x)
    np.isnan = _safe_isnan
    np._is_patched_v4 = True

# 2. Patch OneHotEncoder._transform dengan pengaman rekursi & import internal
if not hasattr(OneHotEncoder, '_is_patched_final_v4'):
    try:
        # Import internal secara langsung di dalam blok untuk mencegah NameError
        import sklearn.preprocessing._encoders as _encoders_module
        _REAL_FUNC = _encoders_module.OneHotEncoder._transform
        
        def _robust_patched_transform(self, X, *args, **kwargs):
            try:
                # Gunakan fungsi asli yang kita simpan di _REAL_FUNC
                return _REAL_FUNC(self, X, *args, **kwargs)
            except (ValueError, TypeError) as e:
                msg = str(e).lower()
                if 'invalid literal' in msg or 'could not convert' in msg:
                    # Konversi ke object jika tipe data bermasalah (misal string masuk ke kolom float)
                    X_fix = X.astype(object) if hasattr(X, 'astype') else pd.DataFrame(X).astype(object)
                    return _REAL_FUNC(self, X_fix, *args, **kwargs)
                raise e

        # Terapkan patch
        OneHotEncoder._transform = _robust_patched_transform
        OneHotEncoder._is_patched_final_v4 = True
        
    except Exception as patch_error:
        # Jika gagal patching, biarkan aplikasi berjalan dengan fungsi asli
        st.warning(f"Sistem patching otomatis dinonaktifkan: {patch_error}")

from config import (
    MODEL_MAPPING,
    FEATURE_NAMES_MAP,
    EVAL_PATH_MAP,
    DATA_DEFAULT,
    PREPROCESSOR_PATH,
    DATE_CANDIDATES,
    RR_CANDIDATES,
)

# =====================================================
# 🔹 ROBUST PICKLE LOADER
# =====================================================
@st.cache_resource
def load_pickle_robust(path):
    if not os.path.exists(path):
        return None, f"Missing: {path}"

    try:
        with open(path, "rb") as f:
            obj = pickle.load(f)
        return obj, f"Loaded pickle: {path}"

    except Exception:
        try:
            with open(path, "rb") as f:
                class CompatUnpickler(pickle.Unpickler):
                    def find_class(self, module, name):
                        if module.startswith("numpy._core"):
                            module = module.replace("numpy._core", "numpy.core")
                        return super().find_class(module, name)

                obj = CompatUnpickler(f).load()
            return obj, f"Loaded with CompatUnpickler: {path}"

        except Exception:
            if importlib.util.find_spec("joblib"):
                try:
                    import joblib
                    return joblib.load(path), f"Loaded with joblib: {path}"
                except Exception:
                    pass

            if importlib.util.find_spec("dill"):
                try:
                    import dill
                    with open(path, "rb") as f:
                        return dill.load(f), f"Loaded with dill: {path}"
                except Exception:
                    pass

    return None, f"Failed load all fallback for {path}"


# =====================================================
# 🔹 MODEL LOADER
# =====================================================
@st.cache_resource
def load_model_safe(path):
    obj, _ = load_pickle_robust(path)
    return obj if (obj is not None and hasattr(obj, "predict")) else None


# =====================================================
# 🔹 EVALUATION METRICS
# =====================================================
@st.cache_data
def load_eval_metrics(mode):
    metrics = {}

    for name, path in EVAL_PATH_MAP[mode].items():
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    df_eval = pickle.load(f)

                if isinstance(df_eval, pd.DataFrame):
                    row = df_eval.loc['Stacking'] if 'Stacking' in df_eval.index else df_eval.iloc[0]
                    metrics[name] = {
                        "R2": float(row.get('R2', np.nan)),
                        "RMSE": float(row.get('RMSE', np.nan)),
                        "MAE": float(row.get('MAE', np.nan)),
                    }
                else:
                    metrics[name] = {"R2": np.nan, "RMSE": np.nan, "MAE": np.nan}

            except Exception:
                metrics[name] = {"R2": np.nan, "RMSE": np.nan, "MAE": np.nan}
        else:
            metrics[name] = {"R2": np.nan, "RMSE": np.nan, "MAE": np.nan}

    return metrics


# =====================================================
# 🔹 PREPROCESSOR & FEATURE NAMES
# =====================================================
@st.cache_data
def load_preprocessor(path=PREPROCESSOR_PATH):
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                obj = pickle.load(f)
            if hasattr(obj, "transform"):
                # Modify OneHotEncoder to handle unknown categories
                if hasattr(obj, 'named_transformers_'):
                    for name, trans in obj.named_transformers_.items():
                        if hasattr(trans, 'handle_unknown'):
                            trans.handle_unknown = 'ignore'
                return obj
        except Exception:
            return None
    return None


@st.cache_data
def load_feature_names(path):
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                obj = pickle.load(f)
            return list(obj) if isinstance(obj, (list, tuple)) else None
        except Exception:
            return None
    return None


# =====================================================
# 🔹 DATASET LOADER (UPLOAD / DEFAULT)
# =====================================================
@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith((".xls", ".xlsx")):
                return pd.read_excel(uploaded_file)
            return pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error membaca file upload: {e}")
            return None

    if os.path.exists(DATA_DEFAULT):
        try:
            return pd.read_excel(DATA_DEFAULT)
        except Exception as e:
            st.error(f"Gagal baca data default: {e}")
            return None

    return None


# =====================================================
# 🔹 LOAD ALL PER MODE
# =====================================================
def load_all_for_mode(mode):
    models = {
        name: load_model_safe(path)
        for name, path in MODEL_MAPPING[mode].items()
    }
    metrics = load_eval_metrics(mode)
    feat_names = load_feature_names(FEATURE_NAMES_MAP[mode])
    preproc = load_preprocessor()
    return models, metrics, feat_names, preproc


# =====================================================
# 🔹 GENERIC LOADER (ANY FORMAT)
# =====================================================
def load_any(path):
    if path is None or not os.path.exists(path):
        return None

    try:
        import joblib
        return joblib.load(path)
    except Exception:
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except Exception:
            return None


# =====================================================
# 🔹 BEST ITERATION FINDER
# =====================================================
def compute_best_iteration_for_mode(mode):
    best_iter, best_r2 = None, -np.inf

    for it_name, path in EVAL_PATH_MAP.get(mode, {}).items():
        try:
            if not os.path.exists(path):
                continue

            obj = load_any(path)
            r2 = None

            if isinstance(obj, pd.DataFrame):
                if 'Model' in obj.columns and 'R2 Test' in obj.columns:
                    r2 = float(
                        obj.loc[obj['Model'] == 'Stacking', 'R2 Test'].values[0]
                        if 'Stacking' in obj['Model'].values
                        else obj.iloc[-1]['R2 Test']
                    )
                elif 'R2' in obj.columns:
                    r2 = float(obj.iloc[-1]['R2'])

            elif isinstance(obj, dict):
                r2 = float(obj.get('R2', np.nan))

            if r2 is not None and not np.isnan(r2) and r2 > best_r2:
                best_r2, best_iter = r2, it_name

        except Exception:
            continue

    return best_iter, (best_r2 if best_iter else np.nan)


# =====================================================
# 🔹 UPLOAD HANDLER
# =====================================================
def load_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return None

    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif name.endswith((".xls", ".xlsx")):
        return pd.read_excel(uploaded_file)

    uploaded_file.seek(0)
    return pd.read_csv(uploaded_file)


# =====================================================
# 🔹 DATE & RR DETECTOR
# =====================================================
def detect_date_and_rr(df):
    cols = list(df.columns)
    date_col, rr_col = None, None

    for cand in DATE_CANDIDATES:
        for c in cols:
            if cand in c.lower():
                date_col = c
                break
        if date_col:
            break

    if date_col is None:
        date_col = cols[0]

    for cand in RR_CANDIDATES:
        for c in cols:
            if cand in c.lower():
                rr_col = c
                break
        if rr_col:
            break

    if rr_col is None and len(cols) > 1:
        rr_col = cols[1]

    return date_col, rr_col


# =====================================================
# 🔹 FLEXIBLE PKL DATA LOADER (EVALUASI / GRAFIK)
# =====================================================
@st.cache_data
def load_pkl_data(file_path):
    """Loader fleksibel untuk file .pkl (DataFrame / dict berisi DataFrame)."""
    try:
        data = pd.read_pickle(file_path)

        if isinstance(data, pd.DataFrame):
            df = data.copy()
        elif isinstance(data, dict):
            df = next((v.copy() for v in data.values() if isinstance(v, pd.DataFrame)), None)
            if df is None:
                st.error(f"⚠️ {file_path} tidak mengandung DataFrame valid.")
                return None
        else:
            st.error(f"⚠️ {file_path} bukan format yang dikenali.")
            return None

        if isinstance(df.index, pd.PeriodIndex):
            df.index = df.index.to_timestamp(how="end")

        if not isinstance(df.index, pd.DatetimeIndex):
            date_cols = [c for c in df.columns if any(k in c.lower() for k in ['tanggal','bulan','date','periode'])]
            if date_cols:
                df = df.set_index(date_cols[0])
                df.index = pd.to_datetime(df.index, errors="coerce")

        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.RangeIndex(1, len(df) + 1, name="Index")

        return df

    except FileNotFoundError:
        st.error(f"❌ File {file_path} tidak ditemukan.")
        return None
    except Exception as e:
        st.error(f"❌ Error load {file_path}: {e}")
        return None


# =====================================================
# 🔹 CLEAN DATA FOR PREDICTION (FIX FOR ONEHOTENCODER ERRORS)
# =====================================================
def clean_data_for_prediction(df, preprocessor):
    """
    Bersihkan data untuk prediksi agar cocok dengan preprocessor yang sudah di-fit.
    - Strip dan map kategori ke categories yang valid.
    - Pastikan numeric columns aman.
    """
    if preprocessor is None:
        return df

    # Ambil kategori dari OneHotEncoder di preprocessor
    cat_cols = []
    if hasattr(preprocessor, 'named_transformers_'):
        for name, trans in preprocessor.named_transformers_.items():
            if hasattr(trans, 'categories_') and len(trans.categories_) > 0:
                cat_cols.append(name)
                categories = list(trans.categories_[0])  # Asumsi single column per transformer
                if name in df.columns:
                    df[name] = df[name].astype(str).str.strip()
                    # Map unknown ke kategori pertama (atau 'Unknown' jika ada)
                    df[name] = df[name].apply(lambda x: x if x in categories else (categories[0] if categories else 'Unknown'))

    # Pastikan kolom numeric aman
    numeric_cols = [col for col in df.columns if col not in cat_cols + ['Tanggal']]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


# =====================================================
# PRA-PROCESSING
# =====================================================
from pathlib import Path
import pandas as pd

# BASE_DIR menunjuk ke folder 'rainpredict_app'
DATASET_PATH = Path(__file__).resolve().parent

def load_dataset():
    # Gunakan .parent untuk naik 1 tingkat ke folder 'skripsi_hujan_web'
    path = DATASET_PATH.parent / "data iklim harian - Semarang (2020-2023).xlsx"
    
    df = pd.read_excel(path)
    return df
    
# =====================================================
# LOAD DATASET AMAN
# =====================================================
def load_dataset(path=DATASET_PATH):
    """
    Load dataset harian dan pastikan kolom numeric & kategori aman untuk scikit-learn.
    """
    df = pd.read_excel(path)
    df['Tanggal'] = pd.to_datetime(df['Tanggal'], format='%d-%m-%Y', errors='coerce')
    df = df.sort_values('Tanggal').reset_index(drop=True)

    # Pastikan numeric
    numeric_cols = ["Tn", "Tx", "Tavg", "RH_avg", "ss", "ff_x", "ddd_x", "ff_avg", "RR"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Pastikan kategori aman untuk OneHotEncoder
    cat_cols = ['ddd_car']  # tambahkan kolom kategori lain jika ada
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().fillna('Unknown')

    return df


# =====================================================
# MISSING VALUE HANDLING
# =====================================================
def handle_missing(df):
    """
    Penanganan missing value aman untuk scikit-learn:
    - Interpolasi linear untuk kolom numeric smooth
    - Imputasi musiman RR
    - Imputasi modus ddd_car
    """
    # --- Numeric smooth
    numeric_cols = ["Tn", "Tx", "Tavg", "RH_avg", "ss", "ff_x", "ddd_x", "ff_avg"]
    df[numeric_cols] = df[numeric_cols].interpolate(method="linear", limit_direction="both")

    # --- Imputasi musiman RR
    df['Bulan'] = df['Tanggal'].dt.month
    rr_monthly_median = df.groupby('Bulan')['RR'].transform(lambda x: x.fillna(x.median()))
    df['RR'] = df['RR'].fillna(rr_monthly_median)
    df['RR'] = df['RR'].interpolate(method="linear", limit_direction="both")

    # --- Imputasi ddd_car
    df.loc[(df['ff_avg'] == 0) & (df['ddd_car'].isna()), 'ddd_car'] = 'C'

    def mode_impute(x):
        return x.mode()[0] if not x.mode().empty else 'Unknown'

    monthly_mode = df.groupby('Bulan')['ddd_car'].transform(lambda x: x.fillna(mode_impute(x)))
    df['ddd_car'] = df['ddd_car'].fillna(monthly_mode)
    global_mode = df['ddd_car'].mode()[0]
    df['ddd_car'] = df['ddd_car'].fillna(global_mode)

    df.drop(columns='Bulan', inplace=True)

    # --- Pastikan numeric
    for col in numeric_cols + ['RR']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # --- Pastikan kategori aman untuk OneHotEncoder
    cat_cols = ['ddd_car']  # tambahkan kolom kategori lain jika ada
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().fillna('Unknown')

    return df


# =====================================================
# VALIDASI TIME SERIES
# =====================================================
def validate_timeseries(df):
    full_range = pd.date_range(df['Tanggal'].min(), df['Tanggal'].max(), freq='D')
    return {
        "is_sorted": df['Tanggal'].is_monotonic_increasing,
        "missing_days": full_range.difference(df['Tanggal']),
        "duplicate_dates": df[df['Tanggal'].duplicated(keep=False)]
    }


# =====================================================
# ENSURE CONTINUOUS DATE
# =====================================================
def ensure_continuous(df):
    full_range = pd.date_range(df['Tanggal'].min(), df['Tanggal'].max(), freq='D')
    df = df.set_index('Tanggal').reindex(full_range).reset_index()
    df.rename(columns={'index': 'Tanggal'}, inplace=True)
    return df



# =====================================================
# OUTLIER HANDLING
# =====================================================
def cap_iqr(series):
    Q1, Q3 = series.quantile([0.25, 0.75])
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR
    return np.where(series < lower, lower,
                    np.where(series > upper, upper, series))


def handle_outlier(df):
    before = df.copy()
    for col in df.select_dtypes(include=[np.number]).columns:
        if col == 'RR':
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - df[col].quantile(0.25)
            upper = Q3 + 1.5 * IQR
            df[col] = np.where(df[col] > upper, upper, df[col])
            df[col] = np.log1p(df[col])
        else:
            df[col] = cap_iqr(df[col])
    return before, df


# =====================================================
# FEATURE ENGINEERING
# =====================================================
def add_time_features(df):
    df['Tahun'] = df['Tanggal'].dt.year
    df['Bulan'] = df['Tanggal'].dt.month
    df['Month_sin'] = np.sin(2*np.pi*df['Bulan']/12)
    df['Month_cos'] = np.cos(2*np.pi*df['Bulan']/12)
    return df


def add_lag_rolling(df):
    for k in [1, 3, 7]:
        df[f'RR_lag{k}'] = df['RR'].shift(k)
    df['RR_roll_mean_3'] = df['RR'].rolling(3, min_periods=1).mean()
    df['RR_roll_std_3'] = df['RR'].rolling(3, min_periods=1).std().fillna(0)
    df.fillna(0, inplace=True)
    return df


# =====================================================
# TIME-BASED SPLIT
# =====================================================
def time_based_split(df, test_year=2023):
    train_df = df[df['Tanggal'].dt.year < test_year].copy()
    test_df = df[df['Tanggal'].dt.year == test_year].copy()
    return train_df, test_df
