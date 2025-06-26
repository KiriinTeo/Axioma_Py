import tkinter as tk
from tkinter import filedialog

def selecionar_arquivo():
    root = tk.Tk()

    print("Selecione um arquivo para carregar...")
    arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=[("CSV Files", "*.csv"), ("JSON Files", "*.json"), ("Todos os arquivos", "*.*")]
    )

    root.destroy()

    if not arquivo:
        print("Nenhum arquivo selecionado.")
        return None
    return arquivo

