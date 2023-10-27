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
        self.alturas = Queue()  # Fila para armazenar as alturas ao longo do tempo
        self.fig, self.ax = plt.subplots()
        self.canvas_widget = FigureCanvasTkAgg(self.fig, master=self.grafico_window)
        self.canvas_widget.get_tk_widget().pack()

    def criar_altura_final_label(self):
        self.altura_final_label = tk.Label(self.canvas, text="", font=("Arial", 12))
        self.canvas.create_window(450, 160, window=self.altura_final_label)

    def criar_tempo_label(self):
        if not self.tempo_label:
            self.tempo_label = tk.Label(self.canvas, text="", font=("Arial", 12))
            self.canvas.create_window(450, 190, window=self.tempo_label)

    def atualizar_altura_final(self):
        self.altura_final_label.config(text=f"Altura Final: {self.altura:.2f} metros")

    def atualizar_tempo_label(self, tempo):
        self.tempo_label.config(text="Tempo: {:.2f} s".format(tempo))

    def mover_objeto(self):
        g = 9.81  # Aceleração devido à gravidade (m/s^2)
        self.altura = self.altura_inicial - (0.5 * g * self.tempo**2)
        self.alturas.put(self.altura)
        self.atualizar_altura_final()
        self.atualizar_tempo_label(self.tempo)
        self.plot_grafico()

    def simular_queda(self):
        while self.altura >= 0:
            self.mover_objeto()
            self.canvas.update()
            self.tempo += self.intervalo_tempo
            time.sleep(self.intervalo_tempo)

    def resetar_simulacao(self):
        while not self.alturas.empty():
            self.alturas.get()  # Limpa a fila
        self.tempo = 0
        self.altura = self.altura_inicial
        altura_inicial_entry.delete(0, "end")
        if self.altura_final_label:
            self.altura_final_label.config(text="")
        if self.tempo_label:
            self.tempo_label.config(text="")
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

# Funções para interagir com a interface
def simular_queda():
    global queda_livre
    altura_inicial = float(altura_inicial_entry.get())
    
    queda_livre = QuedaLivre(canvas, grafico_window, altura_inicial, 0.001)  # Intervalo de tempo de 0.001 segundos
    queda_livre.criar_altura_final_label()
    queda_livre.criar_tempo_label()
    queda_livre.simular_queda()

def resetar_simulacao():
    queda_livre.resetar_simulacao()

# Configuração da janela principal
root = tk.Tk()
root.title("Simulador de Queda Livre")

# Configuração dos elementos da interface
altura_inicial_label = tk.Label(root, text="Altura Inicial (m):")
altura_inicial_entry = tk.Entry(root)
simular_button = tk.Button(root, text="Simular", command=simular_queda)
reset_button = tk.Button(root, text="Resetar", command=resetar_simulacao)
grafico_window = tk.Toplevel(root)
grafico_window.title("Gráfico de Queda Livre")
grafico_window.geometry("600x400")
canvas = tk.Canvas(root, width=900, height=300)

# Posicionamento dos elementos na interface
altura_inicial_label.pack(pady=5)
altura_inicial_entry.pack()
simular_button.pack(pady=10)
reset_button.pack(pady=10)
canvas.pack()

root.mainloop()

