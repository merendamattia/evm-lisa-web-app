from services.EVMLisa.EVMLisaValidator import EVMLisaValidator 
from flask import jsonify

class EVMLisaParams :

    def __init__(self, link_unsound_jumps = False, dot = False, bytecode = '', address = '') :

        self.link_unsound_jumps = link_unsound_jumps
        self.dot = dot
        self.bytecode = bytecode
        self.address = address

    def build_command(self) : 

        cmd = list()

        if self.address : 
            if EVMLisaValidator.is_valid_evm_address(self.address): 
                cmd.append(f'-a')
                cmd.append(f'{self.address}')
            else:
                raise ValueError(f"Invalid Ethereum address provided: {self.address}")
        
        if self.link_unsound_jumps : 
            cmd.append('--link-unsound-jumps-to-all-jumpdest')

        if self.dot : 
            cmd.append('--dot')

        if self.bytecode:
            if EVMLisaValidator.is_valid_bytecode(self.bytecode):
                cmd.append(f'--bytecode')
                cmd.append(f'{self.bytecode}')
            else:
                raise ValueError('Invalid bytecode provided.')
            
        return cmd
    
