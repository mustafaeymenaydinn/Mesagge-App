import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
from datetime import datetime

# Ana klasör (notlar buraya kaydedilecek)
NOTES_DIR = "Notlar"
os.makedirs(NOTES_DIR, exist_ok=True)

# Metadata dosyası (notların sırası, başlık vs.)
META_FILE = os.path.join(NOTES_DIR, "meta.json")

class MesajNotDefteri:
    def __init__(self, root):
        self.root = root
        self.root.title("Mesajlaşma Tarzı Not Defteri")
        self.root.geometry("900x600")
        self.root.minsize(700, 400)

        # Not listesi ve seçili not
        self.notes = self.load_notes()
        self.selected_note = None

        self.setup_ui()
        self.load_note_list()

    def setup_ui(self):
        # Ana çerçeve
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Sol panel: Not listesi
        left_frame = tk.Frame(main_frame, width=250, bg="#2c3e50")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        left_frame.pack_propagate(False)

        # Başlık
        title_label = tk.Label(left_frame, text="NOTLAR", font=("Helvetica", 12, "bold"),
                               bg="#2c3e50", fg="white")
        title_label.pack(pady=10)

        # Arama çubuğu
        search_frame = tk.Frame(left_frame, bg="#2c3e50")
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, fg="white", bg="#34495e")
        search_entry.pack(fill=tk.X)
        search_entry.bind("<KeyRelease>", self.filter_notes)

        # Not listesi (Listbox)
        self.note_listbox = tk.Listbox(left_frame, bg="#34495e", fg="white", selectbackground="#3498db")
        self.note_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.note_listbox.bind("<<ListboxSelect>>", self.on_note_select)

        # Yeni not butonu
        new_btn = tk.Button(left_frame, text="+ Yeni Not", bg="#27ae60", fg="white",
                            command=self.new_note)
        new_btn.pack(fill=tk.X, padx=10, pady=5)

        # Sağ panel: Not içeriği
        right_frame = tk.Frame(main_frame, bg="white")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Not başlığı
        self.title_var = tk.StringVar(value="Not Seçilmedi")
        title_entry = tk.Entry(right_frame, textvariable=self.title_var, font=("Helvetica", 14, "bold"))
        title_entry.pack(fill=tk.X, padx=20, pady=(20, 10))
        title_entry.bind("<KeyRelease>", self.update_title)

        # Metin alanı
        self.text_area = tk.Text(right_frame, wrap=tk.WORD, undo=True, font=("Segoe UI", 11))
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Otomatik kaydetme (her 2 saniyede bir)
        self.root.after(2000, self.auto_save)

    def load_notes(self):
        if os.path.exists(META_FILE):
            with open(META_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_notes(self):
        with open(META_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=2)

    def load_note_list(self):
        self.note_listbox.delete(0, tk.END)
        search_term = self.search_var.get().lower()
        for note in self.notes:
            title = note["title"]
            if search_term in title.lower():
                self.note_listbox.insert(tk.END, title)

    def filter_notes(self, event=None):
        self.load_note_list()

    def new_note(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        title = f"Yeni Not - {timestamp}"
        filename = f"not_{len(self.notes)}.txt"
        filepath = os.path.join(NOTES_DIR, filename)

        # Yeni not oluştur
        new_note = {
            "title": title,
            "filename": filename,
            "filepath": filepath
        }
        self.notes.append(new_note)
        self.save_notes()

        # Dosyayı oluştur
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("")

        self.load_note_list()
        self.select_note_by_index(len(self.notes) - 1)

    def on_note_select(self, event):
        selection = self.note_listbox.curselection()
        if selection:
            index = selection[0]
            self.select_note_by_index(index)

    def select_note_by_index(self, index):
        self.selected_note = self.notes[index]
        self.title_var.set(self.selected_note["title"])
        with open(self.selected_note["filepath"], 'r', encoding='utf-8') as f:
            content = f.read()
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, content)
        self.note_listbox.selection_clear(0, tk.END)
        self.note_listbox.selection_set(index)

    def update_title(self, event=None):
        if self.selected_note:
            new_title = self.title_var.get().strip()
            if new_title == "":
                new_title = "Adsız Not"
            self.selected_note["title"] = new_title
            self.save_notes()
            self.load_note_list()
            # Seçimi koru
            idx = self.notes.index(self.selected_note)
            self.note_listbox.selection_set(idx)

    def auto_save(self):
        if self.selected_note:
            content = self.text_area.get(1.0, tk.END).strip()
            with open(self.selected_note["filepath"], 'w', encoding='utf-8') as f:
                f.write(content)
        self.root.after(2000, self.auto_save)

# Uygulamayı başlat
if __name__ == "__main__":
    root = tk.Tk()
    app = MesajNotDefteri(root)
    root.mainloop()
