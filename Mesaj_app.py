import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
from datetime import datetime

# Notlar klasörü
NOTES_DIR = "Notlar"
os.makedirs(NOTES_DIR, exist_ok=True)
META_FILE = os.path.join(NOTES_DIR, "meta.json")

class MesajNotDefteri:
    def __init__(self, root):
        self.root = root
        self.root.title("Mesajlaşma Tarzı Not Defteri")
        self.root.geometry("900x600")
        self.root.minsize(700, 400)
        self.root.configure(bg="#f0f0f0")

        self.notes = self.load_notes()
        self.selected_note = None

        self.setup_ui()
        self.load_note_list()

    def setup_ui(self):
        # Ana çerçeve
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Sol Panel - Not Listesi
        left_frame = tk.Frame(main_frame, width=280, bg="#2c3e50")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        left_frame.pack_propagate(False)

        # Başlık
        tk.Label(left_frame, text="NOTLAR", font=("Helvetica", 13, "bold"),
                 bg="#2c3e50", fg="white").pack(pady=(15, 8))

        # Arama
        search_frame = tk.Frame(left_frame, bg="#2c3e50")
        search_frame.pack(fill=tk.X, padx=12, pady=5)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, fg="white", bg="#34495e", insertbackground="white")
        search_entry.pack(fill=tk.X, padx=5, pady=2)
        search_entry.bind("<KeyRelease>", self.filter_notes)

        # Not Listesi
        self.listbox = tk.Listbox(left_frame, bg="#34495e", fg="white", selectbackground="#3498db",
                                  font=("Segoe UI", 10), relief=tk.FLAT, highlightthickness=0)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        self.listbox.bind("<<ListboxSelect>>", self.select_note)

        # Yeni Not Butonu
        tk.Button(left_frame, text="+ Yeni Not", bg="#27ae60", fg="white", font=("Helvetica", 10, "bold"),
                  command=self.new_note, relief=tk.FLAT, cursor="hand2").pack(fill=tk.X, padx=12, pady=8)

        # Sağ Panel - Not İçeriği
        right_frame = tk.Frame(main_frame, bg="white")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)

        # Not Başlığı
        self.title_var = tk.StringVar(value="Not seçilmedi")
        title_entry = tk.Entry(right_frame, textvariable=self.title_var, font=("Helvetica", 16, "bold"),
                               relief=tk.FLAT, bg="white", fg="#2c3e50")
        title_entry.pack(fill=tk.X, padx=20, pady=(15, 8))
        title_entry.bind("<KeyRelease>", self.update_title)

        # Metin Alanı
        self.text_area = tk.Text(right_frame, wrap=tk.WORD, undo=True, font=("Segoe UI", 11),
                                 relief=tk.FLAT, bd=0, highlightthickness=1, highlightbackground="#ddd")
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Otomatik kaydetme
        self.root.after(1500, self.auto_save)

    def load_notes(self):
        if os.path.exists(META_FILE):
            try:
                with open(META_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_notes(self):
        with open(META_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=2)

    def load_note_list(self):
        self.listbox.delete(0, tk.END)
        search = self.search_var.get().lower()
        for note in self.notes:
            if search in note["title"].lower():
                self.listbox.insert(tk.END, note["title"])

    def filter_notes(self, event=None):
        self.load_note_list()

    def new_note(self):
        timestamp = datetime.now().strftime("%d.%m %H:%M")
        title = f"Yeni Not - {timestamp}"
        filename = f"not_{len(self.notes)}.txt"
        path = os.path.join(NOTES_DIR, filename)

        note = {"title": title, "filename": filename, "filepath": path}
        self.notes.append(note)
        open(path, 'w', encoding='utf-8').close()
        self.save_notes()
        self.load_note_list()
        self.select_note_by_index(len(self.notes) - 1)

    def select_note(self, event):
        sel = self.listbox.curselection()
        if sel:
            self.select_note_by_index(sel[0])

    def select_note_by_index(self, idx):
        self.selected_note = self.notes[idx]
        self.title_var.set(self.selected_note["title"])
        with open(self.selected_note["filepath"], 'r', encoding='utf-8') as f:
            content = f.read()
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, content)
        self.listbox.selection_set(idx)

    def update_title(self, event=None):
        if self.selected_note:
            new_title = self.title_var.get().strip() or "Adsız Not"
            self.selected_note["title"] = new_title
            self.save_notes()
            self.load_note_list()
            idx = self.notes.index(self.selected_note)
            self.listbox.selection_set(idx)

    def auto_save(self):
        if self.selected_note:
            content = self.text_area.get(1.0, tk.END).rstrip()
            with open(self.selected_note["filepath"], 'w', encoding='utf-8') as f:
                f.write(content)
        self.root.after(1500, self.auto_save)

# Başlat
if __name__ == "__main__":
    root = tk.Tk()
    app = MesajNotDefteri(root)
    root.mainloop()