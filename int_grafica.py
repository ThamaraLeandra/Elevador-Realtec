from tkinter import *  #não preciso referenciar todas as funções
from tkinter.font import Font
import threading
from var_compartilhadas import *

def iniciar_interface():
    
    global estado_A, estado_B, atual_A, atual_B, atualiza_int
    lock = threading.Lock()
    
    Janela = Tk()
    Janela.title("Elevadores Realtec")
    Janela.geometry("1440x800")

    fonte_arial = Font(family="Arial", size=12, weight="bold")

    #----------------------------------------------- Estado Atual
    estado_el_A = Label(Janela, text= "Estado atual do elevador A:") #cria um texto na Janela principal
    estado_el_A.place(x=400, y=50, anchor="center") #define a posição na janela, pela quantidade de pixels
     
    estado_A = Label(Janela, text= '') #exibe o estado do elevador A
    estado_A.place(x=400, y=70, anchor="center")

    estado_el_B = Label(Janela, text= "Estado atual do elevador B:") #cria um texto na Janela principal
    estado_el_B.place(x=1040, y=50, anchor="center")

    estado_B = Label(Janela, text= '') #exibe o estado do elevador B
    estado_B.place(x=1040, y=70, anchor="center")
    
    #------------------------------------------------ Direção de movimento - era para ter outro nome mas troquei as bolas 
    andar_at_A = Label(Janela, text= "Direção de movimento do elevador A:") #cria um texto na Janela principal
    andar_at_A.place(x=400, y=150, anchor="center")

    atual_A = Label(Janela, text= "") #exibe o estado do elevador A
    atual_A.place(x=400, y=170, anchor="center")

    andar_at_B = Label(Janela, text= "Direção de movimento do elevador B:") #cria um texto na Janela principal
    andar_at_B.place(x=1040, y=150, anchor="center")

    #atualizar a variável texto_andar_A no código principal
    atual_B = Label(Janela, text= "") 
    atual_B.place(x=1040, y=170, anchor="center")
    
    #------------------------------------------------ Andar atual
    int_andar_A = Label(Janela, text= "Andar atual A:") #cria um texto na Janela principal
    int_andar_A.place(x=400, y=250, anchor="center")

    andar_at_A = Label(Janela, text= "") #exibe o estado do elevador A
    andar_at_A.place(x=400, y=270, anchor="center")

    int_andar_B = Label(Janela, text= "Andar atual B:") #cria um texto na Janela principal
    int_andar_B.place(x=1040, y=250, anchor="center")

    andar_at_B = Label(Janela, text= "") 
    andar_at_B.place(x=1040, y=270, anchor="center")
    
    #------------------------------------------------ Exibe a imagem do elevador
    imagem_A = PhotoImage(file="elevador.png")
    A = Label(Janela, image=imagem_A)
    A.place(x=312, y=300)

    B = Label(Janela, image=imagem_A)
    B.place(x=949, y=300)
    #------------------------------------------------  Requisições
    
    texto_fila_A = Label(Janela, text= "Requisições na fila do elevador A:")
    texto_fila_A.place(x=400, y=520, anchor="center")
    
    fila_A = Label(Janela, text= "") 
    fila_A.place(x=400, y=550, anchor="center")
    
    texto_fila_B = Label(Janela, text= "Requisições na fila do elevador B:")
    texto_fila_B.place(x=1040, y=520, anchor="center")
    
    fila_B = Label(Janela, text= "") 
    fila_B.place(x=1040, y=550, anchor="center")
    
    #------------------------------------------------ Pega o andar
    texto_ler_andar_s = Label(Janela, text= "Digite qual andar você está:")
    texto_ler_andar_s.place(x=400, y=600, anchor="center")
    saida = Entry(Janela, bg= "#D4BCF2", fg= "black", width= 5, font= fonte_arial, justify= "center") #pega o valor do andar
    saida.place(x=400, y=630, anchor="center")  #exibe o campo para puxar o valor


    texto_ler_andar_c = Label(Janela, text= "Digite para qual andar você deseja ir:")
    texto_ler_andar_c.place(x=1040, y=600, anchor="center")
    chegada = Entry(Janela, bg= "#D4BCF2", fg= "black", width= 5, font= fonte_arial, justify= "center")
    chegada.place(x=1040, y=630, anchor="center")

    def le_requisicao():
        try:
            # Captura os valores dos campos de entrada
            andar_saida = int(saida.get())
            andar_chegada = int(chegada.get())
            
            # Valida os valores
            if 0 <= andar_saida <= 10 and 0 <= andar_chegada <= 10:
                chamada = (andar_saida, andar_chegada)
                with lock:
                    fila['G'].append(chamada)  # Adiciona à fila geral
                print(f"Requisição adicionada: {chamada}")
                
                saida.delete(0, END)  # Limpa o campo de entrada
                chegada.delete(0, END)  # Limpa o campo de entrada
                
            else:
                print("Favor selecionar andares válidos entre 0 e 10.")
        except ValueError:
            print("Por favor, insira números válidos nos campos.")


    botao = Button(Janela, text= "SOLICITAR", command= le_requisicao,bg= "#77509A", fg= "white", width= 15, height= 2, font= fonte_arial)
    botao.place(x= 700, y=700, anchor="center")

    #----------------------------------------------- Atualiza a interface
    
    def att_interface():
        estado_A['text'] = atualiza_int['at_A']
        estado_B['text'] = atualiza_int['at_B']
        atual_A['text'] = atualiza_int['di_A']
        atual_B['text'] = atualiza_int['di_B']
        andar_at_A['text'] = atualiza_int['andar_A']
        andar_at_B['text'] = atualiza_int['andar_B']
        fila_A['text'] = fila['A']
        fila_B['text'] = fila['B']
        Janela.after(1000, att_interface)

    att_interface()
    
    Janela.mainloop() #não deixa a janela fechar