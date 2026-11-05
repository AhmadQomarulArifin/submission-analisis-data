import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Mengatur tema dasar grafik agar serasi dengan notebook
sns.set(style='darkgrid')

# 1. Konfigurasi Halaman Utama Dashboard
st.set_page_config(page_title="E-Commerce Insights Dashboard", page_icon="📊", layout="wide")
st.title('E-Commerce Multi-Dimensional Performance Dashboard 📊')
st.markdown("Aplikasi pelaporan interaktif untuk memantau performa penjualan produk, karakteristik pelanggan (RFM), dan demografi wilayah sepanjang tahun 2017.")

# 2. Fungsi Memuat Dataset Bersih dari Cache
@st.cache_data
def load_clean_data():
    df = pd.read_csv("master_clean_data.csv")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

master_df = load_clean_data()

# 3. Membuat Komponen Filter Rentang Waktu di Sidebar
min_date = master_df["order_purchase_timestamp"].min().date()
max_date = master_df["order_purchase_timestamp"].max().date()

with st.sidebar:
    st.image("https://github.com", width=200)
    st.markdown("### Filter Rentang Analisis")
    date_range = st.date_input(
        label='Tentukan Rentang Waktu Transaksi:',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Memastikan user sudah memilih sepasang tanggal (Mulai & Selesai) sebelum memfilter DataFrame
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = master_df[(master_df["order_purchase_timestamp"].dt.date >= start_date) & 
                            (master_df["order_purchase_timestamp"].dt.date <= end_date)]
else:
    # Jika user baru mengeklik satu tanggal, gunakan seluruh data penuh sementara agar tidak crash
    filtered_df = master_df.copy()

# 4. Membuat Rangkuman Metrik Utama (KPI) di Bagian Atas
st.markdown("### Ringkasan Performa Bisnis")
total_revenue = filtered_df.price.sum()
total_orders = filtered_df.order_id.nunique()

kpi_col1, kpi_col2 = st.columns(2)
with kpi_col1:
    st.metric("Total Omset Bisnis (Revenue)", value=format_currency(total_revenue, "USD", locale="en_US"))
with kpi_col2:
    st.metric("Total Transaksi Sukses", value=f"{total_orders:,} Orders")

st.markdown("---")

# 5. LAYOUT TAB UTAMA (Menggunakan Kombinasi Teks Emoji yang Kompatibel)
tab1, tab2, tab3 = st.tabs([
    "增 Performa Finansial Produk", 
    "👥 Segmentasi Perilaku Pelanggan (RFM)", 
    "🌍 Analisis Geospasial Wilayah"
])

# --- TAB 1: JAWABAN PERTANYAAN BISNIS 1 ---
with tab1:
    st.header("Analisis Performa Pendapatan Kategori Produk")
    st.markdown("Menampilkan komoditas barang dengan performa pendapatan tertinggi (Top) dan terendah (Bottom) untuk optimasi inventaris gudang.")
    
    # Hitung revenue per kategori
    revenue_by_cat = filtered_df.groupby("product_category_name_english")["price"].sum().sort_values(ascending=False).reset_index()
    
    # Menentukan palet warna kontras fungsional (Prinsip Integritas Desain)
    colors_best = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    colors_worst = ["#FF6B6B", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
    # Membuat 2 kolom visualisasi berdampingan (Top vs Bottom)
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        st.markdown("#### 5 Kategori Produk Unggulan Teratas")
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        sns.barplot(x="price", y="product_category_name_english", data=revenue_by_cat.head(5), hue="product_category_name_english", palette=colors_best, legend=False)
        ax1.set_xlabel("Total Revenue (USD)")
        ax1.set_ylabel(None)
        st.pyplot(fig1)
        
    with col_graph2:
        st.markdown("#### 5 Kategori Produk dengan Pendapatan Terendah")
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        sns.barplot(x="price", y="product_category_name_english", data=revenue_by_cat.tail(5).sort_values(by="price", ascending=True), hue="product_category_name_english", palette=colors_worst, legend=False)
        ax2.set_xlabel("Total Revenue (USD)")
        ax2.set_ylabel(None)
        st.pyplot(fig2)

# --- TAB 2: JAWABAN PERTANYAAN BISNIS 2 ---
with tab2:
    st.header("Karakteristik Pelanggan Menggunakan Metode RFM")
    st.markdown("Mengelompokkan profil pembeli secara mandiri berdasarkan total kontribusi finansial belanja kuartal terakhir.")
    
    # Pemrosesan Parameter RFM Real-time
    recent_date = filtered_df["order_purchase_timestamp"].max()
    rfm_df = filtered_df.groupby(by="customer_unique_id", as_index=False).agg({
        "order_purchase_timestamp": "max",
        "order_id": "nunique",
        "price": "sum"
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    
    # Menghitung Kluster Manual Spender
    def assign_segment(value):
        if value > 200: return "High-Spender Customer"
        elif value > 70: return "Medium-Spender Customer"
        else: return "Low-Spender Customer"
    rfm_df["customer_segment"] = rfm_df["monetary"].apply(assign_segment)
    
    # Urutan visualisasi kelompok pelanggan
    segment_counts = rfm_df["customer_segment"].value_counts().reset_index()
    segment_counts.columns = ["customer_segment", "count"]
    
    fig3, ax3 = plt.subplots(figsize=(12, 4))
    sns.barplot(x="count", y="customer_segment", data=segment_counts, hue="customer_segment", palette="coolwarm", legend=False)
    ax3.set_xlabel("Jumlah Pelanggan Unik")
    ax3.set_ylabel(None)
    st.pyplot(fig3)

# --- TAB 3: JAWABAN ANALISIS LANJUTAN (GEOSPATIAL) ---
with tab3:
    st.header("Analisis Distribusi Geospasial Konsumen")
    st.markdown("Menganalisis sebaran kepadatan demografi lokasi geografis pengguna unik di setiap wilayah negara bagian.")
    
    # Kalkulasi jumlah pelanggan per negara bagian
    state_customer = filtered_df.groupby("customer_state")["customer_unique_id"].nunique().sort_values(ascending=False).reset_index()
    state_customer.columns = ["customer_state", "customer_count"]
    
    fig4, ax4 = plt.subplots(figsize=(12, 5))
    sns.barplot(x="customer_count", y="customer_state", data=state_customer.head(10), hue="customer_state", palette="viridis", legend=False)
    ax4.set_title("10 Negara Bagian dengan Konsentrasi Pasar Terbesar", fontsize=12, weight="bold")
    ax4.set_xlabel("Jumlah Pelanggan Unik")
    ax4.set_ylabel("Kode Wilayah")
    st.pyplot(fig4)

st.caption("Copyright © Ahmad Qomarul Arifin 2026 | Submission Dicoding Fundamental Analisis Data")
