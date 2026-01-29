# Simulação de Elevadores Assíncronos
## Descrição do Projeto

Este projeto consiste em uma simulação de dois elevadores operando de forma assíncrona, utilizando threads para permitir que ambos funcionem simultaneamente sem bloqueio mútuo. O sistema recebe requisições por meio de uma interface gráfica e realiza a distribuição inteligente dessas requisições, buscando minimizar o tempo total de atendimento.

## Funcionamento Geral

Dois valores são informados na interface gráfica:

* Andar atual do usuário

* Andar de destino

Esses valores são armazenados e adicionados a uma fila geral de requisições.

Uma função principal monitora constantemente a fila geral. Sempre que uma nova requisição é identificada, uma thread é criada para realizar a distribuição dessa requisição entre os elevadores disponíveis.

A função de distribuição calcula o tempo estimado para cada elevador atender a requisição, considerando:

* Existência de requisições pendentes na fila do elevador

* Elevador parado sem requisições

* Elevador em movimento sem requisições pendentes

Cada elevador possui uma variável que armazena o tempo total estimado de execução. A requisição é encaminhada para o elevador com menor tempo calculado.

## Controle de Concorrência

* Cada elevador possui sua própria fila de requisições.

* As filas dos elevadores são monitoradas continuamente.

* Caso haja uma requisição disponível:

* Uma thread específica é criada para o elevador correspondente.

* O funcionamento de um elevador não interfere no outro.

Existe uma restrição para criação de threads: uma nova thread do mesmo tipo só pode ser iniciada após a finalização da anterior, evitando conflitos de execução.

## Fluxo de Execução do Elevador

* A thread do elevador chama a função movimenta():

  * Define o status do elevador como "em movimento"

  * Remove a requisição da fila do elevador

  * Armazena a requisição em uma variável de controle

* Em seguida, a função operacao() é executada:

  * Move o elevador do andar atual até o andar solicitado pelo usuário

  * Realiza o deslocamento até o andar de destino

* Simula o tempo de execução com:

  * 2 segundos por andar percorrido

  * 5 segundos para embarque e desembarque

* Durante a execução, são atualizadas variáveis como:

  * Andar atual

  * Status do elevador

  * Estado de movimento

* Ao final da operação:

  * O controle retorna à função movimenta()

  * O estado final do elevador é ajustado

  * A thread é encerrada

  *Caso existam novas requisições, uma nova thread é criada

## Interface Gráfica

A interface gráfica foi desenvolvida utilizando Tkinter. Como o Tkinter não permite a atualização da interface fora da thread principal, foi necessário o uso de variáveis globais para armazenar os estados do sistema.

Uma função executada na thread principal realiza a atualização da interface gráfica a cada 1 segundo, utilizando os valores armazenados nessas variáveis globais.

## Desafios Encontrados

* Comunicação entre threads concorrentes

* Sincronização do estado dos elevadores

* Atualização segura da interface gráfica

* Controle do ciclo de vida das threads

## Decisões de Projeto

Embora o uso de classes pudesse melhorar a organização e reutilização do código, optou-se por não utilizá-las devido ao curto prazo de desenvolvimento e à complexidade envolvida na comunicação entre objetos concorrentes.

Dessa forma, foram utilizadas variáveis globais e dicionários para garantir a estabilidade e o correto funcionamento do sistema dentro do tempo disponível.

## Objetivo

O principal objetivo deste projeto é aplicar conceitos de:

* Programação concorrente

* Uso de threads

* Sistemas assíncronos

* Integração entre lógica de execução e interface gráfica
