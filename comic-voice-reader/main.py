import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pytesseract
import cv2
import numpy as np
from gtts import gTTS
import playsound
import os

# Pastikan Tesseract diinstal di sistem
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Sesuaikan path

class ComicVoiceReader:
    def __init__(self, root):
        self.root = root
        self.root.title("Comic Voice Reader")
        self.root.geometry("500x300")
        self.root.config(bg="#f0f0f0")

        # Label
        tk.Label(root, text="📄 Comic Voice Reader", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)

        # Tombol Pilih Gambar
        tk.Button(root, text="Pilih Gambar Komik", command=self.select_image, 
                  font=("Arial", 12), bg="#4CAF50", fg="white", padx=20, pady=10).pack(pady=10)

        # Tombol Baca Suara
        tk.Button(root, text="Baca Suara Teks", command=self.read_aloud, 
                  font=("Arial", 12), bg="#2196F3", fg="white", padx=20, pady=10).pack(pady=10)

        # Status
        self.status_label = tk.Label(root, text="", font=("Arial", 10), bg="#f0f0f0", fg="red")
        self.status_label.pack(pady=10)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Pilih Gambar Komik",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            self.image_path = file_path
            self.status_label.config(text=f"Gambar dipilih: {os.path.basename(file_path)}", fg="green")
        else:
            self.status_label.config(text="Tidak ada gambar yang dipilih.", fg="red")

    def read_aloud(self):
        if not hasattr(self, 'image_path'):
            messagebox.showwarning("Peringatan", "Silakan pilih gambar terlebih dahulu!")
            return

        try:
            # Baca gambar
            image = cv2.imread(self.image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            # Ekstrak teks dengan OCR
            text = pytesseract.image_to_string(thresh, lang='ind+eng')  # Bahasa Indonesia + Inggris
            text = text.strip()

            if not text:
                messagebox.showinfo("Info", "Tidak ditemukan teks pada gambar.")
                return

            # Simpan teks ke file (opsional)
            with open("output/text_extracted.txt", "w", encoding="utf-8") as f:
                f.write(text)

            # Konversi ke suara
            tts = gTTS(text=text, lang='id')
            audio_file = "output/speech.mp3"
            os.makedirs("output", exist_ok=True)
            tts.save(audio_file)

            # Putar suara
            playsound.playsound(audio_file)

            self.status_label.config(text="✅ Teks berhasil dibaca!", fg="green")
            messagebox.showinfo("Sukses", "Teks berhasil diekstraksi dan dibacakan!")

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
            self.status_label.config(text=f"❌ Error: {str(e)}", fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = ComicVoiceReader(root)
    root.mainloop()
