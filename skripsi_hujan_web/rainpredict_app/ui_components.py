""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
from datetime import datetime
from PIL import Image
from loaders import load_data, load_eval_metrics, load_feature_names, load_preprocessor, compute_best_iteration_for_mode
from utils import ensure_date_index, create_future_dates, _maybe_preprocess, recursive_predict, generate_narration
from config import MODEL_MAPPING, FEATURE_NAMES_MAP, SHAP_PATH_MAP, EVAL_PATH_MAP, PREPROCESSOR_PATH
from loaders import resolve_path

def sidebar():
    with st.sidebar:
        # Bagian Branding/Logo
        st.markdown("""
            <div style="text-align: center;">
                <h1 style='color: #1E88E5;'>🌧️ RainPredict</h1>
                <p style='font-size: 0.9em; color: #555;'>Semarang Weather Forecasting System</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        
        # Deskripsi singkat aplikasi
        st.subheader("Aplikasi Prediksi Curah Hujan")
        st.write("""
        RainPredict Semarang adalah sistem prediksi curah hujan harian dan bulanan berbasis model stacking ensemble dengan studi kasus Kota Semarang, 
        dan dapat diterapkan pada wilayah lain selama data memenuhi karakteristik deret waktu (*time series*).
        """)
        
        # Fitur utama
        st.markdown("### Fitur Utama:")
        st.markdown("- **Prediksi Harian**: Analisis curah hujan per hari.")
        st.markdown("- **Prediksi Bulanan**: Ramalan untuk 6 bulan terakhir.")
        
        # Instruksi singkat
        st.markdown("### Cara Penggunaan:")
        st.write("1. Unggah file Excel atau .csv data hujan.")
        st.write("2. Pilih mode (Harian/Bulanan) dan iterasi.")
        st.write("3. Klik 'Prediksi' untuk hasil.")
        
        # Info tambahan
        st.markdown("---")
        #st.write("**Versi:** 1.0")
        st.write("**Dikembangkan untuk:** Penelitian dan Analisis Cuaca")
        
        # Kontak atau disclaimer
        st.markdown("### Kontak:")
        st.write("Untuk pertanyaan, hubungi: sekarayuning8121@students.unnes.ac.id")
        st.caption("Disclaimer: Prediksi berdasarkan data historis. Gunakan sebagai referensi, bukan keputusan akhir.")


def tabs():
    df_raw = load_data(st.session_state.get('uploaded_file'))
    st.session_state.df_raw = df_raw

    tab_home, tab_prediksi, tab_model, tab_about = st.tabs(["Home", "Prediksi", "Model", "About"])

    # Tab Home: Pembuka skripsi dengan judul, pentingnya curah hujan, dll.
        # Tab Home: Pembuka skripsi dengan judul, pentingnya curah hujan, dll.
    with tab_home:
        with tab_home:
            # ============================================================
            # HERO SECTION – Judul & Deskripsi + Logo (dengan jarak pas)
            # ============================================================
            col1, col2 = st.columns([2.4, 0.9], gap="large")  # rasio lebih lebar untuk teks
        
            with col1:
                st.markdown("""
                <div class="home-hero">
                    <h1 style="font-size:2.6rem; font-weight:800; margin-bottom:0.2rem;">
                        🌧️ Prediksi Curah Hujan
                    </h1>
                    <h3 style="font-weight:500; color:#C4B0F8; margin-top:0.2rem; line-height:1.4;">
                        Stacking Ensemble dengan XGBoostRegressor<br>
                        dan Interpretabilitas Global SHAP
                    </h3>
                    <p style="font-size:1rem; text-align:justify; margin-top:1rem; color:#E0D8F0; line-height:1.6;">
                        Aplikasi web ini merupakan implementasi hasil skripsi yang bertujuan
                        untuk memprediksi curah hujan di <b>Kota Semarang</b> menggunakan pendekatan
                        <b>Stacking Ensemble Learning</b> dengan meta-model
                        <b>XGBoostRegressor</b>, serta didukung oleh interpretabilitas global
                        menggunakan <b>SHAP (SHapley Additive exPlanations)</b>.
                        Pada implementasi website, sistem difokuskan untuk <b>menyajikan hasil prediksi</b>
                        curah hujan harian dan bulanan secara efisien dan mudah digunakan.
                        Visualisasi SHAP tidak ditampilkan pada aplikasi web karena bersifat
                        analisis penelitian dan membutuhkan sumber daya komputasi yang tinggi.
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
            with col2:
                with col2:
                    # Lottie Animation - Rain Weather
                    st.markdown("""
                    <div style="
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        margin-top: 10px;
                        background: rgba(255,255,255,0.03);
                        border-radius: 24px;
                        padding: 12px;
                    ">
                        <lottie-player 
                            src="https://assets10.lottiefiles.com/packages/lf20_2b9f3b1a.json" 
                            background="transparent" 
                            speed="1" 
                            style="width: 280px; height: 280px;"
                            loop 
                            autoplay>
                        </lottie-player>
                    </div>
                    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
                    """, unsafe_allow_html=True)
        
            st.divider()

        # ============================================================
        # KENAPA PREDIKSI CURAH HUJAN PENTING – dengan ikon & card
        # ============================================================
        st.markdown("""
        <div class="section-title">
            <h2 style="font-weight:700; margin-bottom:0.5rem;">
                🌱 Mengapa Prediksi Curah Hujan Penting?
            </h2>
            <p style="color:#B8B0D0; font-size:1.05rem;">
                Prediksi curah hujan memiliki peran strategis dalam berbagai sektor kehidupan,
                khususnya di wilayah perkotaan seperti Semarang:
            </p>
        </div>
        """, unsafe_allow_html=True)

        colA, colB = st.columns(2, gap="medium")

        with colA:
            st.markdown("""
            <div class="home-card">
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
                    <span style="font-size:28px;">🌾</span>
                    <h4 style="margin:0; font-weight:600;">Pertanian</h4>
                </div>
                <p style="margin:0 0 0 40px; color:#D4CCE8;">
                    Membantu perencanaan tanam dan panen serta mengurangi risiko gagal panen.
                </p>
            </div>
            <div class="home-card" style="margin-top:12px;">
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
                    <span style="font-size:28px;">🚗</span>
                    <h4 style="margin:0; font-weight:600;">Transportasi</h4>
                </div>
                <p style="margin:0 0 0 40px; color:#D4CCE8;">
                    Mengantisipasi kemacetan dan kecelakaan akibat hujan deras.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with colB:
            st.markdown("""
            <div class="home-card">
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
                    <span style="font-size:28px;">🌊</span>
                    <h4 style="margin:0; font-weight:600;">Mitigasi Bencana</h4>
                </div>
                <p style="margin:0 0 0 40px; color:#D4CCE8;">
                    Mendukung kesiapsiagaan terhadap banjir yang sering terjadi di Semarang.
                </p>
            </div>
            <div class="home-card" style="margin-top:12px;">
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
                    <span style="font-size:28px;">🏥</span>
                    <h4 style="margin:0; font-weight:600;">Kesehatan Masyarakat</h4>
                </div>
                <p style="margin:0 0 0 40px; color:#D4CCE8;">
                    Mengurangi risiko penyakit musiman yang meningkat saat musim hujan.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # ============================================================
        # PENJELASAN AWAM & PROFESIONAL – dalam card terpisah
        # ============================================================
        st.markdown("""
        <div style="display:flex; gap:20px; flex-wrap:wrap; justify-content:center; margin:20px 0;">
            <div class="home-card" style="flex:1; min-width:220px; background:rgba(167,139,250,0.08); border-left:4px solid #A78BFA;">
                <h4 style="margin-top:0;">👥 Untuk Masyarakat Umum</h4>
                <p style="margin:0; color:#D4CCE8;">
                    Aplikasi ini membantu memperkirakan apakah akan terjadi hujan,
                    sehingga dapat digunakan untuk perencanaan aktivitas harian.
                </p>
            </div>
            <div class="home-card" style="flex:1; min-width:220px; background:rgba(125,211,252,0.08); border-left:4px solid #7DD3FC;">
                <h4 style="margin-top:0;">🔬 Untuk Akademisi & Profesional</h4>
                <p style="margin:0; color:#D4CCE8;">
                    Model dibangun menggunakan data historis iklim dan pendekatan
                    ensemble learning dengan performa tinggi, sehingga relevan
                    untuk penelitian dan analisis klimatologi.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ============================================================
        # CALL TO ACTION – tombol besar di tengah
        # ============================================================
        st.markdown(
            "<h3 style='text-align:center; font-weight:600; margin-bottom:0.5rem;'>🚀 Mulai Prediksi Curah Hujan Anda</h3>",
            unsafe_allow_html=True
        )

        col_btn = st.columns([1, 1.5, 1])
        with col_btn[1]:
            if st.button("⚡ Prediksi Sekarang", use_container_width=True):
                st.info("Klik tab **Prediksi** di bagian navbar/atas untuk melanjutkan.")




        
    with tab_prediksi:
        from utils import (
            preprocess_dataset,
            handle_outliers,
            add_time_features,
            add_lag_rolling_features,
            predict,
            generate_narration
        )

        st.title("Mulai Prediksi Sekarang")

        # ======================================================
        # UPLOAD DATA & INSTRUKSI
        # ======================================================
        st.markdown("""
        ### Petunjuk Unggah Data
        Untuk mendapatkan hasil prediksi yang akurat dan konsisten, harap perhatikan ketentuan dataset berikut:

        1. **Format File**  
        Sistem mendukung format **.xlsx (Excel)** dan **.csv**.

        2. **Struktur Data (Time Series)**  
        Dataset harus berupa data deret waktu (*time series*) yang tersusun secara kronologis dan berkelanjutan, baik dalam skala **harian, bulanan, maupun tahunan**.

        3. **Penggabungan Data (Wajib)**  
        Seluruh data **harus digabungkan terlebih dahulu menjadi satu file** sebelum diunggah.  
        Sistem **tidak memproses banyak file secara terpisah**, sehingga penggabungan data dilakukan di sisi pengguna untuk menjaga konsistensi pemodelan.

        4. **Kecukupan Data Historis**  
        Hindari mengunggah data dalam rentang waktu yang terlalu pendek (misalnya hanya satu hari).  
        Model membutuhkan data historis yang memadai untuk mempelajari pola tren, musiman, dan rata-rata bergerak secara optimal.

        5. **Sumber Data (Direkomendasikan)**  
        Untuk menjaga validitas dan keandalan hasil prediksi, sangat disarankan menggunakan data resmi dari **BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)** atau sumber terpercaya yang setara.
        """)


        uploaded_file = st.file_uploader("Pilih file dataset Anda", type=["xlsx", "csv"])

        if uploaded_file:
            status_proses=st.empty()
            status_proses.info("Sedang memproses data...")

            # ======================================================
            # PREPROCESSING & FEATURE ENGINEERING
            # ======================================================
            # 1. Preprocessing Awal
            df = preprocess_dataset(uploaded_file)

            # 2. Penanganan Outlier 
            # (Silakan uncomment bagian di bawah ini jika ingin mengaktifkan pembersihan outlier secara manual)
            df_before, df_after = handle_outliers(df)
            
            # --- Bagian Tabel Perbandingan Outlier (Uncomment untuk memanggil) ---
            # st.subheader("Perbandingan Statistik Data")
            # col_ot1, col_ot2 = st.columns(2)
            # with col_ot1:
            #     st.markdown("**Sebelum Outlier Handling**")
            #     st.dataframe(df_before.describe())
            # with col_ot2:
            #     st.markdown("**Sesudah Outlier Handling**")
            #     st.dataframe(df_after.describe())

            # 3. Feature Engineering 
            # (Wajib dijalankan karena model membutuhkan fitur ini)
            df_feat = add_time_features(df_after)
            df_feat = add_lag_rolling_features(df_feat)

            # Menghilangkan pesan info setelah proses di atas selesai
            status_proses.empty()

            # ======================================================
            # TAMPILKAN RINGKASAN PROSES (USER & PAKAR)
            # ======================================================
            with st.expander("Lihat Ringkasan Pra-pemrosesan Data"):
                st.markdown("""
                Sistem telah melakukan serangkaian langkah teknis untuk memastikan data siap digunakan oleh model:
                
                1. **Pembersihan Data Awal**: Menyelaraskan format waktu dan menangani nilai kosong pada dataset.
                2. **Penanganan Outlier**: Mengidentifikasi nilai ekstrem yang tidak wajar menggunakan metode statistik agar tidak mengganggu stabilitas prediksi.
                3. **Transformasi Temporal**: Mengubah variabel waktu ke dalam fungsi matematis untuk menangkap pola siklus musiman iklim.
                4. **Ekstraksi Fitur Historis**: Membuat fitur *Lag* (data sebelumnya) dan *Rolling Statistics* (rata-rata bergerak) guna menangkap tren jangka pendek dan jangka panjang.
                """)

            st.success("Data berhasil diproses dan siap diprediksi.")

            # ======================================================
            # PENGATURAN PREDIKSI
            # ======================================================
            st.subheader("Pengaturan Prediksi")
            mode = st.radio(
                "Pilih skema prediksi:",
                ["Harian", "Bulanan"],
                horizontal=True,
                help="Harian untuk prediksi tiap hari, Bulanan untuk akumulasi total per bulan."
            )

            # ======================================================
            # EKSEKUSI PREDIKSI
            # ======================================================
            if st.button("Jalankan Prediksi"):
                col1, col2 = st.columns([1, 1.2])

                with col1:
                    with st.spinner("Sistem sedang menghitung..."):
                        result = predict(df=df_feat, mode=mode, iteration=2)

                    st.success("Prediksi Selesai")
                    st.dataframe(result.head(10), use_container_width=True)
                    
                    st.download_button(
                        "Download Hasil Prediksi (CSV)",
                        data=result.to_csv(index=False),
                        file_name=f"hasil_prediksi_{mode.lower()}_iter1.csv",
                        mime="text/csv"
                    )

                with col2:
                    # Menampilkan narasi analisis gabungan (Umum & Pakar)
                    generate_narration(result, mode)
        

    # Tab Model: Metode dan hasil
    with tab_model:
        st.markdown('<div class="card"><h3>Informasi Dataset</h3></div>', unsafe_allow_html=True)
        # 1. Kolom kiri: grafik historis curah hujan
        # Kolom kanan: rata-rata curah hujan dan menampilkan preview dataset
        col_left, col_right = st.columns([2, 1])
        with col_left:
            if df_raw is not None:
                df_idx = ensure_date_index(df_raw)
                if df_idx is not None:
                    st.markdown("### Ringkasan Dataset")
                    with st.expander("Detail Dataset", expanded=True):
                        try:
                            min_date = df_idx.index.min().strftime('%d %B %Y')
                            max_date = df_idx.index.max().strftime('%d %B %Y')
                            st.success(f"**Periode Data:** {min_date} → {max_date}")
                        except Exception:
                            st.warning("**Periode:** Tidak dapat dibaca (format tanggal tidak valid)")
                        st.info(f"**Jumlah Data:** {len(df_idx):,} baris")
                        st.info(f"**Sumber Data:** Kaggle (Public Dataset)")

                    # --- Membuat Grafik Historis Curah Hujan berdasarkan dataset ---
                    # choose RR column
                    rr_candidates = [c for c in df_idx.columns if any(w in c.lower() for w in ["rr", "curah", "precip"])]
                    rr_col = rr_candidates[0] if rr_candidates else df_idx.columns[0]

                    st.markdown("### Historis Curah Hujan")
                    if st.session_state.mode == "Bulanan":
                        df_idx['month'] = df_idx.index.to_period('M').to_timestamp()
                        df_hist = df_idx.groupby('month')[rr_col].sum().reset_index().set_index('month')
                        x = df_hist.index; y = df_hist[rr_col].values; title = "Historis Curah Hujan Bulanan (Akumulasi)"
                        y_title = "mm/bulan"
                        total_rain = float(df_hist[rr_col].sum())
                        avg_rain = float(df_hist[rr_col].mean())
                    else:
                        x = df_idx.index; y = df_idx[rr_col].values; title = "Historis Curah Hujan Harian"
                        y_title = "mm/hari"
                        total_rain = float(df_idx[rr_col].sum())
                        avg_rain = float(df_idx[rr_col].mean())

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=x, y=y, mode='lines',
                        name='Actual RR', line=dict(color='#0369a1', width=2)))
                    fig.update_layout(
                        title=title,
                        xaxis_title="Tanggal",
                        yaxis_title=y_title,
                        template="plotly_white",
                        height=280)
                    st.plotly_chart(fig, use_container_width=True)

                    # simpan hasil ke session_state agar bisa digunakan di bagian statistik
                    st.session_state.total_rain = total_rain
                    st.session_state.avg_rain = avg_rain

                    # simpan ringkasan
                    st.info(f"**Kolom Curah Hujan Digunakan:** `{rr_col}`")
                    st.caption("*Grafik interaktif: Hover untuk detail, zoom/pan untuk eksplorasi. Data diisi 0 untuk missing values.*")

        with col_right:
            with st.container():
                st.markdown("Preview Dataset")
                try:
                    st.dataframe(df_idx.head(5), use_container_width=True, height=220)
                except Exception:
                    st.error("Gagal menampilkan preview dataset.")

                st.markdown("Statistik Curah Hujan")
                # pastikan nilai total dan rata-rata sudah disimpan di session_state
                if all(k in st.session_state for k in ['total_rain', 'avg_rain', 'mode']):
                    total_rain = float(st.session_state.total_rain)
                    avg_rain = float(st.session_state.avg_rain)
                    mode = st.session_state.mode

                    # tentukan satuan waktu
                    unit = 'hari' if mode.lower() == 'harian' else 'bulan'

                    # tampilkan metrik
                    st.metric(
                        label="Total Curah Hujan",
                        value=f"{total_rain:.1f} mm",
                        delta=f"Rata-rata: {avg_rain:.1f} mm/{unit}"
                    )
                else:
                    st.info("Statistik curah hujan belum tersedia. Silakan buat grafik historis terlebih dahulu.")
        st.markdown("---")

        # PRE-PROCESSING
        st.markdown('<div class="card"><h3>Pra-Pemrosesan Data Curah Hujan</h3></div>', unsafe_allow_html=True)
        from loaders import (
            load_dataset,
            validate_timeseries,
            ensure_continuous,
            handle_missing,
            handle_outlier,
            add_time_features,
            add_lag_rolling,
            time_based_split
        )

        #st.set_page_config(layout="wide")
        #st.title("Pra-Pemrosesan Data Curah Hujan Harian")

        # =====================================================
        # LOAD AWAL
        # =====================================================
        df = load_dataset()

        tabs = st.tabs([
            "Validasi Data",
            "Missing Value",
            "Outlier",
            "Feature Engineering",
            "Split Data"
        ])

        # ================= TAB 0 =================
        with tabs[0]:
            st.subheader("Validasi Time Series")
            result = validate_timeseries(df)

            c1, c2, c3 = st.columns(3)
            c1.metric("Tanggal Terurut", "Ya" if result['is_sorted'] else "Tidak")
            c2.metric("Tanggal Duplikat", "Tidak" if result['duplicate_dates'].empty else "Ada")
            c3.metric("Hari Hilang", len(result['missing_days']))

            with st.expander("Detail Hari Hilang"):
                st.write(result['missing_days'])

        # ================= TAB 1 =================
        with tabs[1]:
            st.subheader("Penanganan Missing Value")

            df = ensure_continuous(df)
            before = df.copy()
            df = handle_missing(df)

            col_left, col_right = st.columns([1,1])
            with col_left:
                st.markdown("**Jumlah missing value sebelum imputasi:**")
                st.dataframe(before.isna().sum())

            with col_right:
                with st.container():
                    st.markdown("**Jumlah missing value sesudah imputasi:**")
                    st.dataframe(df.isna().sum())

        # ================= TAB 2 =================
        with tabs[2]:
            st.subheader("Penanganan Outlier")

            # Jalankan proses outlier (inti tetap)
            _, df = handle_outlier(df)

            st.subheader("Perbandingan Outlier Sebelum dan Sesudah Penanganan")

            # Path gambar hasil visualisasi IQR
            image_path = "IQR.png"  # sesuaikan dengan lokasi file kamu

            try:
                from PIL import Image
                image = Image.open(image_path)

                st.image(
                    image,
                    caption="Boxplot variabel cuaca sebelum (merah) dan sesudah (biru) penanganan outlier",
                    use_container_width=True
                )

            except FileNotFoundError:
                st.error(f"Gambar '{image_path}' tidak ditemukan. Pastikan file ada di folder assets.")

            st.markdown("""
            Visualisasi ini menunjukkan dampak penanganan outlier menggunakan metode
            **Interquartile Range (IQR)**.  
            Baris atas merepresentasikan distribusi data **sebelum** dilakukan capping outlier,
            sedangkan baris bawah menunjukkan distribusi data **setelah** penanganan outlier.
            """)

            st.info(
                "Outlier ditangani menggunakan metode Interquartile Range (IQR). "
                "Khusus variabel curah hujan (RR), diterapkan transformasi logaritmik "
                "untuk mengurangi skewness sehingga distribusi data menjadi lebih stabil "
                "dan representatif untuk pemodelan machine learning."
            )

        # ================= TAB 3 =================
        with tabs[3]:
            st.subheader("Feature Engineering")

            st.markdown("""
            Feature engineering dilakukan untuk menangkap pola musiman dan
            ketergantungan temporal pada data curah hujan harian.
            """)

            st.markdown("### Fitur Waktu")
            st.markdown("""
            - **Tahun & Bulan**: menangkap tren dan musim tahunan  
            - **Month_sin & Month_cos**: representasi siklus bulan secara kontinu
            """)

            st.markdown("### Fitur Lag Curah Hujan")
            st.markdown("""
            - RR_lag1: pengaruh 1 hari sebelumnya  
            - RR_lag3: pengaruh jangka pendek  
            - RR_lag7: pengaruh mingguan
            """)

            st.markdown("### Fitur Rolling Statistik")
            st.markdown("""
            - RR_roll_mean_3: rata-rata hujan 3 hari terakhir  
            - RR_roll_std_3: variasi hujan 3 hari terakhir
            """)

            df = add_time_features(df)
            df = add_lag_rolling(df)

            with st.expander("Daftar fitur akhir"):
                st.code(df.columns.tolist())

        # ================= TAB 4 =================
        with tabs[4]:
            st.subheader("Pembagian Data Train dan Test")

            st.markdown("""
            Data dibagi berdasarkan urutan waktu (*time-based split*)
            untuk menghindari kebocoran data (*data leakage*).
            """)

            train_df, test_df = time_based_split(df)

            c1, c2 = st.columns(2)
            c1.metric("Data Train (2020–2022)", len(train_df))
            c2.metric("Data Test (2023)", len(test_df))

            with st.expander("Preview Data Train"):
                st.dataframe(train_df.head())

            with st.expander("Preview Data Test"):
                st.dataframe(test_df.head())

            st.success("Pra-pemrosesan selesai. Dataset siap untuk tahap pemodelan.")

        st.markdown("---")
        # ============================================================
        # HASIL AKURASI & EVALUASI MODEL
        # ============================================================

        st.markdown(
            '<div class="card"><h3>Konfigurasi Model Prediksi Curah Hujan</h3></div>',
            unsafe_allow_html=True
        )
        st.caption(
            "Halaman ini menjelaskan alur eksperimen penelitian, konfigurasi model, "
            "serta strategi tuning hyperparameter yang diterapkan pada setiap iterasi."
        )

        st.markdown("""
        **Metode yang Digunakan**  
        Penelitian ini menerapkan pendekatan **Stacking Ensemble**, yang mengombinasikan
        beberapa *base learner* (Random Forest dan Support Vector Regression) dengan
        **XGBoost Regressor** sebagai *meta learner*.

        Pendekatan ini bertujuan untuk meningkatkan akurasi prediksi dengan
        memanfaatkan keunggulan masing-masing model.  
        Interpretabilitas model dianalisis menggunakan **SHAP**, yang memberikan
        penjelasan global terkait kontribusi setiap fitur terhadap hasil prediksi,
        misalnya pengaruh curah hujan pada hari sebelumnya (*lag feature*).
        """)

        st.markdown("""
        Perancangan model ini berdasarkan dataset:

         *data iklim harian – Semarang (2020–2023).xlsx*

        Data dianalisis dalam dua skema waktu, yaitu **Harian** dan **Bulanan**,
        sesuai dengan konteks dan kebutuhan prediksi curah hujan.
        """)
        st.markdown("---")
        # ALUR UMUM PENELITIAN
        st.header("Alur Umum Penelitian")

        st.markdown("""
        Penelitian ini menggunakan pendekatan **Stacking Ensemble Learning**
        untuk memprediksi curah hujan harian dan bulanan melalui tahapan berikut:

        1. **Pra-pemrosesan Data**  
        Data iklim disusun dalam bentuk deret waktu (*time series*),
        kemudian dibagi menjadi data latih dan data uji.

        2. **Pelatihan Base Learners**  
        Model dasar yang digunakan adalah **Random Forest Regressor (RF)**
        dan **Support Vector Regression (SVR)**.

        3. **Pembentukan Stacking Ensemble**  
        Output dari base learner digabungkan dan dipelajari kembali oleh
        **XGBoost Regressor** sebagai *meta learner*.

        4. **Eksperimen Bertahap (Iteratif)**  
        Proses eksperimen dilakukan dalam tiga iterasi untuk mengevaluasi
        dampak tuning parameter terhadap performa model.
        """)
        st.markdown("---")
        # ITERASI 1
        st.header("Iterasi 1 — Model Baseline (Tanpa Tuning)")

        st.markdown("""
        **Tujuan Iterasi 1**  
        Iterasi ini bertujuan untuk menetapkan **baseline performa model**
        dengan menggunakan parameter default (tanpa proses tuning).
        Hasil dari iterasi ini digunakan sebagai acuan pembanding
        pada iterasi selanjutnya.
        """)

        df_iter1 = pd.DataFrame([
            {
                "Komponen": "Random Forest",
                "Parameter Utama": "n_estimators=200, max_depth=10, min_samples_leaf=5",
                "Keterangan": "Base learner tanpa tuning"
            },
            {
                "Komponen": "SVR",
                "Parameter Utama": "C=1.0, epsilon=0.1, gamma=scale",
                "Keterangan": "Base learner tanpa tuning"
            },
            {
                "Komponen": "XGBoost",
                "Parameter Utama": "n_estimators=100, max_depth=3, learning_rate=0.05",
                "Keterangan": "Meta learner tanpa tuning"
            },
            {
                "Komponen": "Stacking",
                "Parameter Utama": "cv=5, passthrough=True",
                "Keterangan": "Baseline ensemble"
            }
        ])

        st.subheader("Konfigurasi Model Iterasi 1")
        st.dataframe(df_iter1, use_container_width=True)

        st.info("""
        Catatan:
        - Iterasi ini berfungsi sebagai **titik awal perbandingan**
        - Tidak dilakukan optimasi parameter
        - Digunakan untuk mengamati efek stacking secara murni
        """)

        # ITERASI 2
        st.header("Iterasi 2 — Tuning Meta Learner")

        st.markdown("""
        **Tujuan Iterasi 2**  
        Pada iterasi ini, konfigurasi *base learner* dipertahankan sama
        dengan Iterasi 1, sementara **meta learner (XGBoost)** dilakukan
        hyperparameter tuning.

        Pendekatan ini bertujuan untuk mengisolasi dan mengevaluasi
        kontribusi meta learner terhadap peningkatan performa model.
        """)

        df_iter2 = pd.DataFrame([
            {
                "Komponen": "Random Forest",
                "Parameter Utama": "Sama dengan Iterasi 1",
                "Keterangan": "Tanpa tuning"
            },
            {
                "Komponen": "SVR",
                "Parameter Utama": "Sama dengan Iterasi 1",
                "Keterangan": "Tanpa tuning"
            },
            {
                "Komponen": "XGBoost (Meta)",
                "Parameter Utama": (
                    "n_estimators=[50,100,200], "
                    "max_depth=[2,3,4,6], "
                    "learning_rate=[0.01–0.1], "
                    "reg_alpha=[0,0.1,0.5], "
                    "reg_lambda=[0.5,1,2]"
                ),
                "Keterangan": "RandomizedSearchCV"
            },
            {
                "Komponen": "Validasi",
                "Parameter Utama": "5-Fold CV, scoring=RMSE",
                "Keterangan": "Optimasi meta learner"
            }
        ])

        st.subheader("Konfigurasi Model Iterasi 2")
        st.dataframe(df_iter2, use_container_width=True)

        st.info("""
        Catatan:
        - Base learner dikunci untuk menjaga konsistensi eksperimen
        - Tuning hanya dilakukan pada meta learner
        - Iterasi ini menunjukkan peran meta learner terhadap performa akhir
        """)

        # ITERASI 3
        st.header("Iterasi 3 — Tuning Base Learners dan Meta Learner")

        st.markdown("""
        **Tujuan Iterasi 3**  
        Iterasi ini merupakan konfigurasi **paling komprehensif**,
        di mana seluruh komponen model, baik *base learner* maupun
        *meta learner*, dilakukan hyperparameter tuning
        untuk memperoleh performa optimal.
        """)

        df_iter3 = pd.DataFrame([
            {
                "Komponen": "Random Forest",
                "Parameter Utama": (
                    "n_estimators=[100,200,300], "
                    "max_depth=[3,5,10], "
                    "min_samples_leaf=[1,2,4], "
                    "max_features=[sqrt,log2]"
                ),
                "Keterangan": "RandomizedSearchCV"
            },
            {
                "Komponen": "SVR",
                "Parameter Utama": "C=[0.1,1,10], epsilon=[0.01,0.1,0.2], gamma=[scale,auto]",
                "Keterangan": "RandomizedSearchCV"
            },
            {
                "Komponen": "XGBoost (Meta)",
                "Parameter Utama": (
                    "n_estimators=[50,100,200], "
                    "max_depth=[2,3,4,6], "
                    "learning_rate=[0.01–0.1]"
                ),
                "Keterangan": "RandomizedSearchCV"
            },
            {
                "Komponen": "Validasi",
                "Parameter Utama": "5-Fold CV, scoring=RMSE",
                "Keterangan": "Full tuning"
            }
        ])

        st.subheader("Konfigurasi Model Iterasi 3")
        st.dataframe(df_iter3, use_container_width=True)

        st.success("""
        Kesimpulan Iterasi 3:
        - Seluruh model dioptimasi secara sistematis
        - Risiko overfitting dikendalikan melalui cross-validation
        """)

        # RINGKASAN ANTAR ITERASI
        st.header("Ringkasan Perbandingan Antar Iterasi")

        df_summary = pd.DataFrame([
            {
                "Iterasi": "Iterasi 1",
                "Base Learner": "Tanpa tuning",
                "Meta Learner": "Tanpa tuning",
                "Tujuan": "Baseline"
            },
            {
                "Iterasi": "Iterasi 2",
                "Base Learner": "Tanpa tuning",
                "Meta Learner": "Tuning",
                "Tujuan": "Evaluasi kontribusi meta learner"
            },
            {
                "Iterasi": "Iterasi 3",
                "Base Learner": "Tuning",
                "Meta Learner": "Tuning",
                "Tujuan": "Model terbaik"
            }
        ])

        st.dataframe(df_summary, use_container_width=True)

        st.caption(
            "Struktur eksperimen ini dirancang untuk memastikan evaluasi model "
            "yang adil, transparan, dan dapat direplikasi."
        )
        st.divider()

        # DAFTAR FILE PKL EVALUASI
        from loaders import load_pkl_data
        all_pkl_files = [
            "eval_harian_iter1.pkl", "eval_harian_iter2.pkl", "eval_harian_iter3.pkl",
            "eval_bulanan_iter1.pkl", "eval_bulanan_iter2.pkl", "eval_bulanan_iter3.pkl"
        ]

        harian_files = sorted([f for f in all_pkl_files if f.startswith("eval_harian")])
        bulanan_files = sorted([f for f in all_pkl_files if f.startswith("eval_bulanan")])

        # ===============================
        # 🔽 DROPDOWN UNTUK PILIHAN USER
        # ===============================
        col1, col2 = st.columns([1, 1])
        with col1:
            mode = st.selectbox("Pilih Mode Analisis:", ["Harian", "Bulanan"])
        with col2:
            iterasi = st.selectbox("Pilih Iterasi:", ["Iterasi 1", "Iterasi 2", "Iterasi 3"])

        file_mapping = {
            ("Harian", "Iterasi 1"): "eval_harian_iter1.pkl",
            ("Harian", "Iterasi 2"): "eval_harian_iter2.pkl",
            ("Harian", "Iterasi 3"): "eval_harian_iter3.pkl",
            ("Bulanan", "Iterasi 1"): "eval_bulanan_iter1.pkl",
            ("Bulanan", "Iterasi 2"): "eval_bulanan_iter2.pkl",
            ("Bulanan", "Iterasi 3"): "eval_bulanan_iter3.pkl"
        }

        selected_file = file_mapping[(mode, iterasi)]
        df_eval = load_pkl_data(selected_file)

        # TAMPILKAN TABEL EVALUASI
        st.subheader(f"Tabel Evaluasi Model ({mode} - {iterasi})")
        if df_eval is not None:
            st.dataframe(df_eval, use_container_width=True, hide_index=True)
            st.caption("Tabel menampilkan data aktual vs prediksi model. Kolom error menunjukkan perbedaan prediksi dengan data nyata.")
        else:
            st.warning("Data evaluasi belum tersedia untuk kombinasi tersebut.")

        st.divider()

        # VISUALISASI PREDIKSI
        st.title("Visualisasi Hasil Prediksi (Harian & Bulanan)")
        st.markdown("""
        Grafik berikut menampilkan hasil **perbandingan prediksi model** terhadap **data aktual**.
        Gunakan dropdown di atas untuk memilih mode dan iterasi.
        """)

        grafik_file_mapping = {
            ("Harian", "Iterasi 1"): "perbandingan_harian_iter1.pkl",
            ("Harian", "Iterasi 2"): "perbandingan_harian_iter2.pkl",
            ("Harian", "Iterasi 3"): "perbandingan_harian_iter3.pkl",
            ("Bulanan", "Iterasi 1"): "perbandingan_bulanan_iter1.pkl",
            ("Bulanan", "Iterasi 2"): "perbandingan_bulanan_iter2.pkl",
            ("Bulanan", "Iterasi 3"): "perbandingan_bulanan_iter3.pkl"
        }

        selected_grafik_file = grafik_file_mapping.get((mode, iterasi))
        df_plot = load_pkl_data(selected_grafik_file)

        # ===============================
        # 🔧 FUNGSI MEMBUAT GRAFIK
        # ===============================
        def create_multi_model_chart(df_plot, title, file_name):
            """Buat grafik garis untuk RF, SVR, dan Stacking."""
            if df_plot is None or len(df_plot) <= 1:
                st.warning(f"Data tidak cukup untuk membuat grafik dari {file_name}.")
                return

            rf_keywords = ('rf', 'randomforest')
            svr_keywords = ('svr', 'supportvector')
            stacking_keywords = ('stacking', 'ensemble')
            ignore_keywords = ('error', 'selisih', 'mape', 'rmse', 'diff', 'aktual', 'actual', 'y_true')

            clean_numeric_cols = [
                col for col in df_plot.select_dtypes(include=['number']).columns
                if not any(k in col.lower() for k in ignore_keywords)
            ]

            rf_cols = [c for c in clean_numeric_cols if any(k in c.lower() for k in rf_keywords)]
            svr_cols = [c for c in clean_numeric_cols if any(k in c.lower() for k in svr_keywords)]
            stacking_cols = [c for c in clean_numeric_cols if any(k in c.lower() for k in stacking_keywords)]

            columns_to_plot, series_names = [], {}
            if rf_cols:
                columns_to_plot.append(rf_cols[0])
                series_names[rf_cols[0]] = 'Prediksi RF'
            if svr_cols:
                columns_to_plot.append(svr_cols[0])
                series_names[svr_cols[0]] = 'Prediksi SVR'
            if stacking_cols:
                columns_to_plot.append(stacking_cols[0])
                series_names[stacking_cols[0]] = 'Prediksi Stacking'

            if not columns_to_plot:
                st.error(f"Tidak ditemukan kolom prediksi model yang valid dalam {file_name}.")
                return

            df_chart = df_plot[columns_to_plot].copy()
            if not isinstance(df_chart.index, pd.DatetimeIndex):
                df_chart.index = pd.to_datetime(df_chart.index, errors='coerce')

            fig = go.Figure()
            color_map = {
                # Biru Elektrik: Terlihat stabil, teknis, dan sangat umum di dunia IT
                'Prediksi RF': '#00D4FF',       
                
                # Ungu Medium: Warna transisi yang elegan, sering dipakai di dashboard high-end
                'Prediksi SVR': '#9D50BB',      
                
                # Soft Neon Pink: Pink yang muda/cerah tapi punya kesan "Electric" (bukan pink mainan)
                # Ini sangat cocok untuk menunjukkan "Meta-Model" sebagai hasil akhir yang paling menonjol
                'Prediksi Stacking': '#FF8AD8'  
            }

            for col, label in series_names.items():
                fig.add_trace(go.Scatter(
                    x=df_chart.index.astype(str),
                    y=pd.to_numeric(df_chart[col], errors='coerce'),
                    mode='lines+markers',
                    name=label,
                    line=dict(width=3, color=color_map[label]),
                    marker=dict(size=6)
                ))

            fig.update_layout(
                title=title,
                xaxis_title='Tanggal' if mode == "Harian" else 'Bulan',
                yaxis_title='Nilai Prediksi',
                template='plotly_white',
                hovermode='x unified'
            )

            st.plotly_chart(fig, use_container_width=True)
            st.caption("Grafik menampilkan prediksi: **RF (biru)**, **SVR (ungu)**, **Stacking (pink)**.")

        # --- Tampilkan Grafik ---
        if df_plot is not None:
            st.subheader(f"Grafik Perbandingan Model ({mode} - {iterasi})")
            create_multi_model_chart(
                df_plot,
                f"Perbandingan Model {mode} - {iterasi}",
                selected_grafik_file
            )
        else:
            st.info("File grafik belum tersedia atau gagal dimuat.")

        st.divider()
        st.info("Gunakan dropdown di atas untuk mengubah mode dan iterasi, tabel dan grafik akan otomatis menyesuaikan.")

        # =========================================================
        # MENAMPILKAN SHAP SESUAI MODE
        # =========================================================
        if st.session_state.mode == "Harian":
            st.title("Ranking Global SHAP (Fitur Paling Berpengaruh)")

            data_harian = {
                "Iterasi 1": {
                    "Feature": [
                        "pred_RF", "pred_SVR", "RR_roll_mean_3", "RH_avg", "RR_lag1", "Tx", "RR_lag3",
                        "RR_roll_std_3", "ss", "Tn", "Tavg", "RR_lag7", "ff_x", "Month_sin",
                        "ddd_car_C", "Month_cos", "ddd_car_E", "ddd_car_NW", "ddd_car_NE"
                    ],
                    "MeanAbsSHAP": [
                        0.369961, 0.307085, 0.116306, 0.092874, 0.041539, 0.017468, 0.016122, 0.011935,
                        0.009003, 0.002798, 0.002284, 0.001306, 0.001053, 0.000857, 0.000775,
                        0.000759, 0.000742, 0.000617
                    ],
                    "Image": "shap harian iterasi 1.png"
                },
                "Iterasi 2": {
                    "Feature": [
                        "pred_SVR", "pred_RF", "RR_roll_mean_3", "RH_avg", "RR_lag1", "Tx", "RR_lag3", "ss",
                        "Tn", "RR_roll_std_3", "Tavg", "RR_lag7", "Month_sin", "ff_x",
                        "ddd_car_C", "Month_cos", "ddd_car_NW", "ddd_car_N", "ddd_car_W", "ddd_car_SE"
                    ],
                    "MeanAbsSHAP": [
                        0.362691, 0.340595, 0.111834, 0.067776, 0.049368, 0.033535, 0.018021, 0.018007,
                        0.014736, 0.013519, 0.009987, 0.006380, 0.003674, 0.001912, 0.001349,
                        0.001131, 0.001030, 0.000544, 0.000525, 0.000137
                    ],
                    "Image": "shap harian iterasi 2.png"
                },
                "Iterasi 3": {
                    "Feature": [
                        "pred_SVR", "RR_roll_mean_3", "pred_RF", "RR_lag1", "RR_roll_std_3", "Tn", "RH_avg",
                        "Tx", "Tavg", "ss", "RR_lag3", "RR_lag7", "Month_sin", "ff_x", "Month_cos",
                        "ddd_car_SW", "ddd_car_C", "ddd_car_E", "ddd_car_SE", "ddd_car_NW"
                    ],
                    "MeanAbsSHAP": [
                        0.554547, 0.148408, 0.107397, 0.074029, 0.032047, 0.025279, 0.020609, 0.018558,
                        0.012468, 0.011615, 0.009714, 0.007842, 0.004482, 0.003162, 0.002573,
                        0.000282, 0.000242, 0.000219, 0.000165, 0.000088
                    ],
                    "Image": "shap harian iterasi 3.png"
                }
            }

        data_bulanan = {
            "Iterasi 1": {
                "Feature": [
                    "RR_roll_mean_1", "pred_RF", "ss", "pred_SVR", "wind_sin", "Tavg", "RH_avg",
                    "RR_lag2", "ff_x", "wind_cos", "RR_roll_mean_2", "Tn", "RR_lag1", "Tx", "ff_avg"
                ],
                "MeanAbsSHAP": [
                    7.032736, 4.253529, 0.627390, 0.254886, 0.167924, 0.144375, 0.052845,
                    0.026213, 0.017272, 0.016410, 0.014398, 0.007407, 0.006738, 0.005833, 0.000000
                ],
                "Image": "shap bulanan iterasi 1.png"
            },
            "Iterasi 2": {
                "Feature": [
                    "RR_roll_mean_1", "pred_RF", "ss", "wind_sin", "pred_SVR", "RH_avg",
                    "RR_roll_mean_2", "ff_x", "RR_lag2", "wind_cos", "RR_lag1",
                    "Tn", "Tavg", "Tx", "ff_avg"
                ],
                "MeanAbsSHAP": [
                    7.160813, 4.647531, 0.934135, 0.232169, 0.231016, 0.133048,
                    0.130600, 0.089729, 0.034465, 0.030409, 0.025554,
                    0.023247, 0.011572, 0.010862, 0.000000
                ],
                "Image": "shap bulanan iterasi 2.png"
            },
            "Iterasi 3": {
                "Feature": [
                    "RR_roll_mean_1", "pred_SVR", "ss", "wind_sin", "ff_x", "Tn", "RR_lag1",
                    "Tx", "Tavg", "RH_avg", "RR_lag2", "wind cos", "ff_avg", "RR_roll_mean_2"
                ],
                "MeanAbsSHAP": [
                    7.421799, 3.186305, 2.155816, 0.974181, 0.217292, 0.109770,
                    0.035889, 0.023535, 0.023105, 0.019142, 0.018460,
                    0.007580, 0.000000, 0.000000
                ],
                "Image": "shap bulanan iterasi 3.png"
            }
        }

        # =========================================================
        # PILIH DATA
        # =========================================================
        data = data_harian[iterasi] if mode == "Harian" else data_bulanan[iterasi]

        #PENGAMAN PANJANG DATA (TANPA UBAH INTI)
        n = min(len(data["Feature"]), len(data["MeanAbsSHAP"]))

        df = pd.DataFrame({
            "Feature": data["Feature"][:n],
            "MeanAbsSHAP": data["MeanAbsSHAP"][:n]
        })

        col_left, col_right = st.columns([1, 1.3])
        with col_left:
            # TAMPILAN TABEL
            st.header(f"Global SHAP {mode} — {iterasi}")

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "MeanAbsSHAP": st.column_config.NumberColumn(
                        "Mean |SHAP|",
                        format="%.6f"
                    )
                }
            )

        with col_right:
            with st.container():
                # TAMPILAN GAMBAR
                st.subheader(f"Global SHAP {mode} — Summary Plot ({iterasi})")
                
                try:
                    # Mencari jalur file gambar secara fleksibel di seluruh folder
                    img_path = resolve_path(data["Image"])
        
                    if img_path and img_path.exists():
                        img = Image.open(img_path)
                        img.thumbnail((1200, 1000))
                        st.image(img, use_container_width=True)
                    else:
                        st.error(f"Gambar '{data['Image']}' tidak ditemukan.")
                except Exception as e:
                    st.error(f"Gagal memuat gambar '{data['Image']}': {e}")


    # Tab About: Tentang sistem
    with tab_about:
        st.markdown('<div class="card"><h3>Tentang Sistem RainPredict Semarang</h3></div>', unsafe_allow_html=True)
        st.caption("Informasi pengembang, tujuan penelitian, dan panduan penggunaan aplikasi")


        # ============================================================
        # TENTANG DEVELOPER
        # ============================================================
        st.header("Tentang Developer")

        st.markdown("""
        Website RainPredict Semarang ini dikembangkan sebagai bagian dari penyusunan skripsi oleh Sekar Ayu Mustika Ningrat yang berjudul:

        > **“PREDIKSI CURAH HUJAN DENGAN STACKING ENSEMBLE BERBASIS META-MODEL XGBOOSTREGRESSOR DAN INTERPRETABILITAS GLOBAL SHAP: STUDI KASUS KOTA SEMARANG”**

        Pengembangan website ini bertujuan untuk menerapkan hasil penelitian
        ke dalam bentuk sistem prediksi curah hujan berbasis web yang bersifat interaktif, transparan,
        dan mudah digunakan. Website ini dirancang agar dapat dimanfaatkan oleh berbagai kalangan, sebagai sarana pendukung dalam memahami dan memprediksi pola curah hujan secara lebih informatif.
        
        Untuk informasi lebih lanjut, silakan menghubungi melalui email sekarayuning8121@students.unnes.ac.id
        """)
        st.divider()

        # TUJUAN PENELITIAN / OBJECTIVE
        st.header("Tujuan Penelitian")

        st.markdown("""
        Aplikasi ini dikembangkan untuk mendukung penelitian prediksi curah hujan
        dengan pendekatan **machine learning berbasis stacking ensemble**.

        Secara umum, tujuan penelitian dan pengembangan aplikasi ini adalah:

        - Mengembangkan model prediksi curah hujan **harian dan bulanan**
        menggunakan kombinasi beberapa algoritma *machine learning*.
        - Menerapkan **Stacking Ensemble Learning**, dengan:
            - **Random Forest Regressor** dan **Support Vector Regression (SVR)** sebagai *Base learners*.
            - **XGBoost Regressor** sebagai *Meta learner*.
        - Menganalisis pengaruh **tuning hyperparameter** terhadap performa model
        melalui beberapa iterasi eksperimen.
        - Menyediakan interpretasi global model menggunakan **SHAP (SHapley Additive exPlanations)** untuk memahami kontribusi fitur
        terhadap hasil prediksi.
        - Menyajikan hasil penelitian dalam bentuk **aplikasi website interaktif**
        yang mudah dipahami dan dapat direplikasi.
        """)

        st.info("""
        Singkatnya, aplikasi ini tidak hanya menampilkan hasil prediksi,
        tetapi juga menjelaskan proses ilmiah di balik pengembangan model prediksi curah hujan.
        """)

        st.divider()

        # ============================================================
        # CARA PENGGUNAAN APLIKASI
        # ============================================================
        st.header("Cara Menggunakan Aplikasi (How to Use)")

        st.markdown("""
        Berikut adalah prosedur penggunaan aplikasi prediksi curah hujan:
        """)

        st.markdown("""
        **Langkah-langkah penggunaan:**

        1. Buka tab **Prediksi Curah Hujan** pada menu aplikasi.
        2. Unggah file dataset dalam format yang telah ditentukan (misalnya `.csv` atau `.xlsx`).
        3. Pastikan dataset berisi data iklim yang lengkap dan tersusun dengan benar.
        4. Pilih jenis prediksi:
        - **Prediksi Harian**, atau
        - **Prediksi Bulanan**.
        5. Klik tombol **Jalankan Prediksi**.
        6. Sistem akan memproses data dan menampilkan hasil prediksi sesuai dengan pilihan pengguna.
        """)

        st.warning("""
        **Perhatian Penting untuk Pengguna:**

        - Pastikan file yang diunggah memiliki **struktur kolom yang sesuai**
        dengan data pelatihan model.
        - Disarankan menggunakan **data terbaru** agar hasil prediksi lebih relevan.
        - Dataset yang tidak sesuai format atau mengandung nilai kosong yang berlebihan
        dapat menyebabkan proses prediksi gagal atau kurang akurat.
        """)

        st.success("""
        Dengan mengikuti prosedur di atas, pengguna dapat memanfaatkan aplikasi ini
        sebagai alat bantu prediksi curah hujan berbasis pembelajaran mesin.
        """)

        st.divider()

        # PENUTUP
        st.caption(
            "Aplikasi ini dikembangkan sebagai bagian dari penelitian akademik "
            "dan diharapkan dapat menjadi referensi dalam penerapan machine learning "
            "untuk bidang klimatologi dan hidrologi."
        )
