from tkinter  import *
from tkinter import ttk
from tkinter import scrolledtext
from MRU.movimento_MRU import simulacaoMRU 
from MUV.interfaceMUV import simulacaoMUV


root = Tk()
root.title("Simulador de Movimentos de Física")
root.geometry("1000x900")

# Widget Notebook para abas
notebook = ttk.Notebook(root)

# Aba 1
janela1 = Frame(notebook)
notebook.add(janela1, text="Movimento MRU") 
movimento = simulacaoMRU(janela1) # Adiciona a simulação MRU na aba 1

# Aba 2
movimentoMUV = Frame(notebook)
notebook.add(movimentoMUV, text="Movimento MUV")
# janela2 = simulacaoMUV(movimentoMUV)

notebook.pack(expand=True, fill=BOTH)
# janela1.mainloop()


root.mainloop()
