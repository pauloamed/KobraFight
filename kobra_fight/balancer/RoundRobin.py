class RoundRobin(Balancer):
    def __init__(self, port):
        super().__init__()

        self.chosenServer = 0

    def initServers(self, numInitServers):
        for i in numInitServers:
            self.initServer()


    def findServer(self):
        if debug:
            print(">>> Tentando achar server")
        foundServer = -1

        while True:
            if not self.isServerFull(self.chosenServer):
                foundServer = self.servers[self.chosenServer]
                self.chosenServer = (1 + self.chosenServer) % len(self.chosenServer)
                break
            else:
                self.chosenServer = (1 + self.chosenServer) % len(self.chosenServer)

        return foundServer
