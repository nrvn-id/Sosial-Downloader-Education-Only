import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import yt_dlp
import os
import threading
import re
import time
import subprocess
import imageio_ffmpeg

class DesktopDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Downloader HD Pro (Mute & Enhance)")
        self.root.geometry("650x800")
        
        self.save_path = ""
        # Mencari path ffmpeg otomatis dari library imageio-ffmpeg
        try:
            self.ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        except:
            self.ffmpeg_path = "ffmpeg"

        # --- UI LAYOUT ---
        tk.Label(root, text="SOCIAL VIDEO DOWNLOADER HD", font=("Arial", 16, "bold"), fg="#2c3e50").pack(pady=15)

        # 1. Folder Selection
        frame_folder = tk.LabelFrame(root, text=" 1. Lokasi Penyimpanan ", padx=10, pady=10)
        frame_folder.pack(padx=20, fill="x", pady=5)
        
        tk.Button(frame_folder, text="Pilih Folder", command=self.browse_folder, bg="#ecf0f1").pack(side="left", padx=5)
        self.label_path = tk.Label(frame_folder, text="LOKASI BELUM DIPILIH!", fg="red", font=("Arial", 9, "bold"))
        self.label_path.pack(side="left", fill="x")

        # 2. Settings
        frame_settings = tk.LabelFrame(root, text=" 2. Konfigurasi Keamanan & Efek ", padx=10, pady=10)
        frame_settings.pack(padx=20, fill="x", pady=5)
        
        tk.Label(frame_settings, text="Jeda Antar Video (Detik):").grid(row=0, column=0, sticky="w")
        self.spin_delay = tk.Spinbox(frame_settings, from_=1, to=60, width=5)
        self.spin_delay.delete(0, "end")
        self.spin_delay.insert(0, "6")
        self.spin_delay.grid(row=0, column=1, padx=5, sticky="w")

        self.var_enhance = tk.BooleanVar(value=True)
        tk.Checkbutton(frame_settings, text="HD Enhance (Sharpen/Vivid)", variable=self.var_enhance).grid(row=0, column=2, sticky="w")

        self.var_mute = tk.BooleanVar(value=False)
        tk.Checkbutton(frame_settings, text="Mute Video (Hapus Suara)", variable=self.var_mute, fg="#c0392b").grid(row=1, column=2, sticky="w")

        # 3. Input Area Tabs
        self.tabs_frame = tk.Frame(root)
        self.tabs_frame.pack(pady=10)
        
        self.mode = "single"
        self.btn_single = tk.Button(self.tabs_frame, text="Single Download", command=self.show_single, width=18, relief="sunken")
        self.btn_single.grid(row=0, column=0)
        self.btn_multi = tk.Button(self.tabs_frame, text="Multi (Maks 10)", command=self.show_multi, width=18)
        self.btn_multi.grid(row=0, column=1)

        self.input_frame = tk.Frame(root, padx=20)
        self.input_frame.pack(fill="x")
        self.entry_single = tk.Entry(self.input_frame, font=("Arial", 10))
        self.entry_single.pack(fill="x", pady=5)
        self.text_multi = tk.Text(self.input_frame, height=6, font=("Arial", 9))

        # 4. Log Box
        tk.Label(root, text="Proses & Log Aktivitas:", font=("Arial", 9, "bold")).pack(anchor="w", padx=20, pady=(10,0))
        self.log_box = tk.Text(root, height=12, state="disabled", bg="#2f3640", fg="#f5f6fa", font=("Consolas", 8))
        self.log_box.pack(padx=20, fill="x", pady=5)

        # 5. Download Button
        self.btn_download = tk.Button(root, text="MULAI DOWNLOAD SEKARANG", command=self.validate_and_start, 
                                     bg="#27ae60", fg="white", font=("Arial", 12, "bold"), height=2)
        self.btn_download.pack(pady=15, padx=20, fill="x")

    # --- LOGIC FUNCTIONS ---

    def log(self, message):
        self.log_box.config(state="normal")
        self.log_box.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_box.see(tk.END)
        self.log_box.config(state="disabled")
        self.root.update()

    def show_single(self):
        self.mode = "single"; self.btn_single.config(relief="sunken"); self.btn_multi.config(relief="raised")
        self.text_multi.pack_forget(); self.entry_single.pack(fill="x")

    def show_multi(self):
        self.mode = "multi"; self.btn_single.config(relief="raised"); self.btn_multi.config(relief="sunken")
        self.entry_single.pack_forget(); self.text_multi.pack(fill="x")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_path = folder
            self.label_path.config(text=folder, fg="#27ae60")

    def validate_and_start(self):
        if not self.save_path:
            messagebox.showerror("Error", "Pilih folder simpan terlebih dahulu!"); return
        
        delay = int(self.spin_delay.get())
        if delay <= 5:
            if not messagebox.askyesno("Peringatan", f"Jeda {delay}s sangat berisiko terdeteksi bot. Tetap lanjutkan?"): return

        urls = [self.entry_single.get().strip()] if self.mode == "single" else [l.strip() for l in self.text_multi.get("1.0", tk.END).split("\n") if l.strip()][:10]
        
        if not any(urls):
            messagebox.showwarning("Kosong", "Link tidak boleh kosong!"); return

        self.btn_download.config(state="disabled", bg="#7f8c8d")
        threading.Thread(target=self.download_process, args=(urls,), daemon=True).start()

    def process_ffmpeg(self, input_file, final_output):
        """Proses Mute, HD Enhance, dan Rename tanpa memunculkan CMD"""
        temp_work = input_file.replace(".mp4", "_work.mp4")
        
        # Konfigurasi agar jendela CMD FFmpeg tidak muncul
        startupinfo = None
        if os.name == 'nt':  # Cek jika sistem operasinya Windows
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0 # 0 berarti SW_HIDE (sembunyikan jendela)

        cmd = [self.ffmpeg_path, '-i', input_file]
        
        if self.var_enhance.get():
            cmd += ['-vf', 'unsharp=5:5:1.0:5:5:0.0,eq=contrast=1.1:saturation=1.2']
            self.log("HD Enhance: Sharpening & Color Boost...")
            
        if self.var_mute.get():
            cmd += ['-an']
            self.log("Audio: Menghapus suara (Mute)...")
        else:
            cmd += ['-c:a', 'copy']

        cmd += ['-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-sn', '-map_metadata', '-1', temp_work, '-y']
        
        try:
            # Menambahkan parameter startupinfo dan creationflags
            subprocess.run(
                cmd, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL, 
                check=True,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            if os.path.exists(final_output): os.remove(final_output)
            os.rename(temp_work, final_output)
            if os.path.exists(input_file): os.remove(input_file)
            return True
        except Exception as e:
            self.log(f"FFmpeg Error: Gagal memproses efek.")
            if not os.path.exists(final_output): os.rename(input_file, final_output)
            return False

    # Ganti bagian ini di dalam fungsi download_process
    def download_process(self, urls):
        total = len(urls)
        delay_val = int(self.spin_delay.get())
        
        for i, url in enumerate(urls):
            if i > 0:
                self.log(f"Jeda Keamanan: Menunggu {delay_val} detik...")
                time.sleep(delay_val)

            try:
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    raw_title = info.get('title', 'video')
                    clean_title = re.sub(r'[\\/*?:"<>|]', "", raw_title)[:15].strip()
                    if not clean_title: clean_title = f"video_{int(time.time())}"
                
                # --- LOGIKA ANTI-OVERWRITE ---
                base_name = clean_title
                counter = 1
                final_output = os.path.join(self.save_path, f"{base_name}.mp4")
                
                # Cek jika file sudah ada, tambahkan angka di belakangnya
                while os.path.exists(final_output):
                    final_output = os.path.join(self.save_path, f"{base_name}_{counter}.mp4")
                    counter += 1
                
                new_clean_title = os.path.basename(final_output).replace(".mp4", "")
                # -----------------------------

                self.log(f"[{i+1}/{total}] Download: {new_clean_title}...")
                
                temp_file = os.path.join(self.save_path, f"tmp_dl_{int(time.time())}_{i}.mp4")
                
                ydl_opts = {
                    'outtmpl': temp_file,
                    'format': 'bestvideo+bestaudio/best',
                    'quiet': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl_dl:
                    ydl_dl.download([url])

                self.process_ffmpeg(temp_file, final_output)
                self.log(f"SUKSES: Saved as {os.path.basename(final_output)}")

            except Exception as e:
                self.log(f"ERROR: {str(e)[:60]}")
                continue

        self.log("--- SEMUA ANTRIAN SELESAI ---")
        self.btn_download.config(state="normal", bg="#27ae60")
        messagebox.showinfo("Berhasil", "Semua video telah diproses dan disimpan.")
        os.startfile(self.save_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopDownloader(root)
    root.mainloop()