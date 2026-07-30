"File ini berisi utlitas umum seerti helpers untuk tanggal, preprocessing, recursive predict, dan fungsi pembantu lainnya atau toolkit yang digunakan oleh file lain, seperti untuk memproses data atau menghasilkan narasi"

import os
import pickle
import importlib
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
from config import DATA_DEFAULT, PREPROCESSOR_PATH, MODEL_MAPPING, FEATURE_NAMES_MAP, EVAL_PATH_MAP
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from config import RANDOM_STATE

# -------------------------
# Utility: Smart load with fallbacks
# -------------------------
@st.cache_resource
def load_pickle_robust(path):
    if not os.path.exists(path):
        return None, f"Missing: {path}"
    try:
        with open(path, "rb") as f:
            obj = pickle.load(f)
        return obj, f"Loaded pickle: {path}"
    except Exception as e:
        try:
            with open(path, "rb") as f:
                class CompatUnpickler(pickle.Unpickler):
                    def find_class(self, module, name):
                        if module.startswith("numpy._core"):
                            module = module.replace("numpy._core", "numpy.core")
                        return super().find_class(module, name)
                unp = CompatUnpickler(f)
                obj = unp.load()
            return obj, f"Loaded with CompatUnpickler: {path}"
        except Exception:
            if importlib.util.find_spec("joblib"):
                try:
                    import joblib
                    obj = joblib.load(path)
                    return obj, f"Loaded with joblib: {path}"
                except Exception:
                    pass
            if importlib.util.find_spec("dill"):
                try:
                    import dill
                    with open(path, "rb") as f:
                        obj = dill.load(f)
                    return obj, f"Loaded with dill: {path}"
                except Exception:
                    pass
    return None, f"Failed load all fallback for {path}"

@st.cache_resource
def load_model_safe(path):
    obj, msg = load_pickle_robust(path)
    if obj is None:
        return None
    if hasattr(obj, "predict"):
        return obj
    return obj

@st.cache_data
def load_eval_metrics(mode):
    metrics = {}
    for name, path in EVAL_PATH_MAP[mode].items():
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    df_eval = pickle.load(f)
                if isinstance(df_eval, pd.DataFrame):
                    if 'Stacking' in df_eval.index:
                        row = df_eval.loc['Stacking']
                    else:
                        row = df_eval.iloc[0]
                    metrics[name] = {
                        "R2": float(row.get('R2', np.nan)),
                        "RMSE": float(row.get('RMSE', np.nan)),
                        "MAE": float(row.get('MAE', np.nan))
                    }
                else:
                    metrics[name] = {"R2": np.nan, "RMSE": np.nan, "MAE": np.nan}
            except Exception:
                metrics[name] = {"R2": np.nan, "RMSE": np.nan, "MAE": np.nan}
        else:
            metrics[name] = {"R2": np.nan, "RMSE": np.nan, "MAE": np.nan}
    if all(np.isnan(list(m.values())[0]) for m in metrics.values()):
        if mode == "Harian":
            metrics["Iterasi 2 (Terbaik)"] = {"R2": 0.663, "RMSE": 0.579, "MAE": 0.340}
        else:
            metrics["Iterasi 2 (Terbaik)"] = {"R2": 0.801, "RMSE": 50.1, "MAE": 35.8}
    return metrics

@st.cache_data
def load_preprocessor(path=PREPROCESSOR_PATH):
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                obj = pickle.load(f)
            if hasattr(obj, "transform"):
                return obj
            else:
                return None
        except Exception:
            return None
    return None

@st.cache_data
def load_feature_names(path):
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                obj = pickle.load(f)
            if isinstance(obj, (list, tuple)):
                return list(obj)
            else:
                return None
        except Exception:
            return None
    return None

# -------------------------
# Data loader
# -------------------------
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".xlsx") or uploaded_file.name.endswith(".xls"):
                df = pd.read_excel(uploaded_file, sheet_name=0)
            else:
                df = pd.read_csv(uploaded_file)
            return df
        except Exception as e:
            st.error(f"Error membaca file: {e}")
            return None
    else:
        if os.path.exists(DATA_DEFAULT):
            try:
                df = pd.read_excel(DATA_DEFAULT, sheet_name=0)
                return df
            except Exception as e:
                st.error(f"Gagal baca {DATA_DEFAULT}: {e}")
                return None
        else:
            return None

# -------------------------
# Date helpers
# -------------------------
def ensure_date_index(df, date_col_candidates=["date","Date","Tanggal","tanggal"]):
    if df is None or df.empty:
        return None
    df2 = df.copy()
    date_col = None
    for c in date_col_candidates:
        if c in df2.columns:
            date_col = c
            break
    if date_col is None:
        date_col = df2.columns[0]
        st.warning(f"Kolom tanggal tidak ditemukan; menggunakan kolom pertama: {date_col}")
    try:
        df2[date_col] = pd.to_datetime(df2[date_col], dayfirst=True, errors='coerce', infer_datetime_format=True)
        nat_count = df2[date_col].isna().sum()
        if nat_count > 0:
            st.warning(f"{nat_count} baris tanggal gagal parse; drop baris tersebut.")
            df2 = df2.dropna(subset=[date_col])
        if df2.empty:
            st.error("Semua tanggal gagal parse. Upload data dengan format tanggal valid.")
            return None
        df2 = df2.sort_values(date_col).reset_index(drop=True)
        df2 = df2.set_index(date_col)
        return df2
    except Exception as e:
        st.error(f"Error parsing date column {date_col}: {e}")
        return None

def create_future_dates(last_date, periods, mode="Harian"):
    if isinstance(last_date, (str,)):
        last_date = pd.to_datetime(last_date)
    if mode == "Harian":
        return [last_date + timedelta(days=i) for i in range(1, periods+1)]
    elif mode == "Bulanan":
        return [last_date + pd.DateOffset(months=i) for i in range(1, periods+1)]
    return []

# -------------------------
# Preprocess helper
# -------------------------
def _maybe_preprocess(X_manual, preproc):
    if preproc is not None:
        try:
            return preproc.transform(X_manual)
        except Exception:
            return X_manual.values
    return X_manual.values

# -------------------------
# Auto-narration generator
# -------------------------
def generate_narration(preds, mode, r2_score=None):
    if not preds:
        return "Belum ada prediksi. Unggah data untuk melihat hasil."
    avg_pred = np.mean(preds)
    if r2_score and r2_score > 0.7:
        accuracy = "sangat akurat"
    elif r2_score > 0.5:
        accuracy = "cukup baik"
    else:
        accuracy = "perlu ditingkatkan"
    if mode == "Harian":
        return f"Prediksi harian menunjukkan rata-rata {avg_pred:.1f} mm/hari. Model {accuracy} (R²={r2_score:.2f}), cocok untuk rencana harian seperti pertanian atau lalu lintas. Jika lag kemarin tinggi, besok kemungkinan hujan sedang."
    else:
        return f"Prediksi bulanan menunjukkan akumulasi {avg_pred:.1f} mm/bulan. Model {accuracy} (R²={r2_score:.2f}), berguna untuk perencanaan musiman seperti irigasi atau banjir. Perhatikan tren naik di musim hujan (Oktober-Maret) untuk antisipasi banjir di Semarang."

# -------------------------
# Recursive predict helper
# -------------------------
def recursive_predict(series_rr, model, n_periods, mode, feature_names=None, preprocessor=None):
    if model is None:
        raise ValueError("Model tidak tersedia. Periksa session state.")
    
    preds = []
    history = list(series_rr[-30:].astype(float))
    if len(history) == 0:
        history = [0.0]
    
    max_lag = 7 if mode == "Harian" else 3
    for i in range(n_periods):
        base = {}
        for l in range(1, max_lag + 1):
            base[f"RR_lag{l}"] = history[-l] if len(history) >= l else 0.0
        
        X_df = pd.DataFrame([base])
        
        if feature_names is not None:
            X_model_input = pd.DataFrame(0.0, index=[0], columns=feature_names)
            for col in X_model_input.columns:
                if 'RR_lag' in col:
                    try:
                        lagnum = int(col.split('_lag')[-1])
                        X_model_input.loc[0, col] = base.get(f"RR_lag{lagnum}", 0.0)
                    except Exception as e:
                        X_model_input.loc[0, col] = 0.0
        else:
            X_model_input = X_df
        
        try:
            if preprocessor is not None and hasattr(preprocessor, "transform"):
                X_proc = preprocessor.transform(X_model_input)
            else:
                X_proc = X_model_input.values
        except Exception as e:
            X_proc = X_model_input.values
        
        try:
            yhat = model.predict(X_proc)
            y = float(yhat[0]) if np.ndim(yhat) > 0 else float(yhat)
        except Exception as e:
            y = 0.0
        
        y = max(0.0, y)
        preds.append(y)
        history.append(y)
    
    return preds


class TimeSeriesPreprocessor(TransformerMixin, BaseEstimator):
    def __init__(self, mode='Harian', date_col='date', rr_col='RR',
                fill_method='interpolate', outlier_method='iqr',
                lags=3, rolling_windows=(3,7)):
        self.mode = mode
        self.date_col = date_col
        self.rr_col = rr_col
        self.fill_method = fill_method
        self.outlier_method = outlier_method
        self.lags = lags
        self.rolling_windows = rolling_windows
        self.feature_names_ = None

    def fit(self, X, y=None):
        return self

    def _parse_dates(self, df):
        df = df.copy()
        try:
            df[self.date_col] = pd.to_datetime(df[self.date_col])
        except Exception:
            # try infer
            df[self.date_col] = pd.to_datetime(df[self.date_col], infer_datetime_format=True, errors='coerce')
        df = df.sort_values(self.date_col).dropna(subset=[self.date_col])
        df = df.set_index(self.date_col)
        return df

    def _resample_if_needed(self, df):
        if self.mode.lower().startswith('h'):
            # daily
            df = df.asfreq('D')
        else:
            # monthly
            df = df.resample('M').sum()
        return df

    def _handle_missing(self, df):
        if self.fill_method == 'interpolate':
            df[self.rr_col] = df[self.rr_col].interpolate(limit_direction='both')
        elif self.fill_method == 'ffill':
            df[self.rr_col] = df[self.rr_col].fillna(method='ffill').fillna(0)
        else:
            df[self.rr_col] = df[self.rr_col].fillna(0)
        return df
    
    def _cap_outliers(self, df):
        if self.outlier_method == 'iqr':
            q1 = df[self.rr_col].quantile(0.25)
            q3 = df[self.rr_col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            df[self.rr_col] = df[self.rr_col].clip(lower, upper)
        return df

    def _time_features(self, df):
        df = df.copy()
        df['month'] = df.index.month
        df['day'] = df.index.day
        df['dayofweek'] = df.index.dayofweek
        df['dayofyear'] = df.index.dayofyear
        df['is_month_start'] = df.index.is_month_start.astype(int)
        df['is_month_end'] = df.index.is_month_end.astype(int)
        # circular encoding
        df['sin_month'] = np.sin(2 * np.pi * df['month'] / 12)
        df['cos_month'] = np.cos(2 * np.pi * df['month'] / 12)
        df['sin_dw'] = np.sin(2 * np.pi * df['dayofweek'] / 7)
        df['cos_dw'] = np.cos(2 * np.pi * df['dayofweek'] / 7)
        return df

    def _lag_rolling(self, df):
        for lag in range(1, self.lags + 1):
            df[f'RR_lag{lag}'] = df[self.rr_col].shift(lag)
        for w in self.rolling_windows:
            df[f'RR_roll_mean_{w}'] = df[self.rr_col].rolling(window=w, min_periods=1).mean().shift(1)
            df[f'RR_roll_std_{w}'] = df[self.rr_col].rolling(window=w, min_periods=1).std().shift(1).fillna(0)
        return df

    def transform(self, X):
        df = X.copy()
        df = self._parse_dates(df)
        df = self._resample_if_needed(df)
        # ensure numeric
        df[self.rr_col] = pd.to_numeric(df[self.rr_col], errors='coerce')
        df = self._handle_missing(df)
        df = self._cap_outliers(df)
        df = self._time_features(df)
        df = self._lag_rolling(df)
        # drop rows with NaN features created by shift
        df = df.dropna()
        # store features order
        self.feature_names_ = [c for c in df.columns if c != self.rr_col]
        X_out = df[self.feature_names_].copy()
        return X_out


def train_test_split_time(df, test_periods=365, mode='Harian'):
    # expects df indexed by date and target column named 'RR' or original
    # default test_periods for daily: 365, for monthly user may pass months (e.g., 12)
    if mode.lower().startswith('h'):
        test_n = int(test_periods)
    else:
        # monthly: interpret as months
        test_n = int(test_periods)
    train = df.iloc[:-test_n]
    test = df.iloc[-test_n:]
    return train, test


def save_artifacts(obj, path):
    joblib.dump(obj, path)


def load_artifacts(path):
    return joblib.load(path)










# ======================================================
# PATH CONFIG (Tetap)
# ======================================================
MODEL_PATHS = {
    "Harian": {
        1: "stacking_model_harian_iter1.pkl",
        2: "stacking_model_harian_iter2.pkl",
        3: "stacking_model_harian_iter3.pkl",
    },
    "Bulanan": {
        1: "stacking_model_bulanan_iter1.pkl",
        2: "stacking_model_bulanan_iter2.pkl",
        3: "stacking_model_bulanan_iter3.pkl",
    }
}

PREPROCESSOR_PATHS = {
    "Harian": "preprocessor_harian.pkl",
    "Bulanan": "preprocessor_bulanan.pkl",
}

# ======================================================
# LOADER (Tetap)
# ======================================================
@st.cache_resource
def load_pickle(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File tidak ditemukan: {path}")
    with open(path, "rb") as f:
        return pickle.load(f)

# ======================================================
# BASIC PREPROCESS (Tetap)
# ======================================================
def preprocess_dataset(uploaded_file):
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    date_candidates = ["tanggal", "Tanggal", "date", "Date", "datetime", "Datetime", "waktu", "Waktu"]
    date_col = next((c for c in df.columns if c in date_candidates), df.columns[0])
    df = df.rename(columns={date_col: "tanggal"})
    df["tanggal"] = pd.to_datetime(df["tanggal"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["tanggal"])
    if df.empty:
        raise ValueError("Semua nilai tanggal tidak valid")
    df = df.sort_values("tanggal").reset_index(drop=True)
    return df

# ======================================================
# OUTLIER (Tetap)
# ======================================================
def handle_outliers(df):
    before = df.copy()
    after = df.copy()
    for col in after.select_dtypes(include=np.number).columns:
        q1, q3 = after[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        after[col] = after[col].clip(q1 - 1.5 * iqr, q3 + 1.5 * iqr)
    return before, after

# ======================================================
# FEATURE ENGINEERING (Tetap)
# ======================================================
def detect_target(df):
    for c in df.columns:
        if c.lower() in ["rr", "curah_hujan", "curah_hujan_mm"]:
            return c
    raise ValueError("Kolom target curah hujan tidak ditemukan")

def add_time_features(df):
    df = df.copy()
    df["Month"] = df["tanggal"].dt.month
    df["Month_sin"] = np.sin(2 * np.pi * df["Month"] / 12)
    df["Month_cos"] = np.cos(2 * np.pi * df["Month"] / 12)
    return df

def add_lag_rolling_features(df):
    df = df.copy()
    target = detect_target(df)
    for lag in [1, 3, 7]:
        df[f"RR_lag{lag}"] = df[target].shift(lag)
    df["RR_roll_mean_3"] = df[target].rolling(3).mean()
    df["RR_roll_std_3"] = df[target].rolling(3).std()
    return df.dropna().reset_index(drop=True)

# ======================================================
# SPLIT (BAGIAN BULANAN DIPERBAIKI)
# ======================================================
def split_harian(df):
    target = detect_target(df)
    return df.drop(columns=[target, "tanggal"], errors="ignore")

def split_bulanan(df):
    """
    PERBAIKAN: Mengikuti logika agregasi dan feature engineering 
    sesuai code Google Colab agar hasil tidak 0.
    """
    df = df.copy()
    target = detect_target(df)
    
    # Rename target ke 'RR' agar konsisten dengan fitur lag/rolling di model
    df = df.rename(columns={target: 'RR'})
    
    # Pastikan kolom numerik sesuai dengan Colab
    for col in df.columns:
        if col != "tanggal":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # --- 1. Agregasi Bulanan (Sesuai Logika Colab) ---
    # Menggunakan resample agar lebih stabil di Streamlit
    agg_map = {
        'RR': 'sum',
        'Tavg': 'mean',
        'RH_avg': 'mean',
        'Tx': 'max',
        'Tn': 'min',
        'ss': 'mean',
        'ff_x': 'mean',
        'ff_avg': 'mean',
        'wind_sin': 'mean',
        'wind_cos': 'mean'
    }
    
    # Filter hanya kolom yang ada di dataset
    available_agg = {k: v for k, v in agg_map.items() if k in df.columns}
    
    df_m = df.set_index("tanggal").resample("M").agg(available_agg).reset_index()

    # --- 2. Feature Engineering Lag & Rolling (Sesuai Colab) ---
    # Dilakukan SEBELUM tail(6) agar data historis tidak hilang
    for k in [1, 2]:
        df_m[f'RR_lag{k}'] = df_m['RR'].shift(k)
        df_m[f'RR_roll_mean_{k}'] = df_m['RR'].rolling(k).mean()

    # --- 3. Final Touch ---
    # Isi NaN akibat lag dengan 0 (sesuai Colab fillna(0))
    df_m = df_m.fillna(0)
    
    # Ambil 6 bulan terakhir untuk prediksi
    df_m = df_m.tail(6)

    # Hapus kolom target dan tanggal sebelum dikirim ke model
    return df_m.drop(columns=["tanggal", "RR"], errors="ignore")

# ======================================================
# FINAL PREDICT
# ======================================================
def predict(df, mode, iteration):
    if mode not in ["Harian", "Bulanan"]:
        raise ValueError("Mode harus 'Harian' atau 'Bulanan'")

    if mode == "Harian":
        model_path = f"stacking_model_harian_iter{iteration}.pkl"
        prep_path  = "preprocessor_harian.pkl"
        split_result = split_harian(df)
    else:
        model_path = f"stacking_model_bulanan_iter{iteration}.pkl"
        prep_path  = "preprocessor_bulanan.pkl"
        split_result = split_bulanan(df)

    model = load_pickle(model_path)
    preprocessor = load_pickle(prep_path)

    if isinstance(split_result, (tuple, list)):
        X = split_result[0]
    else:
        X = split_result

    X = X.copy()
    
    # Penyelaras fitur: pastikan kolom yang diminta preprocessor ada
    for col in preprocessor.feature_names_in_:
        if col not in X.columns:
            X[col] = 0

    # Urutkan kolom sesuai urutan saat training
    X = X[preprocessor.feature_names_in_]

    # Pastikan tipe data numerik
    for col in X.columns:
        if X[col].dtype == "object":
            X[col] = X[col].astype(str).str.strip().replace({"nan": np.nan, "": np.nan})
        X[col] = pd.to_numeric(X[col], errors="ignore")
        if X[col].dtype == "object":
            X[col] = X[col].fillna("Unknown")
        else:
            X[col] = X[col].fillna(0.0)

    # Transformasi dan Prediksi
    X_transformed = preprocessor.transform(X)
    y_pred = model.predict(X_transformed)
    
    # Pastikan tidak ada prediksi negatif
    y_pred = np.maximum(y_pred, 0)

    return pd.DataFrame({
        "prediksi_curah_hujan": y_pred
    })




def generate_narration(result_df, mode):
    # Hitung statistik dasar dari hasil prediksi
    avg_rain = result_df["prediksi_curah_hujan"].mean()
    max_rain = result_df["prediksi_curah_hujan"].max()
    
    # Interpretasi Kategori BMKG
    def get_category(val, is_monthly):
        if is_monthly:
            if val <= 100: return "Rendah"
            elif val <= 300: return "Menengah"
            elif val <= 500: return "Tinggi"
            else: return "Sangat Tinggi"
        else:
            if val == 0: return "Berawan/Cerah"
            elif val <= 20: return "Hujan Ringan"
            elif val <= 50: return "Hujan Sedang"
            elif val <= 100: return "Hujan Lebat"
            else: return "Hujan Sangat Lebat"

    category = get_category(avg_rain, mode == "Bulanan")
    

    def generate_narration(result_df, mode):
    # Hitung statistik dasar
        avg_rain = result_df["prediksi_curah_hujan"].mean()
        max_rain = result_df["prediksi_curah_hujan"].max()
        
    # Interpretasi Kategori BMKG
    def get_category(val, is_monthly):
        if is_monthly:
            if val <= 100: return "Rendah"
            elif val <= 300: return "Menengah"
            elif val <= 500: return "Tinggi"
            else: return "Sangat Tinggi"
        else:
            if val == 0: return "Cerah/Berawan"
            elif val <= 20: return "Hujan Ringan"
            elif val <= 50: return "Hujan Sedang"
            elif val <= 100: return "Hujan Lebat"
            else: return "Hujan Sangat Lebat"

    category = get_category(avg_rain, mode == "Bulanan")
    label_satuan = "Bulanan" if mode == "Bulanan" else "Harian"

    # Tampilan Narasi Terpadu
    st.info(f"**Analisis Hasil Prediksi {label_satuan}**")
    
    narasi = f"""
    Kolom kiri menunjukkan hari ke- dan kolom kanan menunjukkan hasil prediksi, jika 0 maka {label_satuan} tersebut tidak turun hujan.
    Hasil pemrosesan model menunjukkan bahwa rata-rata curah hujan berada pada angka **{avg_rain:.2f} mm**, 
    yang dikategorikan sebagai kondisi **{category}** menurut standar BMKG. Analisis data mendeteksi 
    puncak curah hujan (maximum) mencapai **{max_rain:.2f} mm**. 

    **Catatan Teknis:** Prediksi ini dihasilkan melalui arsitektur *Stacking Ensemble* dengan mengoptimalkan korelasi variabel 
    cuaca historis dan fitur temporal (sin/cos). Secara statistik, hasil ini mencerminkan pola fluktuasi 
    yang dipengaruhi oleh fitur *lag* (data masa lalu) dan *rolling mean* yang telah diproses. 
    Diharapkan hasil ini dapat menjadi referensi strategis dalam pengambilan keputusan terkait mitigasi 
    cuaca di wilayah terkait.
    """
    st.write(narasi)