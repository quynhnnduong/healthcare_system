from Crypto.Cipher import AES as CryptoAES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

class AESCipher:
    def __init__(self, key):
        """
        Initializes the AES Cipher for encryption and decryption.
        Args:
        key (bytes): The encryption key (must be 16, 24, or 32 bytes long).
        """
        self.key = key
    
    def encrypt_message(self, message):
        """
        Encrypts a message using AES encryption with CBC mode.
        Args:
        message (str): Plain text message to be encrypted.
        
        Returns:
        str: The encrypted message encoded in base64.
        """
        iv = get_random_bytes(CryptoAES.block_size)  # Generate a random IV
        
        cipher = CryptoAES.new(self.key, CryptoAES.MODE_CBC, iv)  # Create cipher object
        encrypted_message = cipher.encrypt(pad(message.encode(), CryptoAES.block_size))  # Encrypt the message
        
        encrypted_message_iv = iv + encrypted_message  # Combine IV with the encrypted message
        encrypted_message_b64 = base64.b64encode(encrypted_message_iv).decode('utf-8')  # Encode to base64
        
        return encrypted_message_b64
    
    def decrypt_message(self, encrypted_message):
        """
        Decrypts a message using AES encryption with CBC mode.
        Args:
        encrypted_message (str): Encrypted message encoded in base64.
        
        Returns:
        str: The decrypted plain text message.
        """
        encrypted_message_iv = base64.b64decode(encrypted_message)  # Decode the base64 encoded message
        
        iv = encrypted_message_iv[:CryptoAES.block_size]  # Extract the IV
        encrypted_message = encrypted_message_iv[CryptoAES.block_size:]  # Extract the encrypted message
        
        cipher = CryptoAES.new(self.key, CryptoAES.MODE_CBC, iv)  # Create cipher object
        decrypted_message = unpad(cipher.decrypt(encrypted_message), CryptoAES.block_size).decode('utf-8')  # Decrypt the message
        
        return decrypted_message

# Example usage
# if __name__ == "__main__":
#     key = get_random_bytes(16)  # AES key must be either 16, 24, or 32 bytes long
#     aes_cipher = AESCipher(key)
#     message = "Hello, world! This is a test message."

#     encrypted = aes_cipher.encrypt_message(message)
#     print("Encrypted:", encrypted)

#     decrypted = aes_cipher.decrypt_message(encrypted)
#     print("Decrypted:", decrypted)
