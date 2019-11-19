from kobra_fight import Balancer
import signal


def main():
    balancer = Balancer(12346)
    # signal.signal(signal.SIGINT, balancer.stop)
    balancer.run()


main()
