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

    # balancer = RoundRobin(port, 2)
    balancer = Balancer(port)
    # signal.signal(signal.SIGINT, balancer.stop)
    balancer.run()


main()
