import os
import tkinter as tk
import requests
from tkinter import ttk, messagebox

# Caminho onde o Steam armazena os dados dos usuários
PASTA_STEAM = r"C:\Program Files (x86)\Steam\userdata"

# Função para buscar os IDs na pasta Steam
def listar_steam_ids():
    if not os.path.exists(PASTA_STEAM):
        return []
    return [pasta for pasta in os.listdir(PASTA_STEAM) if pasta.isdigit()]


# Função que faz a requisição à API
def buscar_dados():
    steam_id = combo.get()
    if not steam_id:
        messagebox.showerror("Erro", "Selecione um SteamID.")
        return

    try:
        url = f"http://localhost:8000/open_dota/obter_nome_jogador/{steam_id}"
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()
        output = f"Jogador: {dados}"
        resultado_var.set(output)
    except Exception as e:
        resultado_var.set(f"Erro: {e}")

# Interface Gráfica
root = tk.Tk()
root.title("Analisador de Partida - SteamID")

tk.Label(root, text="Selecione um SteamID detectado no sistema:").pack(pady=5)

combo = ttk.Combobox(root, values=listar_steam_ids(), width=40)
combo.pack(pady=5)

tk.Button(root, text="Buscar dados", command=buscar_dados).pack(pady=5)

resultado_var = tk.StringVar()
tk.Label(root, textvariable=resultado_var, justify="left", wraplength=400).pack(pady=10)

root.mainloop()
