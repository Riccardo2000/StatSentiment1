
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import docx
import Global_data

def browse_file(text_area, load_data_to_treeview):
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("Word files", "*.docx")])
    try:
        if file_path.endswith(".xlsx"):
            Global_data.df = pd.read_excel(file_path)
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, "File Excel caricato correttamente\n")
            load_data_to_treeview(Global_data.df)
            return Global_data.df
        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, f"File Word caricato correttamente\n\nTesto Estratto:\n\n{text}\n")
            return None
    except Exception as e:
        messagebox.showerror("Errore", str(e))
        return None

def save_to_excel(df):
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel files", "*.xlsx"), ("All Files", "*.*")])
    if file_path:
        try:
            Global_data.df.to_excel(file_path, index=False)
            messagebox.showinfo("Successo", "File salvato con successo!")
        except Exception as e:
            messagebox.showerror("Errore", str(e))
