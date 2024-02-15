from socket_driver.scpi_sockets import Instrument

class Scope(Instrument):
    def __init__(self, name, ip_addr, ip_port, timeout=10):
        super().__init__(name, ip_addr, ip_port, timeout)