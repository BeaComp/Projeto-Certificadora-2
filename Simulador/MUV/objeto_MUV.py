import tkinter as tk
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from queue import Queue


class QuedaLivre:
    def __init__(self, canvas, grafico_window, altura_inicial, intervalo_tempo):
        self.canvas = canvas
        self.grafico_window = grafico_window
        self.altura_inicial = altura_inicial
        self.intervalo_tempo = intervalo_tempo
        self.tempo = 0
        self.altura = altura_inicial
        self.raio = 10
        self.objeto = None
        self.chao = None
        self.altura_final_label = None
        self.tempo_label = None
        self.aceleracao_label = None
        self.velocidade_label = None
        self.alturas = Queue()  # Fila para armazenar as alturas ao longo do tempo
        self.fig, self.ax = plt.subplots()
        self.canvas_widget = FigureCanvasTkAgg(self.fig, master=self.grafico_window)
        self.canvas_widget.get_tk_widget().pack()
        
    def criar_aceleracao_label(self):
        if not self.aceleracao_label:
            self.aceleracao_label = tk.Label(self.canvas, text="", font=("Arial", 12))
            self.canvas.create_window(250, 220, window=self.aceleracao_label)

    def atualizar_aceleracao_label(self):
        self.aceleracao_label.config(text="Acelereção: 9.81 m/s²")
    
    def criar_velocidade_label(self):
        if not self.velocidade_label:
            self.velocidade_label = tk.Label(self.canvas, text="", font=("Arial", 12))
            self.canvas.create_window(250, 250, window=self.velocidade_label)

    def atualizar_velocidade_label(self, tempo):
        g = 9.81
        velocidade_final = g * tempo
        self.velocidade_label.config(text=f"Velocidade Final: {velocidade_final:.2f} metros/s")
    

    def criar_altura_final_label(self):
        self.altura_final_label = tk.Label(self.canvas, text="", font=("Arial", 12))
        self.canvas.create_window(250, 160, window=self.altura_final_label)

    def criar_tempo_label(self):
        if not self.tempo_label:
            self.tempo_label = tk.Label(self.canvas, text="", font=("Arial", 12))
            self.canvas.create_window(250, 190, window=self.tempo_label)

    def atualizar_altura_final(self):
        self.altura_final_label.config(text=f"Altura Final: {self.altura:.2f} metros")

    def atualizar_tempo_label(self, tempo):
        self.tempo_label.config(text="Tempo: {:.2f} s".format(tempo))

    def mover_objeto(self):
        g = 9.81  # Aceleração devido à gravidade (m/s^2)
        self.altura2 = self.altura_inicial - (0.5 * g * self.tempo**2)
        if self.altura2 > 0:
            self.altura = self.altura2
            self.alturas.put(self.altura)
            self.atualizar_altura_final()
            self.atualizar_tempo_label(self.tempo)
            self.atualizar_aceleracao_label()
            self.atualizar_velocidade_label(self.tempo)
            self.plot_grafico()
        else:
           self.altura = 0
            
    def simular_queda(self):
        while self.altura >= 0:
            self.mover_objeto()
            self.canvas.update()
            self.tempo += self.intervalo_tempo
            time.sleep(self.intervalo_tempo)

    def resetar_simulacao(self):
        while not self.alturas.empty():
            self.alturas.get()  # Limpa a fila

        self.intervalo_tempo = 0
        self.altura_inicial = 0

        if self.altura_final_label:
            self.altura_final_label.config(text="")
        if self.tempo_label:
            self.tempo_label.config(text="")
        if self.aceleracao_label:
            self.aceleracao_label.config(text="")
        if self.velocidade_label:
            self.velocidade_label.config(text="")
        # Reinicialize o gráfico
        self.fig, self.ax = plt.subplots()
        self.canvas_widget.get_tk_widget().pack()
        self.canvas_widget.get_tk_widget().destroy()

    def plot_grafico(self):
        self.ax.clear()
        alturas = list(self.alturas.queue)  # Converter a fila em uma lista para plotagem
        self.ax.plot(range(len(alturas)), alturas)
        self.ax.set_xlabel("Tempo (s)")
        self.ax.set_ylabel("Altura (m)")
        self.ax.set_title("Gráfico de Queda Livre")
        self.canvas_widget.draw()  # Atualize o widget do gráfico