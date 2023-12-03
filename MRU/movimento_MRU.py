import tkinter as tk
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from queue import Queue
from objeto_MRU import CarrinhoMRU

#O widget é criado com FigureCanvasTkAgg e essa função draw() é usada para garantir que o gráfico seja exibido na interface.

def simular(): ##Essa função irá ser chamada quando clicar no botão "simular" na interface
    global carrinho  #Coloquei global, pois tenho que chamar embaixo
    velocidade_constante = float(velocidade_entry.get())
    tempo_simulacao = float(tempo_entry.get())
    
    carrinho = CarrinhoMRU(canvas, grafico_window, velocidade_constante, 1)  # Intervalo de tempo de 1 segundo
    carrinho.criar_carrinho()
    carrinho.criar_regua()
    carrinho.criar_posicao_final()
    carrinho.criar_tempo_label()
    carrinho.simular_movimento(tempo_simulacao)

def resetar(): #A função resetar é chamada quando o botão "Reset" na interface é pressionado.
    velocidade_entry.delete(0, "end")
    tempo_entry.delete(0, "end")
    carrinho.resetar_simulacao()

# Função resetar: é responsável por redefinir a simulação, limpar a fila de posições, reiniciar o tempo e a posição, apagar o carrinho da tela e limpar as entradas de texto na interface. Também recria o gráfico para uma nova simulação.

root = tk.Tk()
root.title("Simulador MRU")

# Frames para organizar a interface
frame_controles = tk.Frame(root)
frame_grafico = tk.Frame(root)

# Configuração dos elementos da interface
velocidade_label = tk.Label(frame_controles, text="Velocidade (m/s):")
velocidade_entry = tk.Entry(frame_controles)
tempo_label = tk.Label(frame_controles, text="Tempo de Simulação (s):")
tempo_entry = tk.Entry(frame_controles)
posicao_label = tk.Label(frame_controles, text="Posição desejada (m):")
posicao_entry = tk.Entry(frame_controles)
simular_button = tk.Button(frame_controles, text="Simular", command=simular)
reset_button = tk.Button(frame_controles, text="Reset", command=resetar)
# verificar_button = tk.Button(root, text="Verificar Tempo", command=verificar_tempo)
grafico_window = tk.Canvas(frame_grafico)
canvas = tk.Canvas(root, width=1000, height=400)

# Posicionamento dos elementos na interface
velocidade_label.grid(row=0, column=0, pady=5)
velocidade_entry.grid(row=0, column=1)
tempo_label.grid(row=1, column=0, pady=5)
tempo_entry.grid(row=1, column=1)
simular_button.grid(row=2, column=0, columnspan=2, pady=10)
reset_button.grid(row=3, column=0, columnspan=2, pady=10)
grafico_window.grid(row=4, column=1, pady=5)


# Posicionamento dos frames na janela principal
frame_controles.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.BOTH)
frame_grafico.pack(side=tk.BOTTOM)

canvas.pack()
root.mainloop()
