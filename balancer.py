from kobra_fight import Balancer
import signal

from deef import port

def main():
    balancer = Balancer(port)
    # signal.signal(signal.SIGINT, balancer.stop)
    balancer.run()


main()
