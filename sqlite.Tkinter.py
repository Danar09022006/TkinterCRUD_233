import sqlite3
import tkinter as tk
import tkinter.messagebox as ms

def create_database():
    """Membuat database dan tabel jika belum ada"""
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

def submit_nilai():
    """Mengambil data, melakukan prediksi, dan menyimpan ke SQLite"""
    try:
        # 1. Ambil data
        nama = entry_nama.get()
        biologi = int(entry_biologi.get())
        fisika = int(entry_fisika.get())
        inggris = int(entry_inggris.get())

        # 2. Logika Prediksi
        if biologi > fisika and biologi > inggris:
            prediksi = "Kedokteran"
        elif fisika > biologi and fisika > inggris:
            prediksi = "Teknik"
        elif inggris > biologi and inggris > fisika:
            prediksi = "Bahasa"
        else:
            prediksi = "Belum dapat diprediksi (Nilai sama)"

        # 3. Update Label Output
        output_var.set(f"Hasil Prediksi: {prediksi}")

        # 4. Simpan ke Database SQLite
        conn = sqlite3.connect('nilai_siswa.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
            VALUES (?, ?, ?, ?, ?)
        ''', (nama, biologi, fisika, inggris, prediksi))
        conn.commit()
        conn.close()

        # 5. Pesan Sukses
        ms.showinfo("Sukses", "Data berhasil disimpan ke Database!")
        # 6. Mengatasi 
    except ValueError:
        ms.showerror("Error", "Pastikan nilai Biologi, Fisika, dan Inggris berupa angka!")


# Membuat database
create_database()

top = tk.Tk()
top.title("Aplikasi Prediksi Prodi")
top.geometry("400x450")
top.configure(bg="#01fbdd")

output_var = tk.StringVar(value="Luaran Hasil Prediksi")

# Label Judul
judul_label = tk.Label(top, text="Input Nilai Siswa", bg="#01fbdd", font=("Arial", 12, "bold"))
judul_label.pack(pady=10)

# Frame untuk Form Input
frame_form = tk.Frame(top, bg="#01fbdd")
frame_form.pack(pady=10, padx=20)


# 1. Nama Siswa
tk.Label(frame_form, text="Nama Siswa:", bg="#ffffff", font=("Arial", 10)).grid(row=0, column=0, pady=5, sticky="w")
entry_nama = tk.Entry(frame_form, bd=3, relief="sunken")
entry_nama.grid(row=0, column=1, pady=5, padx=10)

# 2. Nilai Biologi
tk.Label(frame_form, text="Nilai Biologi:", bg="#ffffff", font=("Arial", 10)).grid(row=1, column=0, pady=5, sticky="w")
entry_biologi = tk.Entry(frame_form, bd=3, relief="sunken")
entry_biologi.grid(row=1, column=1, pady=5, padx=10)

# 3. Nilai Fisika
tk.Label(frame_form, text="Nilai Fisika:", bg="#ffffff", font=("Arial", 10)).grid(row=2, column=0, pady=5, sticky="w")
entry_fisika = tk.Entry(frame_form, bd=3, relief="sunken")
entry_fisika.grid(row=2, column=1, pady=5, padx=10)

# 4. Nilai Inggris
tk.Label(frame_form, text="Nilai Inggris:", bg="#ffffff", font=("Arial", 10)).grid(row=3, column=0, pady=5, sticky="w")
entry_inggris = tk.Entry(frame_form, bd=3, relief="sunken")
entry_inggris.grid(row=3, column=1, pady=5, padx=10)


# Tombol Submit_nilai
btn_prediksi = tk.Button(
    top, 
    text="Submit & Prediksi", 
    command=submit_nilai, 
    font=("Arial", 10, "bold"),
    bg="#ba08eb",  
    fg="white",     
    relief="raised",
    bd=3            
)
btn_prediksi.pack(pady=20)

# Output Hasil
label_output = tk.Label(
    top,
    textvariable=output_var,
    bd=3,                   
    relief="sunken",        
    font=("Arial", 10, "italic"),
    bg="#75948f",
    width=40,                
    anchor="center",              
    padx=5                   
)
label_output.pack(pady=10, padx=20)

top.mainloop()