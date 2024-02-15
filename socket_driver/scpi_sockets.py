import socket
import numpy as np
import math

# TODO: 
# 1. timeout is only good per command?
# 1. 

class SCPISocket:
    def __init__(self, ip_addr: str, ip_port: int, timeout=10):
        self.ip_addr = ip_addr
        self.ip_port = ip_port
        self.s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip_addr,ip_port))
        # self.s.connect(('10.0.1.144',4000))
        self.s.settimeout(timeout)
        
    def recv(self, n_bytes, exact=False):
        print(f"requested n_bytes is {n_bytes} {exact=}")
        data_bytes_array = bytearray()
        
        data_bytes = self.s.recv(n_bytes)
        recv_n_bytes = len(data_bytes)
        print(f"{recv_n_bytes=}")
        n_bytes_remaining = n_bytes - recv_n_bytes
        data_bytes_array.extend(data_bytes)
        
        max_iter = 1000
        iter = 0
        while exact and n_bytes_remaining > 0 and iter < max_iter:
            data_bytes = self.s.recv(n_bytes_remaining)
            recv_n_bytes = len(data_bytes)
            n_bytes_remaining -= recv_n_bytes
            data_bytes_array.extend(data_bytes)
            iter +=1
            
        print(f"received length is {len(data_bytes_array)}")
        
        return bytes(data_bytes_array)
        
    def write(self, cmd: str, terminator="\n"):
        self.s.sendall(f"{cmd}{terminator}".encode())

    # TODO: Add check for end of line instead of byte length
    def read_str(self, n_bytes=16384, endline=True):
        max_iter = 1000
        iter = 0
        data = ""
        while iter < max_iter:
            data_bytes = self.recv(n_bytes)
            data = data_bytes.decode()
            if data[-1] == "\n" or not endline:
                break
            data += data
        # data = data.strip()
        return data
    
    def read_raw(self, n_bytes=16384):
        self.s.settimeout(10)
        data_bytes = self.recv(n_bytes, True)
        return data_bytes
     
    def read_int(self, n_bytes=16384):
        return int(self.read_str(n_bytes, False))
    
    def read_hex(self, n_bytes=16384):
        return int(self.read_str(n_bytes, False), 16)
    
    def read_float(self, n_bytes=16384):
        return float(self.read_str(n_bytes, False))
    
    def query_str(self, cmd, n_bytes=16384, terminator="\n"):
        self.write(cmd)
        value = self.read_str(n_bytes)
        return value
    
    def query_raw(self, cmd, n_bytes=16384, terminator="\n"):
        self.write(cmd)
        value = self.read_raw(n_bytes)
        return value
    
    def query_int(self, cmd, n_bytes=16384, terminator="\n"):
        self.write(cmd)
        value = self.read_int(n_bytes)
        return value
    
    def query_float(self, cmd, n_bytes=16384, terminator="\n"):
        self.write(cmd)
        value = self.read_float(n_bytes)
        return value

    # https://rfmw.em.keysight.com/DigitalPhotonics/flexdca/PG/Content/Topics/SCPI-Introduction/binary_block_data.htm
    # The syntax is a pound sign (#) followed by a non-zero digit representing the number of following digits (decimal integer) 
    # that define the number of 8-bit data bytes being sent. This is followed by the actual data. For example, when transmitting 
    # 3000 bytes of data, the syntax would be:
    # #43000<3000 bytes of data>
    # Where:
    # 4 represents the number of characters used to state the number of data bytes.
    # 3000 represents the number of bytes to be transmitted.
    #
    # When your program receives definite-length block data, the program needs to know the data type being returned. 
    # That is how many bytes are used to express an integer or a floating-point number. The program must know this 
    # to successfully convert the bytes to a number. Otherwise, the numbers returned will be spectacularly wrong.
    # Common Data Type Specifiers
    # Specifier	Data Type	Number of Bytes
    # c	ASCII char (unsigned)	1
    # B	bytes, binary (unsigned)	1
    # i	integer (signed)	4
    # I	integer (unsigned)	4
    # h	short integer (signed)	2
    # H	short integer (unsigned	2
    # l	long integer (signed)	4
    # L	long integer (unsigned)	4
    # e	float	2
    # f	float	4
    # d	double	8
    #
    # To correctly interpret definite-length block data, you must know the endianness (byte order) of the returned data 
    # (integers or real) from FlexDCA and you will must likely need specify this same endianness in your program language's 
    # command that is used to query the data. Endianness can be set to "little endian" order in which the least significant 
    # byte is sent first and the most significant byte sent last. Or, the endianness can be set to "big endian" order in 
    # which the most significant byte is sent first and the least significant byte sent last.
    #
    # https://numpy.org/doc/stable/reference/generated/numpy.frombuffer.html
    # numpy.frombuffer(buffer, dtype=float, count=-1, offset=0, *, like=None)
    # https://github.com/tektronix/Programmatic-Control-Examples/blob/master/Examples/Oscilloscopes/PerformanceScopes/src/FetchWaveformDataExample/MSO%20DPO%205K%207K%2070K%20Fetch%20Waveform%20Data.py
    # https://github.com/pyvisa/pyvisa/blob/6bca99233dcf66742db54d6d410c9840efb18cb5/pyvisa/util.py#L645
    def read_binary(self, datatype='b'):
        value_hash = self.read_str(1, False)
        print(f"first byte is {value_hash}")
        value_digits = self.read_int(1)
        print(f"second byte is {value_digits}")
        n_bytes = self.read_int(value_digits)
        print(f"number of bytes is {n_bytes}")
        
        # From https://github.com/morgan-at-keysight/socketscpi/blob/master/socketscpi/socketscpi.py
        if datatype == 'b':
            dtype = np.int8
        elif datatype == 'B':
            dtype = np.uint8
        elif datatype == 'h':
            dtype = np.int16
        elif datatype == 'H':
            dtype = np.uint16
        elif datatype == 'i' or datatype == 'l':
            dtype = np.int32
        elif datatype == 'I' or datatype == 'L':
            dtype = np.uint32
        elif datatype == 'q':
            dtype = np.int64
        elif datatype == 'Q':
            dtype = np.uint64
        elif datatype == 'f':
            dtype = np.float32
        elif datatype == 'd':
            dtype = np.float64
        else:
            raise Exception('Invalid data type selected.')
        
        print("recv data")
        data_bytes = self.recv(n_bytes, True)
        # last_term = self.s.recv(1) # TODO: Check the value?
        
        # data_array = np.frombuffer(data_bytes, "<b")
        data_array = np.frombuffer(data_bytes, dtype)
        return data_array

    def query_binary(self, cmd, datatype='b'):
        self.write(cmd)
        data_array = self.read_binary(datatype)
        
        return data_array
    
class Instrument(SCPISocket):
    def __init__(self, name, ip_addr, ip_port, timeout=10):
        super().__init__(ip_addr, ip_port, timeout)
        self.name = name
    
    def idn(self):
        return self.query_str("*IDN?")

