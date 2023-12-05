import tkinter as tk
from MUV.objeto_MUV import QuedaLivre
from tkinter import messagebox

queda_livre = None

def simulacaoMUV(frame):
    queda_livre = None

# Funções para interagir com a interface
    def simular_queda():
        global queda_livre

        try:
            altura_inicial = float(altura_inicial_entry.get())
        except ValueError:
            # Se a conversão para float falhar (por exemplo, se o usuário inserir texto em vez de números)
            messagebox.showerror("Erro", "Por favor, insira valores numéricos para a altura.")
            altura_inicial_entry.delete(0, "end")
            return  # Encerre a função em caso de erro

        try:
            if queda_livre:
                altura_inicial_entry.delete(0, "end")
                queda_livre.resetar_simulacao()
                queda_livre = None
            else:
                queda_livre = QuedaLivre(canvas, grafico_window, altura_inicial, 0.01)  
                queda_livre.criar_altura_final_label()
                queda_livre.criar_tempo_label()
                queda_livre.criar_aceleracao_label()
                queda_livre.criar_velocidade_label()
                queda_livre.simular_queda()
        except Exception as e:
            # Trate qualquer outra exceção que possa ocorrer durante a inicialização do carrinho
            messagebox.showerror("Erro", f"Ocorreu um erro durante a inicialização: {e}")
            return  # Encerre a função em caso de erro

    # Frames para organizar a interface
    frame_controles = tk.Frame(frame)
    frame_grafico = tk.Frame(frame)

    # Configuração dos elementos da interface
    altura_inicial_label = tk.Label(frame_controles, text="Altura Inicial (m):")
    altura_inicial_entry = tk.Entry(frame_controles)
    simular_button = tk.Button(frame_controles, text="Simular/Resetar", command=simular_queda)
    grafico_window = tk.Canvas(frame_grafico)
    canvas = tk.Canvas(frame, width=400, height=300)

    # Posicionamento dos elementos na interface
    altura_inicial_label.grid(row=0, column=0, pady=5)
    altura_inicial_entry.grid(row=0, column=1)
    simular_button.grid(row=1, column=0, columnspan=2, pady=5)
    grafico_window.grid(row=3, column=1, pady=5)

    frame_controles.pack(side=tk.LEFT, padx=5)
    frame_grafico.pack(side=tk.RIGHT, pady= 5)

    canvas.pack()

