

import matplotlib.pyplot as plt
from tkinter import simpledialog, messagebox
import Global_data

def create_graph():
    if Global_data.df is None:
        messagebox.showerror("Errore", "Nessun file caricato")
        return

    graph_type = simpledialog.askstring("Input", "Inserisci tipo di grafico (bar, line, scatter):")
    x_column = simpledialog.askstring("Input", "Inserisci il nome della colonna X:")
    y_column = simpledialog.askstring("Input", "Inserisci il nome della colonna Y:")

    try:
        plt.figure(figsize=(10, 6))
        if graph_type == 'bar':
            Global_data.df.plot(kind='bar', x=x_column, y=y_column, ax=plt.gca())
        elif graph_type == 'line':
            Global_data.df.plot(kind='line', x=x_column, y=y_column, ax=plt.gca())
        elif graph_type == 'scatter':
            Global_data.df.plot(kind='scatter', x=x_column, y=y_column, ax=plt.gca())
        plt.title(f'{graph_type.title()} Graph')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.show()
    except Exception as e:
        messagebox.showerror("Errore", str(e))

def correlation_analysis():
    if Global_data.df is None:
        messagebox.showerror("Errore", "Nessun file caricato")
        return

    x_column = simpledialog.askstring("Input", "Inserisci il nome della colonna X:")
    y_column = simpledialog.askstring("Input", "Inserisci il nome della colonna Y:")

    try:
        correlation = Global_data.df[x_column].corr(Global_data.df[y_column])
        plt.figure(figsize=(10, 6))
        plt.scatter(Global_data.df[x_column], Global_data.df[y_column])
        plt.title(f'Correlazione tra {x_column} e {y_column}: {correlation:.2f}')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.show()
    except Exception as e:
        messagebox.showerror("Errore", str(e))
