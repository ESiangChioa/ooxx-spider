# coding: utf-8

class Proxy:

    def __init__(self:Proxy, protocol:str, ip:str, port:str):
        self.protocol = protocol.lower()
        self.ip = ip
        self.port = int(port)
        self.ttl = 5
        self.ping = 10000

    def __hash__(self):
        return hash((self.protocol, self.ip, self.port))

    def __eq__(self:Proxy, other:Proxy) -> bool:
        if not isinstance(other, type(self)): return False
        return self.protocol == other.protocol and self.port == other.port and self.ip == other.ip

    def __repr__(self) -> str:
        return 'Proxy({}, {}, {})'.format(self.protocol, self.ip, self.port)

    def assemble(self) -> str:
        return '{}://{}:{}'.format(self.protocol, self.ip, self.port)

