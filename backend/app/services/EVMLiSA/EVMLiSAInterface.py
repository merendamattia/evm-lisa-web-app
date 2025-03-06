import subprocess
import json
import os
from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

class EVMLiSAInterface:
    # Singleton pattern
    _instance = None
    
    class APIKeyManager:
        SECRET_KEY_FILE = "crypto/secret.key"
        API_KEY_FILE = "crypto/api_key.key"  # Cambiato da 'api_key.json' a 'api_key.txt'
        _instance = None

        def __new__(cls):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

        def __init__(self):
            if not hasattr(self, 'initialized'):
                # Crea la cartella "crypto" se non esiste
                if not os.path.exists(os.path.dirname(self.SECRET_KEY_FILE)):
                    os.makedirs(os.path.dirname(self.SECRET_KEY_FILE))
                
                if not os.path.exists(self.SECRET_KEY_FILE):
                    with open(self.SECRET_KEY_FILE, "wb") as f:
                        f.write(Fernet.generate_key())
                with open(self.SECRET_KEY_FILE, "rb") as f:
                    self.cipher = Fernet(f.read())
                self.initialized = True

        def save_api_key(self, api_key):
            encrypted_key = self.cipher.encrypt(api_key.encode())
            # Crea la cartella "crypto" se non esiste
            if not os.path.exists(os.path.dirname(self.API_KEY_FILE)):
                os.makedirs(os.path.dirname(self.API_KEY_FILE))
            with open(self.API_KEY_FILE, "wb") as f:  # Salva come binario
                f.write(encrypted_key)  # Scrivi la chiave cifrata direttamente nel file di testo

        def get_api_key(self):
            if not os.path.exists(self.API_KEY_FILE):
                return None
            with open(self.API_KEY_FILE, "rb") as f:  # Leggi come binario
                encrypted_key = f.read()  # Leggi la chiave cifrata
                return self.cipher.decrypt(encrypted_key).decode()  # Decifra e restituisci la chiave
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EVMLiSAInterface, cls).__new__(cls)
        return cls._instance

    def __init__(self, jar_path: str):
        if not hasattr(self, 'initialized'):
            self.jar_path = jar_path
            self.api_key_manager = self.APIKeyManager()
            self.initialized = True

    def save_api_key (self, api_key) : 
        self.api_key_manager.save_api_key(api_key)

    def run_command(self, params):
        try:
            cmd = ["java", "-jar", self.jar_path, "--etherscan-api-key", self.api_key_manager.get_api_key()]
            cmd.extend(params.build_command())

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            output = result.stderr.strip()
            output = output[output.index("{"):] if "{" in output else ""

            try:
                data = json.loads(output)
            except json.JSONDecodeError:
                data = {"output": output}
            
            return data, 200
        
        except subprocess.CalledProcessError as e:
            output = e.stderr.strip()
            output = output[output.index("{"):] if "{" in output else ""
            error_data = json.loads(output)
            return error_data, 500
            
        except ValueError as e:
            error_data = {"error" : str(e)}
            return error_data, 400

        except Exception as e:
            error_data = {"error" : "An unexpected error occurred."}
            return error_data, 500
        
#java -jar ./evm-LiSA-all.jar --basic-blocks -a 0x6c221dea36d48512947bde8aeb58811db50dbf6f --link-unsound-jumps-to-all-jumpdest --bytecode 0x6080604052600034151560965750604051600230310490736b6e4b338b4d5f7d847dab5492106751c57b7ff0906108fc8315029083906000818181858888f193505050501580156053573d6000803e3d6000fd5b5060405173e09f3630663b6b86e82d750b00206f8f8c6f8ad49082156108fc029083906000818181858888f193505050501580156094573d6000803e3d6000fd5b505b500000a165627a7a723058205ff37c6ec0874792b0fd774633f55769070e24b5f659403ce387b838ccb86a710029
