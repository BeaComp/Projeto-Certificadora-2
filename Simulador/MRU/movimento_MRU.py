import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from queue import Queue
from MRU.objeto_MRU import CarrinhoMRU


#O widget é criado com FigureCanvasTkAgg e essa função draw() é usada para garantir que o gráfico seja exibido na interface.
def simulacaoMRU(frame):
    def simular(): ##Essa função irá ser chamada quando clicar no botão "simular" na interface
        global carrinho
        
        velocidade_constante = float(velocidade_entry.get())
        tempo_simulacao = float(tempo_entry.get())
        
        carrinho = CarrinhoMRU(canvas, grafico_window, velocidade_constante, 1)  # Intervalo de tempo de 1 segundo
        
        if contador == 1:
            resetar()
    
        carrinho.criar_carrinho()
        carrinho.criar_regua()
        carrinho.criar_posicao_final()
        carrinho.criar_tempo_label()
        carrinho.simular_movimento(tempo_simulacao)

        contador = 1
        

    def resetar(): #A função resetar é chamada quando o botão "Reset" na interface é pressionado.
        velocidade_entry.delete(0, "end")
        tempo_entry.delete(0, "end")
        carrinho.resetar_simulacao()


    # Função resetar: é responsável por redefinir a simulação, limpar a fila de posições, reiniciar o tempo e a posição, apagar o carrinho da tela e limpar as entradas de texto na interface. Também recria o gráfico para uma nova simulação.

   

    # # Frames para organizar a interface
    frame_controles = tk.Frame(frame)
    frame_grafico = tk.Frame(frame)

    # Widget Notebook para abas

   
    # Criação de um frame com scroll dentro da aba

    # Configuração dos elementos da interface
    velocidade_label = tk.Label(frame_controles, text="Velocidade (m/s):")
    velocidade_entry = tk.Entry(frame_controles)
    tempo_label = tk.Label(frame_controles, text="Tempo de Simulação (s):")
    tempo_entry = tk.Entry(frame_controles)
    simular_button = tk.Button(frame_controles, text="Simular", command=simular)
    reset_button = tk.Button(frame_controles, text="Reset", command=resetar)
    stop_button = tk.Button(frame_controles, text="Stop")
    grafico_window = tk.Canvas(frame_grafico)
    canvas = tk.Canvas(frame, width=1000, height=200)

    # Posicionamento dos elementos na interface
    velocidade_label.grid(row=0, column=0, pady=5)
    velocidade_entry.grid(row=0, column=1)
    tempo_label.grid(row=1, column=0, pady=5)
    tempo_entry.grid(row=1, column=1)
    simular_button.grid(row=2, column=0, columnspan=2, pady=5)
    reset_button.grid(row=3, column=0, columnspan=2, pady=5)
    stop_button.grid(row=4, column=0, columnspan=2, pady=5)
    grafico_window.grid(row=4, column=1)


    # Posicionamento dos frames na janela principal
    frame_controles.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.BOTH)
    frame_grafico.pack(side=tk.BOTTOM)

    canvas.pack()
    # frame.mainloop()
