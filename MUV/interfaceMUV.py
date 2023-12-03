import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Parâmetros fixos
g = 9.81  # Aceleração da gravidade (m/s²)
intervalo_tempo = 0.1  # Intervalo de tempo entre as medições (s)
velocidade_inicial = 0  # Velocidade inicial do objeto (m/s)
tempo_inicial = 0  # Tempo inicial (s)
altura_inicial = 0  # Altura inicial do objeto (será definida posteriormente)

# Função para calcular a altura em um dado tempo
def calcular_altura(altura_inicial, tempo):
    altura = altura_inicial - (0.5 * g * (tempo ** 2))
    return altura

# Função para atualizar o gráfico
def atualizar_grafico():
    tempos = np.arange(tempo_inicial, tempo_inicial + 20, intervalo_tempo)
    alturas = [calcular_altura(altura_inicial, t) for t in tempos]

    ax.clear()
    ax.plot(tempos, alturas)
    ax.set_xlabel('Tempo (s)')
    ax.set_ylabel('Altura (m)')
    ax.set_title('Queda Livre')
    canvas.draw()

# Função para iniciar a simulação
def iniciar_simulacao():
    global altura_inicial
    altura_inicial = float(altura_inicial_entry.get())
    atualizar_grafico()

# Função para resetar a simulação
def resetar_simulacao():
    altura_inicial_entry.delete(0, tk.END)
    ax.clear()
    canvas.draw()

# Configuração da janela
root = tk.Tk()
root.title("Simulador de Queda Livre")

# Entrada para a altura inicial
altura_inicial_label = ttk.Label(root, text="Altura Inicial (m):")
altura_inicial_label.pack()
altura_inicial_entry = ttk.Entry(root)
altura_inicial_entry.pack()

# Botão para iniciar a simulação
botao_iniciar = ttk.Button(root, text="Iniciar Simulação", command=iniciar_simulacao)
botao_iniciar.pack()

# Botão para resetar a simulação
botao_reset = ttk.Button(root, text="Resetar Simulação", command=resetar_simulacao)
botao_reset.pack()

# Configuração do gráfico
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Iniciar a interface
root.mainloop()