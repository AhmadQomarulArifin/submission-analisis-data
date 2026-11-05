# Proyek Analisis Data E-Commerce 2017 📊

Proyek akhir ini merupakan aplikasi pelaporan multi-dimensi interaktif yang menganalisis performa pendapatan produk, karakteristik pelanggan melalui analisis RFM, serta segmentasi regional (Geospatial Analysis) berdasarkan E-Commerce Public Dataset.

## Struktur Direktori
```text
submission
├── dashboard
│   ├── dashboard.py
│   └── master_clean_data.csv
├── data
│   ├── customers_dataset.csv
│   ├── order_items_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   └── products_dataset.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Langkah Menjalankan Dashboard di Local Perangkat Anda

### 1. Menginstal Dependency (Library Pendukung)
Pastikan path terminal mengarah ke direktori proyek ini, lalu pasang pustaka wajib menggunakan perintah:
```bash
pip install -r requirements.txt
```

### 2. Meluncurkan Aplikasi Dashboard Streamlit
Masuk ke dalam folder dashboard, kemudian jalankan berkas python:
```bash
cd dashboard
streamlit run dashboard.py
```
