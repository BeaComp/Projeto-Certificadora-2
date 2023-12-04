from tkinter  import *
from tkinter import ttk
from tkinter import scrolledtext
from MRU.movimento_MRU import simulacaoMRU 
from MUV.interfaceMUV import simulacaoMUV


root = Tk()
root.title("Simulador de Movimentos de Física")

# Widget Notebook para abas
notebook = ttk.Notebook(root)

# Aba 1
janela1 = Frame(notebook)
notebook.add(janela1, text="Movimento MRU") 
movimentoMRU = simulacaoMRU(janela1) # Adiciona a simulação MRU na aba 1

# Aba 2
janela2 = Frame(notebook)
notebook.add(janela2, text="Movimento MUV")
movimentoMUV = simulacaoMUV(janela2)

notebook.pack(expand=True, fill=BOTH)


root.mainloop()
