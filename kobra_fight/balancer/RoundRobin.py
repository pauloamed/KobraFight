from . import Balancer

debug = True
class RoundRobin(Balancer):
    def __init__(self, port, maxClients, numInitServers):
        super().__init__(port, maxClients)

        self.chosenServer = 0

        self.initServers(numInitServers)

    def initServers(self, numInitServers):
        for i in range(numInitServers):
            self.initServer()


    def findServer(self):
        if debug:
            print(">>> Tentando achar server")
        foundServer = -1

        while True:
            if not self.isServerFull(self.chosenServer):
                foundServer = self.servers[self.chosenServer]
                self.chosenServer = (1 + self.chosenServer) % len(self.servers)
                break
            else:
                self.chosenServer = (1 + self.chosenServer) % len(self.servers)

        return foundServer
