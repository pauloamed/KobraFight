from kobra_fight.balancer import Balancer, RoundRobin
import signal
import sys

balancer = None

def SIGINT_handler(sig_number, sig_stack):
    global balancer
    balancer.delServer()
    exit()

signal.signal(signal.SIGINT, SIGINT_handler)

def main():
    global balancer

    param = sys.argv[1:]
    port = int(param[0])
    maxClients = int(param[1])
    btype = param[2]

    if btype == 'vanilla':
        balancer = Balancer(port, maxClients)
    elif btype == 'roundrobin':
        numservers = int(param[3])
        balancer = RoundRobin(port, maxClients, numservers)
    else:
        print(">>> Unknown param\n>>> Exiting")
        exit()

    balancer.run()


main()
