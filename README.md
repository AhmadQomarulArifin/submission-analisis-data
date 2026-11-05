## Langkah Menjalankan Dashboard di Local Perangkat Anda

### 1. Membuat dan Mengaktifkan Environment Terisolasi (Virtual Environment)
Pastikan posisi terminal atau Command Prompt (CMD) Anda sudah diarahkan masuk ke dalam direktori utama proyek `submission`. Jalankan perintah berikut berdasarkan sistem operasi perangkat Anda:

- **Windows (Command Prompt):**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

- **Mac / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
*Catatan: Jika berhasil aktif, Anda akan melihat tanda penanda `(venv)` muncul di sisi paling kiri baris perintah kursor terminal Anda.*

### 2. Menginstal Dependency (Library Pendukung)
Setelah virtual environment dalam kondisi aktif, pasang seluruh pustaka wajib yang tercatat di dalam proyek ini menggunakan perintah:
```bash
pip install -r requirements.txt
```

### 3. Meluncurkan Aplikasi Dashboard Streamlit
Pindahkan jalur direktori masuk ke dalam folder dashboard, kemudian luncurkan aplikasi web interaktif Anda:
```bash
cd dashboard
streamlit run dashboard.py
```
