import sqlite3
import tkinter as tk
import tkinter.messagebox as ms

def create_database():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    conn.commit()
    conn.close()

def hitung_prediksi(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Belum dapat diprediksi (Nilai sama)"

# --- FUNGSI PENCARIAN BY ID ---
def cari_by_id():
    """Mencari data berdasarkan ID"""
    id_siswa = entry_id.get()
    
    if not id_siswa:
        ms.showwarning("Peringatan", "Masukkan ID Siswa untuk mencari!")
        return

    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    # Pilih nama dan nilai berdasarkan ID
    cursor.execute('SELECT nama_siswa, biologi, fisika, inggris, prediksi_fakultas FROM nilai_siswa WHERE id=?', (id_siswa,))
    data = cursor.fetchone()
    conn.close()

    if data:
        # Data ditemukan (nama, bio, fis, ing, pred)
        nama, biologi, fisika, inggris, prediksi = data
        
        # Bersihkan form lama
        entry_nama.delete(0, tk.END)
        entry_biologi.delete(0, tk.END)
        entry_fisika.delete(0, tk.END)
        entry_inggris.delete(0, tk.END)

        # Isi form dengan data dari database
        entry_nama.insert(0, nama)
        entry_biologi.insert(0, biologi)
        entry_fisika.insert(0, fisika)
        entry_inggris.insert(0, inggris)

        output_var.set(f"ID {id_siswa} Ditemukan: {prediksi}")
    else:
        ms.showerror("Error", f"ID {id_siswa} tidak ditemukan di database.")

def submit_nilai():
    """Menyimpan data baru (ID otomatis dibuat)"""
    try:
        nama = entry_nama.get()
        biologi = int(entry_biologi.get())
        fisika = int(entry_fisika.get())
        inggris = int(entry_inggris.get())

        if not nama:
            ms.showerror("Error", "Nama siswa tidak boleh kosong!")
            return

        prediksi = hitung_prediksi(biologi, fisika, inggris)
        
        conn = sqlite3.connect('nilai_siswa.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
            VALUES (?, ?, ?, ?, ?)
        ''', (nama, biologi, fisika, inggris, prediksi))
        conn.commit()
        
        # Ambil ID yang baru saja dibuat untuk info user
        last_id = cursor.lastrowid
        conn.close()

        output_var.set(f"Tersimpan. ID Baru: {last_id}")
        ms.showinfo("Sukses", f"Data berhasil disimpan!\nID Siswa Anda adalah: {last_id}")
        
        # Kosongkan ID input agar tidak bingung
        entry_id.delete(0, tk.END) 
        
    except ValueError:
        ms.showerror("Error", "Pastikan nilai berupa angka!")

def update_nilai():
    """Update data berdasarkan ID"""
    try:
        id_siswa = entry_id.get()
        nama = entry_nama.get() # Nama bisa diedit sekarang
        biologi = int(entry_biologi.get())
        fisika = int(entry_fisika.get())
        inggris = int(entry_inggris.get())

        if not id_siswa:
            ms.showerror("Error", "Masukkan ID Siswa yang akan diupdate!")
            return

        prediksi = hitung_prediksi(biologi, fisika, inggris)

        conn = sqlite3.connect('nilai_siswa.db')
        cursor = conn.cursor()
        # Update SEMUA data (termasuk nama) dimana ID cocok
        cursor.execute('''
            UPDATE nilai_siswa 
            SET nama_siswa=?, biologi=?, fisika=?, inggris=?, prediksi_fakultas=? 
            WHERE id=?
        ''', (nama, biologi, fisika, inggris, prediksi, id_siswa))
        
        if cursor.rowcount > 0:
            conn.commit()
            output_var.set(f"ID {id_siswa} Terupdate: {prediksi}")
            ms.showinfo("Sukses", "Data berhasil diperbarui!")
        else:
            ms.showwarning("Gagal", "ID tidak ditemukan.")
        conn.close()

    except ValueError:
        ms.showerror("Error", "Pastikan nilai berupa angka!")

def delete_nilai():
    """Menghapus data berdasarkan ID"""
    id_siswa = entry_id.get()
    
    if not id_siswa:
        ms.showerror("Error", "Masukkan ID Siswa yang akan dihapus!")
        return

    if ms.askyesno("Konfirmasi", f"Yakin ingin menghapus data dengan ID {id_siswa}?"):
        conn = sqlite3.connect('nilai_siswa.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM nilai_siswa WHERE id=?', (id_siswa,))
        
        if cursor.rowcount > 0:
            conn.commit()
            output_var.set("Data Terhapus")
            # Bersihkan form
            entry_id.delete(0, tk.END)
            entry_nama.delete(0, tk.END)
            entry_biologi.delete(0, tk.END)
            entry_fisika.delete(0, tk.END)
            entry_inggris.delete(0, tk.END)
            ms.showinfo("Sukses", "Data berhasil dihapus!")
        else:
            ms.showwarning("Gagal", "ID tidak ditemukan.")
        conn.close()

# Membuat database
create_database()

# Setup GUI
top = tk.Tk()
top.title("Aplikasi Prediksi Prodi")
top.geometry("500x550")
top.configure(bg="#3b2638")

output_var = tk.StringVar(value="Siap Menerima Data")

tk.Label(top, text="Input Nilai Siswa", bg="#ffffff", font=("Arial", 12, "bold")).pack(pady=10)

frame_form = tk.Frame(top, bg="#3b2638")
frame_form.pack(pady=5, padx=20)

# --- BARIS 0: ID & TOMBOL CARI (Penting) ---
tk.Label(frame_form, text="ID Siswa:", bg="#ffffff", font=("Arial", 10, "bold")).grid(row=0, column=0, pady=5, sticky="w")
entry_id = tk.Entry(frame_form, bd=3, relief="sunken", width=10) # Lebih pendek karena cuma angka
entry_id.grid(row=0, column=1, pady=5, padx=10, sticky="w")

btn_cari = tk.Button(frame_form, text="Cari ID", command=cari_by_id, bg="#2196F3", fg="white", font=("Arial", 9, "bold"))
btn_cari.grid(row=0, column=2, padx=5, sticky="w")

# --- BARIS 1 dst: Data Siswa ---
# 1. Nama Siswa
tk.Label(frame_form, text="Nama Siswa:", bg="#ffffff", font=("Arial", 10)).grid(row=1, column=0, pady=5, sticky="w")
entry_nama = tk.Entry(frame_form, bd=3, relief="sunken")
entry_nama.grid(row=1, column=1, pady=5, padx=10)

# 2. Nilai Biologi
tk.Label(frame_form, text="Nilai Biologi:", bg="#ffffff", font=("Arial", 10)).grid(row=2, column=0, pady=5, sticky="w")
entry_biologi = tk.Entry(frame_form, bd=3, relief="sunken")
entry_biologi.grid(row=2, column=1, pady=5, padx=10)

# 3. Nilai Fisika
tk.Label(frame_form, text="Nilai Fisika:", bg="#ffffff", font=("Arial", 10)).grid(row=3, column=0, pady=5, sticky="w")
entry_fisika = tk.Entry(frame_form, bd=3, relief="sunken")
entry_fisika.grid(row=3, column=1, pady=5, padx=10)

# 4. Nilai Inggris
tk.Label(frame_form, text="Nilai Inggris:", bg="#ffffff", font=("Arial", 10)).grid(row=4, column=0, pady=5, sticky="w")
entry_inggris = tk.Entry(frame_form, bd=3, relief="sunken")
entry_inggris.grid(row=4, column=1, pady=5, padx=10)

# Frame Tombol Aksi
frame_tombol = tk.Frame(top, bg="#3b2638")
frame_tombol.pack(pady=20)

# Tombol Simpan
tk.Button(frame_tombol, text="Simpan Baru", command=submit_nilai, font=("Arial", 10, "bold"), 
          bg="#ba08eb", fg="white", width=12).grid(row=0, column=0, padx=5)

# Tombol Update
tk.Button(frame_tombol, text="Update by ID", command=update_nilai, font=("Arial", 10, "bold"), 
          bg="#FFA500", fg="white", width=12).grid(row=0, column=1, padx=5)

# Tombol Delete
tk.Button(frame_tombol, text="Delete by ID", command=delete_nilai, font=("Arial", 10, "bold"), 
          bg="#FF0000", fg="white", width=12).grid(row=0, column=2, padx=5)

# Output Label
label_output = tk.Label(top, textvariable=output_var, bd=3, relief="sunken", 
                        font=("Arial", 10, "italic"), bg="#75948f", width=50, padx=5)
label_output.pack(pady=10)

top.mainloop()