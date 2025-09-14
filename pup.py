#!/usr/bin/env python3

from flask import Flask, request, render_template_string
import random
from datetime import datetime
import os

# 1. Inisialisasi Aplikasi Flask
app = Flask(__name__)

# 2. Lokasi File Log (Server-side)
LOG_FILE = "riwayat_web_upload.log" 

# 3. Template HTML (CSS dan HTML dalam satu string)
# === UI TELAH DIROMBAK TOTAL UNTUK TAMPILAN LEBIH MODERN ===
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alat Acak Kelompok oleh Zaviron</title>
    <style>
        /* === GLOBAL RESET & FONT MODERN === */
        :root {
            --primary-color: #007aff;
            --primary-light: #e6f2ff;
            --border-color: #dbe0e4;
            --bg-light: #f4f7f6;
            --bg-white: #ffffff;
            --text-dark: #2c3e50;
            --text-light: #5a7184;
            --success-color: #28a745;
            --error-color: #dc3545;
            --error-bg: #fdf2f2;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 2rem 1rem;
            background-color: var(--bg-light);
            color: var(--text-dark);
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }

        /* === WADAH UTAMA === */
        .container {
            width: 100%;
            max-width: 700px;
            background-color: var(--bg-white);
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.07);
            border: 1px solid var(--border-color);
            overflow: hidden; /* Agar border-radius rapi */
        }

        /* === HEADER ALAT === */
        .tool-header {
            padding: 1.5rem 2rem;
            border-bottom: 1px solid var(--border-color);
            background-color: #fafbfb;
        }
        .tool-header h1 {
            margin: 0 0 0.25rem 0;
            color: var(--text-dark);
            font-size: 1.75rem;
        }
        .tool-header p {
            margin: 0;
            color: var(--text-light);
            font-size: 1rem;
        }
        
        /* === FORM STYLING === */
        form {
            padding: 2rem;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: var(--text-dark);
        }

        input[type="text"], input[type="number"] {
            width: 100%;
            padding: 0.85rem 1rem;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-size: 1rem;
            font-family: inherit;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        input[type="text"]:focus, input[type="number"]:focus, input[type="file"]:focus-within {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px var(--primary-light);
        }

        /* === STYLING INPUT FILE YANG LEBIH BAIK === */
        input[type="file"] {
            width: 100%;
            font-size: 0.95rem;
        }
        /* Menggunakan ::file-selector-button untuk styling tombol internal */
        input[type="file"]::file-selector-button {
            margin-right: 1rem;
            border: none;
            padding: 0.75rem 1rem;
            border-radius: 6px;
            background-color: var(--primary-light);
            color: var(--primary-color);
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        input[type="file"]::file-selector-button:hover {
            background-color: #d4e8ff;
        }

        /* === TOMBOL SUBMIT UTAMA === */
        input[type="submit"] {
            background-color: var(--primary-color);
            color: white;
            padding: 0.9rem 1.5rem;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.1rem;
            font-weight: 600;
            width: 100%;
            margin-top: 1rem;
            transition: background-color 0.2s, transform 0.1s;
        }
        input[type="submit"]:hover {
            background-color: #005ecb;
        }
        input[type="submit"]:active {
            transform: scale(0.99);
        }

        /* === KARTU HASIL & ERROR === */
        .alert {
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin: 2rem 2rem 0 2rem;
            border: 1px solid transparent;
            font-weight: 500;
        }
        .alert-error {
            color: #721c24;
            background-color: var(--error-bg);
            border-color: #f5c6cb;
        }

        #hasil {
            padding: 0 2rem 2rem 2rem;
        }
        #hasil h2 {
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
            color: var(--text-dark);
        }
        #hasil h2 .filename {
            color: var(--success-color);
            font-weight: 600;
        }

        .kelompok-card {
            background-color: #fcfcfc;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        .kelompok-card h3 {
            margin-top: 0;
            margin-bottom: 0.75rem;
            color: var(--primary-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .kelompok-card h3 .anggota-count {
            font-size: 0.9rem;
            font-weight: 500;
            padding: 0.25rem 0.6rem;
            background-color: var(--primary-light);
            color: var(--primary-color);
            border-radius: 1rem;
        }
        .kelompok-card ul {
            padding-left: 1.5rem;
            margin: 0;
            list-style-type: disc;
        }
         .kelompok-card li {
            padding: 0.25rem 0;
            color: var(--text-light);
         }

        /* === LINK FOOTER & COPYRIGHT === */
        .footer-links {
            text-align: center;
            margin-top: 2rem;
            font-size: 0.95rem;
        }
        .footer-links a {
            color: var(--primary-color);
            text-decoration: none;
            font-weight: 500;
        }
        .footer-links a:hover {
            text-decoration: underline;
        }
        
        footer {
            margin-top: 1rem;
            text-align: center;
            color: #999;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="tool-header">
            <h1>🛠️ Alat Acak Kelompok</h1>
            <p>Upload file .txt berisi daftar nama untuk dibagi secara adil.</p>
        </header>

        {% if error %}
            <div class="alert alert-error">{{ error }}</div>
        {% endif %}

        <form method="POST" action="/" enctype="multipart/form-data">
            <div class="form-group">
                <label for="name_file">1. Upload File Nama (.txt)</label>
                <input type="file" id="name_file" name="name_file" accept=".txt" required>
            </div>

            <div class="form-group">
                <label for="group_count">2. Jumlah Kelompok</label>
                <input type="number" id="group_count" name="group_count" min="1" required placeholder="Contoh: 3">
            </div>

            <div class="form-group">
                <label for="group_names">3. Nama Kelompok (Pisahkan dengan koma)</label>
                <input type="text" id="group_names" name="group_names" required placeholder="Contoh: Tim Merah, Tim Biru, Tim Hijau">
            </div>

            <input type="submit" value="Acak Sekarang!">
        </form>

        {% if results %}
            <div id="hasil">
                <h2>🎉 Hasil Pengacakan (File: <span class="filename">{{ filename }}</span>)</h2>
                {% for group in results %}
                    <div class="kelompok-card">
                        <h3>
                            {{ group.nama_grup }} 
                            <span class="anggota-count">{{ group.anggota|length }} Anggota</span>
                        </h3>
                        <ul>
                            {% for member in group.anggota %}
                                <li>{{ member }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>

    <div class="footer-links">
        <a href="/log">Lihat Riwayat Pemakaian</a>
    </div>

    <footer>
        <p>&copy; 2024. Tools ini buatan Zaviron.</p>
    </footer>
    
</body>
</html>
"""

# 4. Fungsi untuk menulis Log (Dimodifikasi untuk menyertakan nama file)
def tulis_log(hasil_grup, total_nama, nama_file_sumber):
    try:
        with open(LOG_FILE, 'a') as log:
            ts = datetime.now().strftime("%A, %d %B %Y - %H:%M:%S")
            log.write("==================================================\n")
            log.write(f"LOG APLIKASI WEB PADA: {ts}\n")
            log.write(f"File Sumber: {nama_file_sumber} ({total_nama} nama)\n") # Log nama file
            log.write(f"Dibagi menjadi: {len(hasil_grup)} kelompok.\n")
            log.write("--------------------------------------------------\n")
            
            for grup in hasil_grup:
                log.write(f"[ KELOMPOK: {grup['nama_grup']} ] ({len(grup['anggota'])} Anggota)\n")
                for nama in grup['anggota']:
                    log.write(f"  -> {nama}\n")
            
            log.write("==================================================\n\n")
    except Exception as e:
        print(f"Gagal menulis log: {e}")

# 5. Rute Utama (/) - Menampilkan form (GET) dan memproses hasil (POST)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # --- BAGIAN MEMBACA FILE UPLOAD (TETAP SAMA) ---
            
            if 'name_file' not in request.files:
                return render_template_string(HTML_TEMPLATE, results=None, error="Tidak ada file yang terdeteksi di request.")
            
            file = request.files['name_file']

            if file.filename == '':
                return render_template_string(HTML_TEMPLATE, results=None, error="Silakan pilih file untuk di-upload.")

            try:
                file_content_bytes = file.read()
                names_list_raw = file_content_bytes.decode('utf-8')
            except UnicodeDecodeError:
                return render_template_string(HTML_TEMPLATE, results=None, error="Gagal membaca file. Pastikan file adalah format teks (plain text) UTF-8.")

            # --- AKHIR BAGIAN FILE ---

            group_count_raw = request.form['group_count']
            group_names_raw = request.form['group_names']

            daftar_nama = [line.strip() for line in names_list_raw.splitlines() if line.strip()]
            nama_kelompok = [name.strip() for name in group_names_raw.split(',') if name.strip()]
            
            if not daftar_nama:
                return render_template_string(HTML_TEMPLATE, results=None, error="File .txt yang di-upload kosong atau tidak berisi nama.")

            jumlah_kelompok = int(group_count_raw)

            if jumlah_kelompok != len(nama_kelompok):
                error_msg = f"ERROR: Anda memasukkan {jumlah_kelompok} kelompok, tapi hanya menyediakan {len(nama_kelompok)} nama kelompok. Keduanya harus sama."
                return render_template_string(HTML_TEMPLATE, results=None, error=error_msg)

            # --- Inti Logika Acak (TETAP SAMA) ---
            random.shuffle(daftar_nama)
            total_nama = len(daftar_nama)
            ukuran_dasar = total_nama // jumlah_kelompok
            sisa = total_nama % jumlah_kelompok
            
            hasil_akhir = []
            idx_nama = 0

            for nama_grup_saat_ini in nama_kelompok:
                anggota_grup_ini = ukuran_dasar
                if sisa > 0:
                    anggota_grup_ini += 1
                    sisa -= 1
                
                anggota_slice = daftar_nama[idx_nama : idx_nama + anggota_grup_ini]
                
                hasil_akhir.append({
                    'nama_grup': nama_grup_saat_ini,
                    'anggota': anggota_slice
                })
                
                idx_nama += anggota_grup_ini
            
            tulis_log(hasil_akhir, total_nama, file.filename)

            return render_template_string(HTML_TEMPLATE, results=hasil_akhir, error=None, filename=file.filename)

        except ValueError:
            return render_template_string(HTML_TEMPLATE, results=None, error="ERROR: Jumlah kelompok harus berupa angka yang valid.")
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, results=None, error=f"Terjadi kesalahan: {e}")

    # Metode GET
    return render_template_string(HTML_TEMPLATE, results=None, error=None)


# 6. Rute untuk Melihat Log (/log) - Diberi sedikit style agar konsisten
@app.route('/log')
def view_log():
    log_style = """
    <style>
        body { font-family: sans-serif; margin: 2rem; background: #f4f7f6; }
        pre { 
            background: #fff; border: 1px solid #ddd; padding: 1.5rem; 
            border-radius: 8px; white-space: pre-wrap; word-wrap: break-word; 
        }
        a { font-weight: bold; color: #007aff; }
    </style>
    """
    log_content = f"<!DOCTYPE html><html><head><title>Log</title>{log_style}</head><body>"
    log_content += f"<h2>Riwayat Pengacakan (dari {LOG_FILE})</h2>"
    log_content += '<a href="/"><< Kembali ke Alat Acak</a><hr>'
    try:
        with open(LOG_FILE, 'r') as f:
            log_content += f"<pre>{f.read()}</pre>"
    except FileNotFoundError:
        log_content += "<p>File log belum ada. Silakan gunakan alatnya terlebih dahulu.</p>"
    
    log_content += '<hr><a href="/"><< Kembali ke Alat Acak</a></body></html>'
    return log_content


# 7. Jalankan Aplikasi
if __name__ == "__main__":
    print(f"{'='*30}\nServer Flask berjalan!")
    print(f"Buka browser Anda (Chrome/Firefox) dan akses:\nhttp://localhost:5000\natau\nhttp://127.0.0.1:5000\n{'='*30}")
    # debug=False adalah default yang lebih aman untuk "produksi" ringan
    app.run(debug=False, host='0.0.0.0', port=5000)

