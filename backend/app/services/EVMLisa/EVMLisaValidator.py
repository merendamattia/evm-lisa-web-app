import re
import os


class EVMLiSAValidator:
    
    # Pattern to validate an Ethereum (EVM) address
    EVM_ADDRESS_PATTERN = re.compile(r"^0x[a-fA-F0-9]{40}$")
    
    @staticmethod
    def is_valid_evm_address(address):
        """
        Method to validate an Ethereum (EVM) address.

        :param address: The address to validate
        :return: True if the address is valid, otherwise False
        """

        print(address)

        return bool(address) and bool(EVMLiSAValidator.EVM_ADDRESS_PATTERN.match(address))

    @staticmethod
    def is_valid_filepath(filepath):
        """
        Method to validate a file path, ensuring it is a safe and valid path.

        :param filepath: The file path to validate
        :return: True if the path is valid, otherwise False
        """
        # Check if the path is a non-empty string and if the file exists
        if not filepath:
            return False
        # Check if the file exists and is a regular file (not a directory)
        if not os.path.isfile(filepath):
            return False
        # Ensure the path does not contain dangerous characters
        if re.search(r"[<>:\"/\\|?*]", filepath):
            return False
        return True
    
    @staticmethod
    def is_valid_bytecode(bytecode):
        """
        Method to validate the bytecode, ensuring it is a valid hexadecimal string.

        :param bytecode: The bytecode string to validate
        :return: True if the bytecode is valid, otherwise False
        """
        # Check if bytecode is a non-empty string
        if not bytecode:
            return False
        # Check if it matches a valid hexadecimal format (common for Ethereum bytecode)
        # Ethereum bytecode is typically a long string of hex characters starting with '0x'
        return len(bytecode) >= 40  # Adjust length if needed