import tkinter as tk
from tkinter import messagebox
from MRU.objeto_MRU import CarrinhoMRU

carrinho = None

#O widget é criado com FigureCanvasTkAgg e essa função draw() é usada para garantir que o gráfico seja exibido na interface.
def simulacaoMRU(frame):
    # carrinho = None

    def simular():
        global carrinho

        try:
            velocidade_constante = float(velocidade_entry.get())
            tempo_simulacao = float(tempo_entry.get())
        except ValueError:
            # Se a conversão para float falhar (por exemplo, se o usuário inserir texto em vez de números)
            messagebox.showerror("Erro", "Por favor, insira valores numéricos para velocidade e tempo.")
            return  # Encerre a função em caso de erro

        try:
            # Verifique se o carrinho já foi inicializado
            if carrinho:
                velocidade_entry.delete(0, "end")
                tempo_entry.delete(0, "end")
                carrinho.resetar_simulacao()
                carrinho = None
            else:
                carrinho = CarrinhoMRU(canvas, grafico_window, velocidade_constante, 1)
                carrinho.criar_carrinho()
                carrinho.criar_regua()
                carrinho.criar_posicao_final()
                carrinho.criar_tempo_label()
                carrinho.criar_velocidade_label()
                carrinho.simular_movimento(tempo_simulacao)
        except Exception as e:
            # Trate qualquer outra exceção que possa ocorrer durante a inicialização do carrinho
            messagebox.showerror("Erro", f"Ocorreu um erro durante a inicialização do carrinho: {e}")
            return  # Encerre a função em caso de erro

    # # Frames para organizar a interface
    frame_controles = tk.Frame(frame)
    frame_grafico = tk.Frame(frame)

    # Configuração dos elementos da interface
    velocidade_label = tk.Label(frame_controles, text="Velocidade (m/s):")
    velocidade_entry = tk.Entry(frame_controles)
    tempo_label = tk.Label(frame_controles, text="Tempo de Simulação (s):")
    tempo_entry = tk.Entry(frame_controles)
    simular_button = tk.Button(frame_controles, text="Simular/Resetar", command=simular)
    stop_button = tk.Button(frame_controles, text="Stop")
    grafico_window = tk.Canvas(frame_grafico)
    canvas = tk.Canvas(frame, width=1000, height=200)

    # Posicionamento dos elementos na interface
    velocidade_label.grid(row=0, column=0, pady=5)
    velocidade_entry.grid(row=0, column=1)
    tempo_label.grid(row=1, column=0, pady=5)
    tempo_entry.grid(row=1, column=1)
    simular_button.grid(row=2, column=0, columnspan=2, pady=5)
    stop_button.grid(row=3, column=0, columnspan=2, pady=5)
    grafico_window.grid(row=2, column=1)


    # Posicionamento dos frames na janela principal
    frame_controles.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.BOTH)
    frame_grafico.pack(side=tk.BOTTOM)

    canvas.pack()
    # frame.mainloop()
