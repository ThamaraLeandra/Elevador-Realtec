from lib_elevador import *
import threading
from int_grafica import iniciar_interface

thread_A = None
thread_B = None
thread_Geral = None
thread_interface = None

#thread da interface, só cria 1 pq não está em loop
thread_interface = threading.Thread(target=iniciar_interface)
thread_interface.start()

while True:

    req_geral = Verifica_Fila('G')
    if req_geral!= 0 and (thread_Geral is None or not thread_Geral.is_alive()): #se tem algo na fila das requisições gerais e se a thread não foi iniciadada, garnte que somente uma thread desse tipo vá executar
        #inicia uma thread para movimentar um elevador
        thread_Geral= threading.Thread(target=Distribui_Requisicoes, args=()) 
        thread_Geral.start()
        
    req_A = Verifica_Fila('A')
    if req_A != 0 and (thread_A is None or not thread_A.is_alive()): #se tiver algo na fila do elevador A vai chamar a função para movimentar o elevador
        #inicia uma thread para movimentar um elevador
        thread_A = threading.Thread(target=movimenta, args=('A')) 
        thread_A.start()
        
    req_B = Verifica_Fila('B') 
    if req_B != 0 and (thread_B is None or not thread_B.is_alive()): #se tiver algo na fila do elevador B vai chamar a função para movimentar o elevador 
        #inicia uma thread para movimentar um elevador
        thread_B = threading.Thread(target=movimenta, args=('B')) 
        thread_B.start()