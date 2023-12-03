import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from queue import Queue
from MUV.objeto_MUV import QuedaLivre

def simulacaoMUV(frame):
# Funções para interagir com a interface
    def simular_queda():
        global queda_livre
        altura_inicial = float(altura_inicial_entry.get())
        
        queda_livre = QuedaLivre(canvas, grafico_window, altura_inicial, 0.001)  # Intervalo de tempo de 0.001 segundos
        queda_livre.criar_altura_final_label()
        queda_livre.criar_tempo_label()
        queda_livre.simular_queda()

    def resetar_simulacao():
        altura_inicial_entry.delete(0, "end")
        queda_livre.resetar_simulacao()

    # Configuração da janela principal
    root = tk.Tk()
    root.title("Simulador Queda Livre")

    # Frames para organizar a interface
    frame_controles = tk.Frame(root)
    frame_grafico = tk.Frame(root)

    # Configuração dos elementos da interface
    altura_inicial_label = tk.Label(frame_controles, text="Altura Inicial (m):")
    altura_inicial_entry = tk.Entry(frame_controles)
    simular_button = tk.Button(frame_controles, text="Simular", command=simular_queda)
    reset_button = tk.Button(frame_controles, text="Resetar", command=resetar_simulacao)
    grafico_window = tk.Canvas(frame_grafico)
    canvas = tk.Canvas(root, width=400, height=300)

    # Posicionamento dos elementos na interface
    altura_inicial_label.grid(row=0, column=0, pady=5)
    altura_inicial_entry.grid(row=0, column=1)
    simular_button.grid(row=1, column=0, columnspan=2, pady=5)
    reset_button.grid(row=2, column=0, columnspan=2, pady=5)
    grafico_window.grid(row=3, column=1, pady=5)

    frame_controles.pack(side=tk.LEFT, padx=5)
    frame_grafico.pack(side=tk.RIGHT, pady= 5, padx=50)

    canvas.pack()

    # root.mainloop()

