import tkinter as tk
from tkinter import messagebox
import json
import os
import sys

# Splash screen
splash = tk.Tk()
splash.title("CassSoft 95™")
splash.geometry("400x200")
splash.configure(bg="#C0C0C0")
splash.overrideredirect(True)
splash.eval('tk::PlaceWindow . center')

splash_label = tk.Label(
    splash,
    text="🔧 Iniciando CassSoft 95™...",
    bg="#C0C0C0",
    fg="black",
    font=("MS Sans Serif", 12)
)
splash_label.pack(expand=True)
splash.after(2000, splash.destroy)
splash.mainloop()

# App principal
janela = tk.Tk()
janela.title("CassSoft 95™ - Macetador")
janela.geometry("800x650")  # Aumentada a janela
janela.configure(bg="#C0C0C0")
janela.option_add("*Font", ("MS Sans Serif", 12))
janela.resizable(False, False)

# Suavizar bordas
janela.attributes('-alpha', 0.97)  # Leve transparência para suavizar o visual

# VARIÁVEIS GLOBAIS
macetadas = 0
macetadas_por_clique = 1
auto_macetadores = 0
poder_auto_macetador = 1
preco_upgrade = 20
preco_auto = 50
preco_turbo_auto = 100

conquistas = {
    "primeiro_click": False,
    "dez_macetadas": False,
    "cinquenta_macetadas": False,
    "primeiro_auto": False
}

SAVE_FILE = "save.json"

# SALVAMENTO E CARREGAMENTO
def salvar_jogo():
    dados = {
        "macetadas": macetadas,
        "macetadas_por_clique": macetadas_por_clique,
        "auto_macetadores": auto_macetadores,
        "poder_auto_macetador": poder_auto_macetador,
        "preco_upgrade": preco_upgrade,
        "preco_auto": preco_auto,
        "preco_turbo_auto": preco_turbo_auto,
        "conquistas": conquistas
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(dados, f)

def carregar_jogo():
    global macetadas, macetadas_por_clique, auto_macetadores, poder_auto_macetador
    global preco_upgrade, preco_auto, preco_turbo_auto, conquistas

    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            dados = json.load(f)
            macetadas = dados.get("macetadas", 0)
            macetadas_por_clique = dados.get("macetadas_por_clique", 1)
            auto_macetadores = dados.get("auto_macetadores", 0)
            poder_auto_macetador = dados.get("poder_auto_macetador", 1)
            preco_upgrade = dados.get("preco_upgrade", 20)
            preco_auto = dados.get("preco_auto", 50)
            preco_turbo_auto = dados.get("preco_turbo_auto", 100)
            conquistas.update(dados.get("conquistas", {}))

# Função de notificação
def mostrar_notificacao(texto):
    notificacao_label.config(text=texto)
    notificacao_label.place(relx=0.5, rely=0.95, anchor="s")
    janela.after(3000, lambda: notificacao_label.place_forget())

# Atualização de UI
def atualizar_labels():
    contador_label.config(text=f"Macetadas computadas: {macetadas}")
    upgrade_label.config(text=f"Upgrade de Clique ({preco_upgrade} macetadas)")
    auto_label.config(text=f"AutoMacetador ({preco_auto} macetadas)")
    turbo_label.config(text=f"Turbo AutoMacetador ({preco_turbo_auto} macetadas)")
    auto_status.config(text=f"{auto_macetadores} ativos | Força: {poder_auto_macetador}/s")

# Conquistas
def checar_conquistas():
    if macetadas >= 1 and not conquistas["primeiro_click"]:
        conquistas["primeiro_click"] = True
        mostrar_notificacao("🏆 Primeira macetada realizada!")
    if macetadas >= 10 and not conquistas["dez_macetadas"]:
        conquistas["dez_macetadas"] = True
        mostrar_notificacao("🏆 10 macetadas atingidas!")
    if macetadas >= 50 and not conquistas["cinquenta_macetadas"]:
        conquistas["cinquenta_macetadas"] = True
        mostrar_notificacao("🏆 50 macetadas! Tá on fire!")
    if auto_macetadores >= 1 and not conquistas["primeiro_auto"]:
        conquistas["primeiro_auto"] = True
        mostrar_notificacao("🏆 Comprou seu primeiro AutoMacetador!")

# Funções principais
def funcao():
    global macetadas
    macetadas += macetadas_por_clique
    greeting.config(text="🛠️ Macetou!")
    atualizar_labels()
    checar_conquistas()

def comprar_upgrade():
    global macetadas, macetadas_por_clique, preco_upgrade
    if macetadas >= preco_upgrade:
        macetadas -= preco_upgrade
        macetadas_por_clique += 1
        preco_upgrade = int(preco_upgrade * 1.5)
        atualizar_labels()

def comprar_auto_macetador():
    global macetadas, auto_macetadores, preco_auto
    if macetadas >= preco_auto:
        macetadas -= preco_auto
        auto_macetadores += 1
        preco_auto = int(preco_auto * 1.5)
        atualizar_labels()
        checar_conquistas()

def comprar_turbo_auto():
    global macetadas, poder_auto_macetador, preco_turbo_auto
    if macetadas >= preco_turbo_auto:
        macetadas -= preco_turbo_auto
        poder_auto_macetador += 1
        preco_turbo_auto = int(preco_turbo_auto * 1.7)
        atualizar_labels()

def gerar_macetadas_auto():
    global macetadas
    macetadas += auto_macetadores * poder_auto_macetador
    atualizar_labels()
    checar_conquistas()
    janela.after(1000, gerar_macetadas_auto)

def loop_salvar_auto():
    salvar_jogo()
    janela.after(5000, loop_salvar_auto)

# INTERFACE
frame_top = tk.Frame(janela, bg="#000080")
titulo = tk.Label(frame_top, text="CassSoft 95™ - MACETADOR", bg="#000080", fg="white", pady=5, font=("MS Sans Serif", 14, "bold"))
titulo.pack(padx=10, pady=10)
frame_top.pack(fill="x")

greeting = tk.Label(janela, text="👋 Oi macetador", bg="#C0C0C0", fg="black", relief="sunken", bd=2, padx=10, pady=5)
greeting.pack(pady=10)

botao = tk.Button(janela, text="💥 Macetar", command=funcao, width=20, height=2, bg="#F0F0F0", fg="black", relief="raised", bd=4)
botao.pack(pady=10)

contador_label = tk.Label(janela, text="Macetadas computadas: 0", bg="#C0C0C0", fg="black", relief="sunken", bd=2, padx=10, pady=5)
contador_label.pack(pady=10)

upgrade_button = tk.Button(janela, text="⬆️ Upgrade de Clique", command=comprar_upgrade, bg="#D0D0D0", relief="raised", bd=3)
upgrade_button.pack(pady=5)
upgrade_label = tk.Label(janela, text="", bg="#C0C0C0")
upgrade_label.pack()

auto_button = tk.Button(janela, text="🤖 Comprar AutoMacetador", command=comprar_auto_macetador, bg="#D0D0D0", relief="raised", bd=3)
auto_button.pack(pady=5)
auto_label = tk.Label(janela, text="", bg="#C0C0C0")
auto_label.pack()
auto_status = tk.Label(janela, text="", bg="#C0C0C0")
auto_status.pack()

turbo_button = tk.Button(janela, text="⚡ Turbo AutoMacetador", command=comprar_turbo_auto, bg="#D0D0D0", relief="raised", bd=3)
turbo_button.pack(pady=5)
turbo_label = tk.Label(janela, text="", bg="#C0C0C0")
turbo_label.pack()

notificacao_label = tk.Label(janela, text="", bg="#FFFF99", fg="black", font=("MS Sans Serif", 10), relief="solid", bd=1, padx=5, pady=2)

# CARREGAR JOGO, INICIAR LOOPS
carregar_jogo()
atualizar_labels()
janela.after(1000, gerar_macetadas_auto)
janela.after(5000, loop_salvar_auto)

janela.mainloop()


# DEPOIS FAZER  HUB DE APLICATIVOS.