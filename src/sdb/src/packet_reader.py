class PacketReader:

    def __init__(self, conenction: Connection):
        self.__buffer = bytearray()

        self.connection = conenction