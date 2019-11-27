# KobraFight
## Descrição
Implementação do jogo KobraFight com suporte para multiplayer online. A implementação

## Requisitos
A fim de instalar os pacotes `python` necessários para execução do projeto, utilize
```
pip install -r requirements.txt
```

## Execução do balançeador
Para executar o balançeador padrão, execute
```
python balancer.py [PORT] [MAXCLIENTS] vanilla
```
Para executar o balançeador RoundRobin, execute
```
python balancer.py [PORT] [MAXCLIENTS] roundrobin [NUMSERVERS]
```
- `[PORT]`: porta que o *socket* do balançeador utilizará para se comunicar com os clientes
- `[MAXCLIENTS]`: quantidade máxima de clientes suportados pelos *Servers*
- `[NUMSERVERS]`: quantidade de servers a serem instanciados no RoundRobin

## Execução do cliente
Para executar o cliente, execute
```
python client.py [PORT] [CLIENT_ID]
```
- `[PORT]`: porta sendo utilizada pelo *socket* do balançeador
- `[CLIENT_ID]`: *id* do cliente, deve ser único para cada cliente

### Autores
- Daniel Guerra
- Gabriel Queiroz
- Paulo Augusto
