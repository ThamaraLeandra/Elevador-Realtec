from collections import deque
from tkinter import Label

tempo_de_espera = { #dicionário 
    'A': 0,
    'B': 0,
}

status_do_elevador = {
    'A' : 0,
    'B': 0 
}

andar_atual = {
    'A' : 0,
    'B': 0 
}

fila = {
    'A' : deque(), 
    'B' : deque(),
    'G' : deque()
}

atualiza_int ={ #somente para a interface gráfica
    'at_A' : 'Aguardando',
    'at_B' : 'Aguardando',
    'di_A' : 'Nenhuma',
    'di_B' : 'Nenhuma',
    'andar_A' : 0,
    'andar_B' : 0
}

ultima_req = {
    'A' : 0,
    'B' : 0
}