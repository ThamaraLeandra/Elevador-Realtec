import time
from collections import deque
import threading
from var_compartilhadas import *
from int_grafica import *

lock = threading.Lock()

#Verifica a Fila, retorna 0 se estiver vazia
def Verifica_Fila(tipo_fila):
    with lock:
        if(len(fila[tipo_fila])==0): #len retorna o tamanho da fila
            return 0
        else:
            return 1
    
# Inicialmente as requisições são adicionadas em uma fila geral para depois ser distribuidas
# O algoritmo para a distribuição das requisições para os respectivos elevadores leva em consideração o menor tempo que o elevador vai gastar para chegar no andar que foi 
# requisitado, ex: o cliente disse que está no andar 6 então será considerado o tempo que o elevador vai gastar para terminar as requisições que estão na sua fila + 
# o tempo gasto do último andar da última requisição até o andar 6, que foi o solicitado
# Então a requisição vai para a fila do elevador que gastar menos tempo
    
def Distribui_Requisicoes(): #Distribui as requisições da fila geral
    global tempo_de_espera, fila, andar_atual
    
    with lock:
        requisicao_atual = fila['G'].popleft()
    andar_saida, andar_chegada = requisicao_atual #desempacota a tupla e coloca em duas variáveis, uma do andar de saída e outro o de chegada
    
    if Verifica_Fila('A') !=0:
        ultima_req_A = fila['A'][-1] #Pega o último andar da última requisição da sua fila para fazer o cálculo do tempo
    elif Verifica_Fila('A') == 0 and status_do_elevador['A'] == 0: #A fila está vazia e o elevador parado, pega o andar atual do elevador
        ultima_req_A = (0,andar_atual['A']) #Caso não tenha requisições na fila, pega o andar que o elevador está parado
    else:
        ultima_req_A = (0, ultima_req['A']) #Caso não tenha requisições na fila mas o elevador está em movimento, vai pegar o ultimo andar da requisição
        
    if Verifica_Fila('B') != 0:
        ultima_req_B = fila['B'][-1]
    elif Verifica_Fila('B') == 0 and status_do_elevador['B'] == 0:
        ultima_req_B = (0,andar_atual['B'])
    else:
         ultima_req_B = (0, ultima_req['B'])
        
    tempo_A = abs(ultima_req_A[1] - andar_saida) * 2 + tempo_de_espera['A'] #calcula o tempo de cada elevador 
    tempo_B = abs(ultima_req_B[1] - andar_saida) * 2 + tempo_de_espera['B'] 
    print("tempo de espera de A:", tempo_de_espera['A'])
    print("tempo de espera de B:", tempo_de_espera['B'])
    #faz uma verificacao para saber qual elevador está mais perto, o abs retorna o valor absoluto da diferença entre os andares atuais dos elevadores e o de chamada
    if(tempo_A <= tempo_B): #se o elevador A estiver mais perto ou a diferença entre A e B for a mesma, coloca a requisição na fila do A
        with lock:
            ultima_req['A'] = requisicao_atual[1]
            fila['A'].append(requisicao_atual)
            tempo_de_espera['A'] = tempo_A + abs(andar_saida - andar_chegada) * 2 + 10  #atualiza o novo tempo de espera com o valor do tempo para chegar até o andar de saída  e o de chegada 
    else:
        with lock:
            ultima_req['B'] = requisicao_atual[1]
            fila['B'].append(requisicao_atual)
            tempo_de_espera['B'] = tempo_B + abs(andar_saida - andar_chegada) * 2 + 10 

def movimenta(elevador):
    global status_do_elevador, andar_atual, fila, atualiza_int
    
    while status_do_elevador[elevador] == 0 and Verifica_Fila(elevador) != 0:
        with lock:
            status_do_elevador[elevador] = 1 #elevador em movimento ou em uso
            req_atendida = fila[elevador].popleft() #Remove a primeira tupla da fila e adiciona na variável req_atendida
            
        andar_saida, andar_chegada = req_atendida #desempacota a tupla e coloca em duas variáveis, uma do andar de saída e outro o de chegada
    
        if (elevador == 'A'):
            
            with lock:
                atualiza_int['at_A'] = "Em movimento" 
            andar = operacao(andar_atual['A'], andar_saida, elevador)
            andar = operacao(andar, andar_chegada, elevador)  #o andar atual só vai ser atualizado quando o elevador terminar de atender a requisição, não atrapalha o cáulculo do tempo na função distibui requisições pois só considera o andar atual se esetiver parado
            with lock:
                status_do_elevador['A'] = 0 #elevador aguardando nova requisição
                andar_atual['A'] = andar
                atualiza_int['andar_A'] = andar
                atualiza_int['at_A'] = "Parado"
            
        elif(elevador == 'B'):
            with lock:
                atualiza_int['at_B'] = "Em movimento"
            andar = operacao(andar_atual['B'], andar_saida, elevador)
            andar = operacao(andar, andar_chegada, elevador)
            with lock: #isso atualiza as variáveis globais depois de fazer a movimentação
                status_do_elevador['B'] = 0
                andar_atual['B'] = andar
                atualiza_int['andar_B'] = andar
                atualiza_int['at_B'] = "Parado"
        
def operacao(andar_atual, andar_prox, elevador): #fiquei sem ideia para o nome da funcao, mas ela de fato faz a movimentação dos elevadores
    andar = andar_atual #não vou alterar a variável andar atual, até que a movimentação termine
    if(andar_atual < andar_prox):
        #subir
        #print('O elevador', elevador, "está subindo")
        while andar != andar_prox:
            andar +=1
            with lock:
                att_var(elevador, 'Em movimento', 'Subindo', andar)  
            print('Andar atual do elevador', elevador, ': ', andar)
            simula_tempo(2, elevador)
        with lock:
            att_var(elevador, 'Parado', 'Aguardando', andar) #isso atualiza as variáveis globais enquanto o elevador está movimentado 
        simula_tempo(5, elevador)
        
    elif(andar_atual > andar_prox):
        #descer
        while andar != andar_prox:
            andar -=1
            with lock:
                att_var(elevador, 'Em movimento', 'Descendo', andar) 
            #print('Andar atual do elevador', elevador, ': ', andar)
            simula_tempo(2, elevador)
        with lock:
            att_var(elevador, 'Parado', 'Aguardando', andar)
        simula_tempo(5, elevador)
    else:
        #abrir as porta
        with lock:
            att_var(elevador, 'Parado', 'Aguardando', andar) 
        simula_tempo(5, elevador)
    return andar

def simula_tempo(tempo, elevador): #simula o passar o tempo e decrementa da variável tempo de espera do elevador
    global tempo_de_espera
    
    for _ in range (tempo):
        time.sleep(1)
        with lock:
            tempo_de_espera[elevador] -= 1 
    

def att_var(elevador, status, movimento, andar): #atualiza o valor das variáveis globais que são exibidas na interface
    if elevador == 'A':
        atualiza_int['di_A'] = movimento
        atualiza_int['at_A'] = status
        atualiza_int['andar_A'] = andar 
    else:
        atualiza_int['di_B'] = movimento
        atualiza_int['at_B'] = status
        atualiza_int['andar_B'] = andar 
    
