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
        API_KEY_FILE = "crypto/api_key.key"
        _instance = None

        def __new__(cls):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

        def __init__(self):
            if not hasattr(self, 'initialized'):
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
            if not os.path.exists(os.path.dirname(self.API_KEY_FILE)):
                os.makedirs(os.path.dirname(self.API_KEY_FILE))
            with open(self.API_KEY_FILE, "wb") as f: 
                f.write(encrypted_key)

        def get_api_key(self):
            if not os.path.exists(self.API_KEY_FILE):
                return None
            with open(self.API_KEY_FILE, "rb") as f:
                encrypted_key = f.read()  
                return self.cipher.decrypt(encrypted_key).decode()
    
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
            if self.api_key_manager.get_api_key() is None:
                error_data = {"error" : "You must set your Etherscan API key!"}
                return error_data, 500

            cmd = ["java", "-jar", self.jar_path, "--etherscan-api-key", self.api_key_manager.get_api_key(), "--web-app-mode"]
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
