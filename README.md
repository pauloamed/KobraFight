# KobraFight

## Descrição
Implementação de um snake-game em `python` utilizando o pacote `pygame`, com suporte para multiplayer online.
O jogo também conta com um [balanceador de cargas](https://pt.wikipedia.org/wiki/Balanceamento_de_carga)
para melhor gerenciar as conexões existentes e aplicáveis. Este snake-game dispõe de um tabuleiro onde
os diferentes jogadores, *cobras*, irão competir para ver quem consome mais alimentos, tendo cuidado com os obstáculos.

## Requisitos
A fim de instalar os pacotes `python` necessários para execução do projeto, utilize:
```
pip install -r requirements.txt
```
### Execução

Para rodar o programa:

## Execução do balançeador

Existem duas opções de balanceador. A padrão sendo pensada e criada pelo grupo, com direcionamentos do professor
[Júlio](https://github.com/juliocpmelo), e uma pega da literatura baseada na técnica [Round-Robin](https://www.somosagility.com.br/balanceamento-de-carga-baseado-no-metodo-round-robin/)

Para executar o balançeador padrão, execute:
```
python3 balancer.py [PORT] [MAXCLIENTS] vanilla
```
Para executar o balanceador Round-Robin, execute:
```
python3 balancer.py [PORT] [MAXCLIENTS] roundrobin [NUMSERVERS]
```
- `[PORT]`: porta que o *socket* do balançeador utilizará para se comunicar com os clientes
- `[MAXCLIENTS]`: quantidade máxima de clientes suportados pelos *Servers*
- `[NUMSERVERS]`: quantidade de servers a serem instanciados no RoundRobin

## Execução do cliente

Para conectar um cliente, execute:
```
python3 client.py [PORT] [CLIENT_ID]
```
- `[PORT]`: porta sendo utilizada pelo *socket* do balançeador
- `[CLIENT_ID]`: *id* do cliente, deve ser único para cada cliente

### Autores

- [@Daniel Guerra](https://github.com/Codigos-de-Guerra)
- [@Gabriel Queiroz](https://github.com/gabriel-igorq)
- [@Paulo Augusto](https://github.com/pauloamed)
