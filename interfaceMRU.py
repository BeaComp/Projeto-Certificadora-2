import tkinter as tk
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from queue import Queue

class CarrinhoMRU:
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
        self.fig, self.ax = plt.subplots()
        self.canvas_widget = FigureCanvasTkAgg(self.fig, master=self.grafico_window)
        self.canvas_widget.get_tk_widget().pack()
        
    

    def criar_carrinho(self):
        x0, y0 = self.posicao - self.raio, 100 - self.raio
        x1, y1 = self.posicao + self.raio, 100 + self.raio
        self.carrinho = self.canvas.create_oval(x0, y0, x1, y1, fill="blue")

    
    def criar_régua(self):
        self.régua = self.canvas.create_line(0, 120, 900, 120, fill="black", width=2)
        for i in range(21):
            x = 50 + i * 50
            self.canvas.create_line(x, 115, x, 125, fill="black")
            self.canvas.create_text(x, 130, text=str(i * 0.5 + 0.5), fill="black")
    

    def criar_posicao_final(self):
        self.posicao_final = tk.Label(self.canvas, text="", font=("Arial", 12))
        self.canvas.create_window(450, 160, window=self.posicao_final)
    
    def criar_tempo_label(self):
        if not self.tempo_label:
            self.tempo_label = tk.Label(self.canvas, text="", font=("Arial", 12))
            self.canvas.create_window(450, 190, window=self.tempo_label)

    def atualizar_posicao_final(self):
        self.posicao_final.config(text=f"Posição Final: {self.posicao:.2f} metros")

    def atualizar_tempo_label(self, tempo):
        self.tempo_label.config(text="Tempo: {:.2f} s".format(tempo))

    def mover_carrinho(self):
        self.posicao += self.velocidade * self.intervalo_tempo
        x0, y0 = self.posicao - self.raio, 100 - self.raio
        x1, y1 = self.posicao + self.raio, 100 + self.raio
        self.canvas.coords(self.carrinho, x0, y0, x1, y1)
        self.posicoes.put(self.posicao)
        self.atualizar_posicao_final()
        self.atualizar_tempo_label(self.tempo)
        self.plot_grafico()


    def simular_movimento(self, tempo_simulacao):
        while self.tempo < tempo_simulacao:
            self.mover_carrinho()
            self.canvas.update()
            self.tempo += self.intervalo_tempo
            time.sleep(self.intervalo_tempo)

    def resetar_simulacao(self):
        while not self.posicoes.empty():
            self.posicoes.get()  # Limpa a fila
        self.tempo = 0
        self.posicao = 0
        self.canvas.delete(self.carrinho)
        velocidade_entry.delete(0, "end")
        tempo_entry.delete(0, "end")
        # Limpar a posição final
        if self.posicao_final:
            self.posicao_final.config(text="")
        if self.tempo_label:
            self.tempo_label.config(text="")
        # Reinicialize o gráfico
        self.fig, self.ax = plt.subplots()
        self.canvas_widget.get_tk_widget().pack()
        self.canvas_widget.get_tk_widget().destroy()
        
    

    def plot_grafico(self):
        self.ax.clear()
        posicoes = list(self.posicoes.queue)  # Converter a fila em uma lista para plotagem
        self.ax.plot(range(len(posicoes)), posicoes)
        self.ax.set_xlabel("Tempo (s)")
        self.ax.set_ylabel("Posição (m)")
        self.ax.set_title("Gráfico MRU")
        self.canvas_widget.draw()    # Atualize o widget do gráfico


    def verificar_tempo(self, posicao_desejada):
        if not self.posicoes.empty():
            while not self.posicoes.empty():
                posicao, tempo = self.posicoes.get()
                if posicao >= posicao_desejada:
                    self.atualizar_tempo_label(f"Tempo para posição {posicao_desejada}m: {tempo:.2f} s")
                    return
        self.atualizar_tempo_label("Posição não alcançada durante a simulação")


def simular():
    global carrinho
    velocidade_constante = float(velocidade_entry.get())
    tempo_simulacao = float(tempo_entry.get())
    
    carrinho = CarrinhoMRU(canvas, grafico_window, velocidade_constante, 1)  # Intervalo de tempo de 1 segundo
    carrinho.criar_carrinho()
    carrinho.criar_régua()
    carrinho.criar_posicao_final()
    carrinho.criar_tempo_label()
    carrinho.simular_movimento(tempo_simulacao)

def resetar():
    carrinho.resetar_simulacao()

def verificar_tempo():
    if not carrinho:
        return
    try:
        posicao_desejada = float(posicao_entry.get())
        carrinho.verificar_tempo(posicao_desejada)
    except ValueError:
        carrinho.atualizar_tempo_label("Digite uma posição válida")


# Configuração da janela principal
root = tk.Tk()
root.title("Simulador MRU")

# Configuração dos elementos da interface
velocidade_label = tk.Label(root, text="Velocidade (m/s):")
velocidade_entry = tk.Entry(root)
tempo_label = tk.Label(root, text="Tempo de Simulação (s):")
tempo_entry = tk.Entry(root)
posicao_label = tk.Label(root, text="Posição desejada (m):")
posicao_entry = tk.Entry(root)
simular_button = tk.Button(root, text="Simular", command=simular)
reset_button = tk.Button(root, text="Reset", command=resetar)
verificar_button = tk.Button(root, text="Verificar Tempo", command=verificar_tempo)
grafico_window = tk.Toplevel(root)
grafico_window.title("Gráfico MRU")
grafico_window.geometry("600x400")
canvas = tk.Canvas(root, width=900, height=250)

# Posicionamento dos elementos na interface
velocidade_label.pack(pady=5)
velocidade_entry.pack()
tempo_label.pack(pady=5)
tempo_entry.pack()
simular_button.pack(pady=10)
reset_button.pack(pady=10)
posicao_label.pack()
posicao_entry.pack()
verificar_button.pack(pady=5)
canvas.pack()

root.mainloop()
