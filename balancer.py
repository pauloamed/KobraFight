from kobra_fight.balancer import Balancer, RoundRobin
import signal

from deef import port

balancer = None

def SIGINT_handler(sig_number, sig_stack):
    global balancer
    balancer.delServer()
    exit()

signal.signal(signal.SIGINT, SIGINT_handler)

def main():
    global balancer
    # balancer = RoundRobin(port, 3)
    balancer = Balancer(port)
    # signal.signal(signal.SIGINT, balancer.stop)
    balancer.run()


main()
