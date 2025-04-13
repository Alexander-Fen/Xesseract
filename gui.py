import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from PIL import Image, ImageTk
from pathlib import Path
import pytesseract
import sv_ttk
import json
import sys
import os

TESSERACT_EXE_PATH_PATH = Path(os.getenv('ProgramData')) / 'xesseract_tess_location.json'

LANGUAGES = {
    'English': 'eng',
    'Deutsch': 'deu',
    'Français': 'fra',
    'Українська': 'ukr',
    'Русский': 'rus',
    'Español': 'spa',
    'Italiano': 'ita',
    'Polski': 'pol'
}


def get_tesseract_path():
    if TESSERACT_EXE_PATH_PATH.exists():
        with open(TESSERACT_EXE_PATH_PATH, 'r') as f:
            data = json.load(f)
            return data.get('tesseract_path')
    else:
        file_path = filedialog.askopenfilename(
            title="Select tesseract.exe",
            filetypes=[("Tesseract Executable", "tesseract.exe")],
            defaultextension=".exe"
        )

        if file_path and file_path.lower().endswith("tesseract.exe"):
            with open(TESSERACT_EXE_PATH_PATH, 'w') as f:
                json.dump({'tesseract_path': file_path}, f)
            return file_path
        else:
            raise FileNotFoundError("Tesseract executable not selected.")


class OCRApp:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("Xesseract")
        self.root.resizable(False, False)

        self.image_path = image_path
        self.original_image = None
        self.tk_img = None

        self.create_widgets()
        self.load_image()
        self.run_ocr()

    def create_widgets(self):
        language_frame = ttk.Frame(self.root)
        language_frame.grid(pady=(5, 0), padx=5, row=0, column=0, columnspan=2, sticky='w')

        buttons_frame = ttk.Frame(self.root)
        buttons_frame.grid(pady=(5, 0), padx=5, row=0, column=0, columnspan=2)

        exit_frame = ttk.Frame(self.root)
        exit_frame.grid(pady=(5, 0), padx=5, row=0, column=0, columnspan=2, sticky='e')

        image_frame = ttk.Frame(self.root)
        image_frame.grid(pady=5, padx=5, row=1, column=0)

        text_frame = ttk.Frame(self.root)
        text_frame.grid(pady=5, padx=(0, 5), row=1, column=1)

        self.lang_var = tk.StringVar()
        self.lang_menu = ttk.Combobox(
            language_frame,
            textvariable=self.lang_var,
            values=list(LANGUAGES.keys()),
            state="readonly",
            width=12
        )
        self.lang_menu.set("English")
        self.lang_menu.pack(side=tk.LEFT)

        self.lang_menu.bind("<<ComboboxSelected>>", lambda e: self.run_ocr())

        self.img_label = ttk.Label(image_frame)
        self.img_label.pack()

        self.text_box = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=65, height=25)
        self.text_box.pack()

        copy_btn = ttk.Button(buttons_frame, text="Copy All", command=self.copy_text)
        exit_btn = ttk.Button(exit_frame, text="Close", command=lambda: self.root.quit())

        copy_btn.pack(side=tk.LEFT, padx=5)
        exit_btn.pack(side=tk.LEFT)

    def load_image(self):
        try:
            self.original_image = Image.open(self.image_path)
            display_image = self.original_image.copy()
            display_image.thumbnail((350, 350))
            self.tk_img = ImageTk.PhotoImage(display_image)
            self.img_label.configure(image=self.tk_img)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{e}")
            sys.exit(1)

    def run_ocr(self):
        lang_code = LANGUAGES.get(self.lang_var.get(), 'eng')
        try:
            text = pytesseract.image_to_string(self.original_image, lang=lang_code)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, text)
        except pytesseract.TesseractError as e:
            messagebox.showerror("Tesseract Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run OCR:\n{e}")

    def copy_text(self):
        text = self.text_box.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()


if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()

    if len(sys.argv) != 2:
        print("Usage: py gui.py /path/to/image")
        sys.exit(1)

    window = tk.Tk()
    app = OCRApp(window, sys.argv[1])
    sv_ttk.set_theme("dark")
    window.mainloop()
