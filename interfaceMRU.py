import tkinter as tk
import time

class CarrinhoMRU:
    def __init__(self, canvas, velocidade, intervalo_tempo):
        self.canvas = canvas
        self.velocidade = velocidade
        self.intervalo_tempo = intervalo_tempo
        self.tempo = 0
        self.posicao = 0  # Posição inicial em metros
        self.raio = 10
        self.carrinho = None
        self.régua = None
        self.posicao_final = None

    def criar_carrinho(self):
        x0, y0 = self.posicao - self.raio, 100 - self.raio
        x1, y1 = self.posicao + self.raio, 100 + self.raio
        self.carrinho = self.canvas.create_oval(x0, y0, x1, y1, fill="blue")

    def criar_régua(self):
        self.régua = self.canvas.create_line(0, 120, 600, 120, fill="black", width=2)
        for i in range(11):
            x = 50 + i * 50
            self.canvas.create_line(x, 115, x, 125, fill="black")
            self.canvas.create_text(x, 130, text=str(i * 0.5 + 0.5), fill="black")

    def criar_posicao_final(self):
        self.posicao_final = tk.Label(self.canvas, text="", font=("Arial", 12))
        self.canvas.create_window(300, 160, window=self.posicao_final)

    def atualizar_posicao_final(self):
        self.posicao_final.config(text=f"Posição Final: {self.posicao:.2f} metros")

    def mover_carrinho(self):
        self.posicao += self.velocidade * self.intervalo_tempo
        x0, y0 = self.posicao - self.raio, 100 - self.raio
        x1, y1 = self.posicao + self.raio, 100 + self.raio
        self.canvas.coords(self.carrinho, x0, y0, x1, y1)
        self.atualizar_posicao_final()

    def simular_movimento(self, tempo_simulacao):
        while self.tempo < tempo_simulacao:
            self.mover_carrinho()
            self.canvas.update()
            self.tempo += self.intervalo_tempo
            time.sleep(self.intervalo_tempo)

    def resetar_simulacao(self):
        self.tempo = 0
        self.posicao = 0
        self.canvas.delete(self.carrinho)
        velocidade_entry.delete(0, "end")
        tempo_entry.delete(0, "end")
        # Limpar a posição final
        if self.posicao_final:
            self.posicao_final.config(text="")


def simular():
    global carrinho
    velocidade_constante = float(velocidade_entry.get())
    tempo_simulacao = float(tempo_entry.get())
    
    carrinho = CarrinhoMRU(canvas, velocidade_constante, 1)  # Intervalo de tempo de 1 segundo
    carrinho.criar_carrinho()
    carrinho.criar_régua()
    carrinho.criar_posicao_final()
    carrinho.simular_movimento(tempo_simulacao)

def resetar():
    carrinho.resetar_simulacao()


# Configuração da janela principal
root = tk.Tk()
root.title("Simulador MRU")

# Configuração dos elementos da interface
velocidade_label = tk.Label(root, text="Velocidade (m/s):")
velocidade_entry = tk.Entry(root)
tempo_label = tk.Label(root, text="Tempo de Simulação (s):")
tempo_entry = tk.Entry(root)
simular_button = tk.Button(root, text="Simular", command=simular)
reset_button = tk.Button(root, text="Reset", command=resetar)
canvas = tk.Canvas(root, width=600, height=200)

# Posicionamento dos elementos na interface
velocidade_label.pack()
velocidade_entry.pack()
tempo_label.pack()
tempo_entry.pack()
simular_button.pack()
reset_button.pack()
canvas.pack()

root.mainloop()
