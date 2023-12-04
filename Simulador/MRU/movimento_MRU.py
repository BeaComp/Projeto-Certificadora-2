import tkinter as tk
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from queue import Queue
from tkinter import messagebox
import numpy as np



carrinho = None

class CarrinhoMRU:  # Classe que inicia as propriedades do carrinho e do simulador (obs: vou dividir em duas classes: info do carrinho e infos da interface)
    def __init__(self, canvas, grafico_window, velocidade, intervalo_tempo):
        self.canvas = canvas
        self.grafico_window = grafico_window
        self.velocidade = velocidade
        self.intervalo_tempo = intervalo_tempo
        self.tempo = 0
        self.posicao = 0  # Posição inicial em metros
        self.raio = 10
        self.carrinho = None
        self.régua = None
        self.posicao_final = None
        self.tempo_label = None
        self.posicoes = Queue()  # Fila para armazenar as posições ao longo do tempo
        self.fig, self.ax = plt.subplots(figsize=(7, 4))
        self.canvas_widget = FigureCanvasTkAgg(self.fig, master=self.grafico_window)
        self.canvas_widget.get_tk_widget().pack()
        
    # Funções para criar a bolinha ('carrinho'), os itens do gráfico e simular o movimento

    def criar_carrinho(self): # Cria a bolinha, que simboliza o carrinho
        x0, y0 = self.posicao - self.raio, 100 - self.raio
        x1, y1 = self.posicao + self.raio, 100 + self.raio
        self.carrinho = self.canvas.create_oval(x0, y0, x1, y1, fill="blue")

    
    def criar_regua(self): #Função para criar a labelregua 
        self.régua = self.canvas.create_line(0, 120, 1200, 120, fill="black", width=2)
        for i in range(21):
            x = 50 + i * 50
            self.canvas.create_line(x, 115, x, 125, fill="black")
            self.canvas.create_text(x, 130, text=str(i * 0.5 + 0.5), fill="black") #A regua vai de 0.5 a 0.5
    

    def criar_posicao_final(self): #Função para criar a label 
        if not self.posicao_final:
            self.posicao_final = tk.Label(self.canvas, text="", font=("Arial", 10))
            self.canvas.create_window(450, 160, window=self.posicao_final)
    
    def criar_tempo_label(self): #Função para criar a label 
        if not self.tempo_label:
            self.tempo_label = tk.Label(self.canvas, text="", font=("Arial", 10))
            self.canvas.create_window(450, 190, window=self.tempo_label)

    def atualizar_posicao_final(self): #Fica aparecendo a posição na tela
        self.posicao_final.config(text=f"Posição Final: {self.posicao:.2f} metros")

    def atualizar_tempo_label(self, tempo): #Fica aparecendo o tempo na tela
        # tempo = tempo + 1
        self.tempo_label.config(text="Tempo: {:.2f} s".format(tempo))


    def mover_carrinho(self, tempo_simulacao): # É responsável por atualizar a posição do carrinho
        self.posicao += self.velocidade * self.intervalo_tempo
        x0, y0 = self.posicao - self.raio, 100 - self.raio
        x1, y1 = self.posicao + self.raio, 100 + self.raio
        self.canvas.coords(self.carrinho, x0, y0, x1, y1)
        self.posicoes.put(self.posicao)
        self.criar_posicao_final()
        self.atualizar_posicao_final() #Atualizar o rótulo que exibe a posição final do carrinho na interface gráfica.
        self.atualizar_tempo_label(self.tempo + 1) #Atualizar o rótulo que exibe a tempo do carrinho na interface gráfica.
        self.plot_grafico(tempo_simulacao) #Plota o gráfico que mostra a posição do carrinho ao longo do tempo


    #Esta função recebe dois argumentos, self (que se refere à instância da classe CarrinhoMRU) e tempo_simulacao, que é o tempo total de simulação desejado.
    def simular_movimento(self, tempo_simulacao):
        temps = tempo_simulacao
        print(temps)
        while self.tempo < tempo_simulacao:
            self.mover_carrinho(tempo_simulacao) #A cada iteração do loop, a função chama o método mover_carrinho
            self.canvas.update() #Esta linha atualiza o canvas da interface gráfica. Ele acompanha o movimento
            self.tempo += self.intervalo_tempo
            time.sleep(self.intervalo_tempo) #Isso controla a velocidade da simulação



    def resetar_simulacao(self): #Reseta tudo, limpa os campos e exclui o grafico
        while not self.posicoes.empty():
            self.posicoes.get()  # Limpa a fila
        self.tempo = 0
        self.posicao = 0
        
        if self.carrinho:
            self.canvas.delete(self.carrinho)
        
        # Limpar a posição final
        if self.posicao_final:
            self.posicao_final.config(text="")
        if self.tempo_label:
            self.tempo_label.config(text="")

        # # Reinicialize o gráfico
        self.fig, self.ax = plt.subplots()
        self.canvas_widget.get_tk_widget().pack()
        self.canvas_widget.get_tk_widget().destroy()
        
    def plot_grafico(self, tempo_simulacao): #Essa função cria o gráfico
        self.ax.clear()  # Limpe o gráfico atual
        posicoes = list(self.posicoes.queue)  # Converta a fila em uma lista para plotagem

        # Reduza o número de pontos no gráfico para evitar densidade excessiva
        num_pontos_grafico = min(len(posicoes), 100)

        # Calcule os tempos para o gráfico usando linspace
        tempos_grafico = np.linspace(0, tempo_simulacao, num_pontos_grafico)

        # Plotar o gráfico usando os tempos do gráfico e as posições reais
        self.ax.plot(tempos_grafico, posicoes[:num_pontos_grafico])
        
        self.ax.set_xlabel("Tempo (s)")
        self.ax.set_ylabel("Posição (m)")
        self.ax.set_title("Gráfico MRU")
        self.canvas_widget.draw()  # Atualize o widget do gráfico

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
                carrinho.simular_movimento(tempo_simulacao)
        except Exception as e:
            # Trate qualquer outra exceção que possa ocorrer durante a inicialização do carrinho
            messagebox.showerror("Erro", f"Ocorreu um erro durante a inicialização do carrinho: {e}")
            return  # Encerre a função em caso de erro

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
