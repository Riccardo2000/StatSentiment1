
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tkinter as tk
from tkinter import messagebox
import Global_data

def perform_sentiment_analysis(text_area):
    text = text_area.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Errore", "Nessun testo trovato nel campo di input")
        return

    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    if sentiment['compound'] >= 0.05:
        sentiment_label = "Positivo"
    elif sentiment['compound'] <= -0.05:
        sentiment_label = "Negativo"
    else:
        sentiment_label = "Neutro"

    sentiment_result = f"Sentiment: {sentiment_label}\nPunteggio: {sentiment['compound']}\n"
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, sentiment_result)

def analyze_data(df, analysis_type, y_column, x_columns, text_area):
    try:
        if Global_data.df is None:
            messagebox.showerror("Errore", "Nessun file caricato")
            return

        text_area.delete('1.0', tk.END)

        if analysis_type == 'regressione':
            perform_linear_regression(Global_data.df, y_column, x_columns, text_area)

        elif analysis_type == 'descrittiva':
            perform_descriptive_analysis(Global_data.df, text_area)

        elif analysis_type == 'regressione logistica':
            perform_logistic_regression(Global_data.df, y_column, x_columns, text_area)

    except Exception as e:
        messagebox.showerror("Errore", str(e))

def perform_linear_regression(df, y_column, x_columns, text_area):
    X = Global_data.df[x_columns.split(',')]
    Y = Global_data.df[y_column]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
    model = LinearRegression().fit(X_train, Y_train)
    Y_pred = model.predict(X_test)
    mse = mean_squared_error(Y_test, Y_pred)
    r2 = r2_score(Y_test, Y_pred)
    text_area.insert(tk.END, f"Risultato Regressione:\nCoefficiente: {model.coef_}\nIntercept: {model.intercept_}\nMSE: {mse}\nR2: {r2}\n")

def perform_descriptive_analysis(df, text_area):
    text_area.insert(tk.END, f"Risultato Analisi Descrittiva:\n{Global_data.df.describe().to_string()}\n")
    # Qui puoi aggiungere ulteriori dettagli o statistiche descrittive

def perform_logistic_regression(df, y_column, x_columns, text_area):
    X = Global_data.df[x_columns.split(',')]
    Y = Global_data.df[y_column]
    model = LogisticRegression()
    model.fit(X, Y)
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
    Y_pred = model.predict(X_test)
    r2 = r2_score(Y_test, Y_pred)
    text_area.insert(tk.END, f"Modello di regressione logistica creato.\nCoefficiente: {model.coef_}\nIntercept: {model.intercept_}\n")

