import tkinter as tk
from tkinter import ttk
import File_azione
import Data_analysis
import File_ui
import Global_data

df=None

def load_data_to_treeview(df):
    if df is not None:
        tree.delete(*tree.get_children())
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')
        for row in df.to_numpy().tolist():
            tree.insert("", "end", values=row)

def update_ui(*args):
    analysis_type = analysis_var.get()
    if analysis_type in ['regressione', 'regressione logistica']:
        y_label.grid()
        y_entry.grid()
        x_label.grid()
        x_entry.grid()
    else:
        y_label.grid_remove()
        y_entry.grid_remove()
        x_label.grid_remove()
        x_entry.grid_remove()

# Creazione della finestra principale
window = tk.Tk()
window.title("Analisi dei Dati")
window.geometry("800x600")

create_graph_button = ttk.Button(window, text="Crea Grafico", command=lambda: File_ui.create_graph(Global_data.df), style='TButton')
correlation_button = ttk.Button(window, text="Analisi Correlazione", command=lambda: File_ui.correlation_analysis(Global_data.df), style='TButton')
# Stile dei widget
style = ttk.Style()
style.configure('TButton', font=('Arial', 10))
style.configure('TLabel', font=('Arial', 10))
style.configure('TEntry', font=('Arial', 10))

# Creazione dei widget dell'interfaccia
file_label = ttk.Label(window, text="Seleziona il File:")
file_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

file_entry = ttk.Entry(window, width=50)
file_entry.grid(row=0, column=1, padx=10, pady=10, sticky='we')

browse_button = ttk.Button(window, text="Sfoglia", command=lambda: File_azione.browse_file(text_area, load_data_to_treeview), style='TButton')
browse_button.grid(row=0, column=2, padx=10, pady=10)

analysis_var = tk.StringVar()
analysis_var.trace('w', update_ui)
analysis_choices = ['descrittiva', 'regressione', 'regressione logistica']
analysis_menu = ttk.OptionMenu(window, analysis_var, analysis_choices[0], *analysis_choices)
analysis_menu.grid(row=1, column=0, padx=10, pady=10, sticky='e')

y_var = tk.StringVar()
y_label = ttk.Label(window, text="Colonna Y:")
y_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
y_entry = ttk.Entry(window, textvariable=y_var, width=20)
y_entry.grid(row=2, column=1, padx=10, pady=10, sticky='we')

x_var = tk.StringVar()
x_label = ttk.Label(window, text="Colonne X (separate da virgola):")
x_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
x_entry = ttk.Entry(window, textvariable=x_var, width=50)
x_entry.grid(row=3, column=1, padx=10, pady=10, sticky='we')

analyze_button = ttk.Button(window, text="Esegui Analisi", command=lambda: Data_analysis.analyze_data(Global_data.df, analysis_var.get(), y_var.get(), x_var.get(), text_area), style='TButton')
analyze_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

text_area = tk.Text(window, height=15, width=80, font=('Arial', 10))
text_area.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

# Nascondi i campi Y e X all'avvio
y_label.grid_remove()
y_entry.grid_remove()
x_label.grid_remove()
x_entry.grid_remove()

create_graph_button = ttk.Button(window, text="Crea Grafico", command=File_ui.create_graph, style='TButton')
create_graph_button.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

correlation_button = ttk.Button(window, text="Analisi Correlazione", command=File_ui.correlation_analysis, style='TButton')
correlation_button.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

# Creazione del widget Treeview per visualizzare i dati del DataFrame
tree = ttk.Treeview(window)
tree.grid(row=8, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

# Aggiungi il pulsante per l'analisi del sentiment su testo Word
perform_sentiment_button = ttk.Button(window, text="Esegui Sentiment Analysis su Word", command=lambda: Data_analysis.perform_sentiment_analysis(text_area), style='TButton')
perform_sentiment_button.grid(row=0, column=3, padx=10, pady=10)

# Pulsante per salvare il DataFrame in un file Excel
save_button = ttk.Button(window, text="Salva su Excel", command=lambda: File_azione.save_to_excel(df))
save_button.grid(row=9, column=0, columnspan=3, padx=10, pady=10)

# Creazione del Scrollbar e collegamento al Treeview
scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
scrollbar.grid(row=8, column=3, sticky='ns')
tree.configure(yscrollcommand=scrollbar.set)

# Aggiustamenti per il layout della finestra
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(8, weight=1)

 # Variabile per memorizzare il DataFrame

window.mainloop()
