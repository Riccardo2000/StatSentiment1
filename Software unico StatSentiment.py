import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import docx
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



def browse_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("Word files", "*.docx")])
    try:
        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, "File Excel caricato correttamente\n")
            load_data_to_treeview()
        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, f"File Word caricato correttamente\n\nTesto Estratto:\n\n{text}\n")
            df = None  # Imposta df su None in modo che non sia richiesto un file Excel
    except Exception as e:
        messagebox.showerror("Errore", str(e))
        df = None


def perform_sentiment_analysis_on_word():
    try:
        text = text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Errore", "Nessun testo trovato nel campo di input")
            return
        perform_sentiment_analysis(text)
    except Exception as e:
        messagebox.showerror("Errore", str(e))


def perform_sentiment_analysis(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)

    # Determina il sentiment sulla base del punteggio complessivo
    if sentiment['compound'] >= 0.05:
        sentiment_label = "Positivo"
    elif sentiment['compound'] <= -0.05:
        sentiment_label = "Negativo"
    else:
        sentiment_label = "Neutro"

    sentiment_result = f"Sentiment: {sentiment_label}\nPunteggio Composito: {sentiment['compound']}\n"

    text_area.delete('1.0', tk.END)  # Rimuovi i risultati precedenti
    text_area.insert(tk.END, sentiment_result)

def load_data_to_treeview():
    global df
    if df is not None:
        tree.delete(*tree.get_children())
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')
        for row in df.to_numpy().tolist():
            tree.insert("", "end", values=row)

def interpret_descriptive_stats(df):
    desc_stats = df.describe()
    interpretation = "Interpretazione delle Statistiche Descrittive:\n"
    for col in desc_stats.columns:
        interpretation += f"\nColonna: {col}\n"
        interpretation += f"Media: {desc_stats[col]['mean']:.2f}\n"
        interpretation += f"Mediana: {df[col].median():.2f}\n"
        interpretation += f"Deviazione Standard: {desc_stats[col]['std']:.2f}\n"
        interpretation += f"Minimo: {desc_stats[col]['min']:.2f}, Massimo: {desc_stats[col]['max']:.2f}\n"
        interpretation += f"25° percentile: {desc_stats[col]['25%']:.2f}, 75° percentile: {desc_stats[col]['75%']:.2f}\n"
    return interpretation

def analyze_data():
    global df
    if df is None:
        messagebox.showerror("Errore", "Nessun file caricato")
        return

    analysis_type = analysis_var.get()
    y_column = y_var.get()
    x_columns = x_var.get()

    try:
        text_area.delete('1.0', tk.END)

        if analysis_type == 'regressione':
            X = df[x_columns.split(',')]
            Y = df[y_column]
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
            model = LinearRegression().fit(X_train, Y_train)
            Y_pred = model.predict(X_test)
            mse = mean_squared_error(Y_test, Y_pred)
            r2 = r2_score(Y_test, Y_pred)
            text_area.insert(tk.END, f"Risultato Regressione:\nCoefficiente: {model.coef_}\nIntercept: {model.intercept_}\nMSE: {mse}\nR2: {r2}\n")

        elif analysis_type == 'descrittiva':
            text_area.insert(tk.END, f"Risultato Analisi Descrittiva:\n{df.describe().to_string()}\n")
            text_area.insert(tk.END, interpret_descriptive_stats(df))

        elif analysis_type == 'regressione logistica':
            X = df[x_columns.split(',')]
            Y = df[y_column]
            model = LogisticRegression()
            model.fit(X, Y)
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
            Y_pred = model.predict(X_test)
            r2 = r2_score(Y_test, Y_pred)

            text_area.insert(tk.END, f"Modello di regressione logistica creato.\nCoefficiente: {model.coef_}\nIntercept: {model.intercept_}\n")

    except Exception as e:
        messagebox.showerror("Errore", str(e))

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

def correlation_analysis():
    global df
    if df is None:
        messagebox.showerror("Errore", "Nessun file caricato")
        return

    x_column = simpledialog.askstring("Input", "Inserisci il nome della colonna X:")
    y_column = simpledialog.askstring("Input", "Inserisci il nome della colonna Y:")

    try:
        correlation = df[x_column].corr(df[y_column])
        plt.figure(figsize=(10, 6))
        plt.scatter(df[x_column], df[y_column])
        plt.title(f'Correlazione tra {x_column} e {y_column}: {correlation:.2f}')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.show()
    except Exception as e:
        messagebox.showerror("Errore", str(e))

def create_graph():
    global df
    if df is None:
        messagebox.showerror("Errore", "Nessun file caricato")
        return

    graph_type = simpledialog.askstring("Input", "Inserisci tipo di grafico (bar, line, scatter):")
    x_column = simpledialog.askstring("Input", "Inserisci il nome della colonna X:")
    y_column = simpledialog.askstring("Input", "Inserisci il nome della colonna Y:")

    try:
        plt.figure(figsize=(10, 6))
        if graph_type == 'bar':
            df.plot(kind='bar', x=x_column, y=y_column, ax=plt.gca())
        elif graph_type == 'line':
            df.plot(kind='line', x=x_column, y=y_column, ax=plt.gca())
        elif graph_type == 'scatter':
            df.plot(kind='scatter', x=x_column, y=y_column, ax=plt.gca())
        plt.title(f'{graph_type.title()} Graph')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.show()
    except Exception as e:
        messagebox.showerror("Errore", str(e))

# Creazione della finestra principale
window = tk.Tk()
window.title("Analisi dei Dati")
window.geometry("800x600")  # Imposta le dimensioni della finestra

# Stile dei widget
style = ttk.Style()
style.configure('TButton', font=('Arial', 10))
style.configure('TLabel', font=('Arial', 10))
style.configure('TEntry', font=('Arial', 10))

# Creazione dei widget dell'interfaccia
file_label = ttk.Label(window, text="Seleziona il File:", style='TLabel')
file_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

file_entry = ttk.Entry(window, width=50, style='TEntry')
file_entry.grid(row=0, column=1, padx=10, pady=10, sticky='we')

browse_button = ttk.Button(window, text="Sfoglia", command=browse_file, style='TButton')
browse_button.grid(row=0, column=2, padx=10, pady=10)

analysis_var = tk.StringVar()
analysis_var.trace('w', update_ui)
analysis_choices = ['descrittiva', 'regressione', 'logistic_regression']
analysis_menu = ttk.OptionMenu(window, analysis_var, analysis_choices[0], *analysis_choices)
analysis_menu.grid(row=1, column=0, padx=10, pady=10, sticky='e')

y_var = tk.StringVar()
y_label = ttk.Label(window, text="Colonna Y:", style='TLabel')
y_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
y_entry = ttk.Entry(window, textvariable=y_var, width=20, style='TEntry')
y_entry.grid(row=2, column=1, padx=10, pady=10, sticky='we')

x_var = tk.StringVar()
x_label = ttk.Label(window, text="Colonne X (separate da virgola):", style='TLabel')
x_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
x_entry = ttk.Entry(window, textvariable=x_var, width=50, style='TEntry')
x_entry.grid(row=3, column=1, padx=10, pady=10, sticky='we')

analyze_button = ttk.Button(window, text="Esegui Analisi", command=analyze_data, style='TButton')
analyze_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

text_area = tk.Text(window, height=15, width=80, font=('Arial', 10))
text_area.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

# Configura lo stretching delle colonne e delle righe
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(5, weight=1)

# Nascondi i campi Y e X all'avvio
y_label.grid_remove()
y_entry.grid_remove()
x_label.grid_remove()
x_entry.grid_remove()

create_graph_button = ttk.Button(window, text="Crea Grafico", command=create_graph, style='TButton')
create_graph_button.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

correlation_button = ttk.Button(window, text="Analisi Correlazione", command=correlation_analysis, style='TButton')
correlation_button.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

# Creazione del widget Treeview per visualizzare i dati del DataFrame
tree = ttk.Treeview(window)
tree.grid(row=8, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

# Add a button to perform sentiment analysis on loaded Word text
perform_sentiment_button = ttk.Button(window, text="Esegui Sentiment Analysis su Word", command=perform_sentiment_analysis_on_word, style='TButton')
perform_sentiment_button.grid(row=0, column=3, padx=10, pady=10)

#modifica dei dati
def on_double_click(event):
    # Ottieni l'item selezionato
    item = tree.selection()[0]
    column = tree.identify_column(event.x)  # Identifica la colonna cliccata

    # Crea un widget di input (Entry) per modificare il valore
    entry = ttk.Entry(window)
    entry.grid(row=8, column=0, columnspan=2, sticky='nsew')
    entry.insert(0, tree.item(item, 'values')[int(column[1:]) - 1])  # Prepopola con il valore corrente

    def on_entry_validate():
        # Aggiorna il valore nella cella del Treeview (e nel DataFrame se necessario)
        tree.item(item, values=[entry.get() if int(column[1:]) - 1 == idx else val for idx, val in enumerate(tree.item(item, 'values'))])
        entry.destroy()  # Rimuovi il widget di input

    entry.bind('<Return>', lambda e: on_entry_validate())  # Aggiorna al pressione di Enter
    entry.bind('<FocusOut>', lambda e: entry.destroy())  # Rimuovi l'entry se perde il focus
    entry.focus()  # Metti il focus sull'entry

# Aggiungi un bind per il doppio clic
tree.bind('<Double-1>', on_double_click)

# Funzione per salvare il DataFrame in un file Excel
def save_to_excel():
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel files", "*.xlsx"), ("All Files", "*.*")])
    if file_path:
        try:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Successo", "File salvato con successo!")
        except Exception as e:
            messagebox.showerror("Errore", str(e))

# Aggiungi un'etichetta sopra il menu a tendina
analysis_label = ttk.Label(window, text="Tipi di Analisi", style='TLabel')
analysis_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky='w')

# Pulsante per salvare il DataFrame in un file Excel
save_button = ttk.Button(window, text="Salva su Excel", command=save_to_excel)
save_button.grid(row=9, column=0, columnspan=3, padx=10, pady=10)

# Creazione del Scrollbar e collegamento al Treeview
scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
scrollbar.grid(row=8, column=3, sticky='ns')
tree.configure(yscrollcommand=scrollbar.set)
# Aggiustamenti per il layout della finestra
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(8, weight=1)

df = None  # Variabile per memorizzare il DataFrame

window.mainloop()