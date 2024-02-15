from library.base_instruments import Scope
from library.vendor.tek import read_wfm

class TekScope(Scope):
    def __init__(self, name, ip_addr, ip_port, timeout=10):
        super().__init__(name, ip_addr, ip_port, timeout)
    
    def clear(self):
        self.write("*CLS")
    
    def reset(self):
        self.write("*RST")
    
    def opc(self):
        value = self.query_raw('*OPC?', 1)
        value_str = value.decode()
        if value_str != "1" and value_str != "0":
            print(f"Warning: OPC returned {value}, likely unread data in the output buffer?")
        return value
    
    def get_cwd(self):
        value = self.query_str("FILESYSTEM:CWD?")
        return value
    
    def set_cwd(self, dir_path):
        instr_path = Path(dir_path)
        self.write(f"FILESYSTEM:CWD \"{instr_path}\"")
        
    def list_files(self, dir_path):
        instr_path = Path(dir_path)
        self.set_cwd(instr_path)
        files = self.query_str("FILESYSTEM:LDIR?")
        value = self.opc()
        print(f"opc value is {value} ")
        self.read_raw(1) # Stray \n ??
        print(f"{files=}")
        files = files.split(",")
        for file in files:
            file_info = file.strip("\"").split(";")
            print(file_info)
        
        return file_info
    
    def get_file_size(self, file_path):
        instr_path = Path(file_path)
        file_name = instr_path.name
        dir_name = instr_path.parent
        print(f"dir_name={dir_name}  file_name={file_name}")
        self.set_cwd(dir_name)
        files = self.query_str("FILESYSTEM:LDIR?")
        value = self.opc()
        print(f"opc value is {value} ")
        self.read_raw(1) # Stray \n ??
        print(f"{files=}")
        files = files.split(",")
        file_size_bytes = -1
        for file in files:
            file_info = file.strip("\"").split(";")
            print(file_info)
            if file_info[0] == file_name:
                file_size_bytes = int(file_info[2])
                break
        # print(f"{file_size_bytes=}")
        
        return file_size_bytes
    
    def download_file(self, file_path, local_file_name=None):
        if local_file_name is None:
            instr_path = Path(file_path)
            save_file_name = instr_path.name
        else:
            remote_file_path = Path(file_path)
            save_file_name = remote_file_path.name
        print(f"{file_path=}")    
        file_size_bytes = self.get_file_size(file_path)
        print(f"{file_size_bytes=}")
        if file_size_bytes > 0:
            print(f"FILESystem:READFile \"{file_path}\"")
            self.write(f"FILESystem:READFile \"{file_path}\"")
            # value = self.query_str("SYSTem:ERRor?")
            # print(f"error value is {value} ")
            value = self.opc()
            print(f"opc value is {value} ")
            # self.write("*OPC")
            imgData = self.read_raw(file_size_bytes)
            print(f"length of imgData is {len(imgData)}")
            file = open(save_file_name, "wb")
            file.write(imgData)
            file.close()
            
            self.clear()
        else:
            print(f"Warning: Requested file size is {file_size_bytes}, likely failed request or doesn't exist?")        
      