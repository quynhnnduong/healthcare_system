from Crypto.Cipher import AES as CryptoAES, AES
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

    def encrypt(self, message):
        """
        Encrypts a message using AES encryption with CBC mode.
        Args:
        message (str): Plain text message to be encrypted.
        
        Returns:
        str: The encrypted message encoded in base64.
        """
        if message is None:
            return None

        iv = get_random_bytes(CryptoAES.block_size)  # Generate a random IV

        cipher = CryptoAES.new(self.key, CryptoAES.MODE_CBC, iv)  # Create cipher object
        encrypted_message = cipher.encrypt(pad(message.encode(), CryptoAES.block_size))  # Encrypt the message

        encrypted_message_iv = iv + encrypted_message  # Combine IV with the encrypted message
        encrypted_message_b64 = base64.b64encode(encrypted_message_iv).decode('utf-8')  # Encode to base64

        return encrypted_message_b64

    def decrypt(self, encrypted_message):
        """
        Decrypts a message using AES encryption with CBC mode.
        Args:
        encrypted_message (str): Encrypted message encoded in base64.
        
        Returns:
        str: The decrypted plain text message.
        """
        if encrypted_message is None:
            return None

        encrypted_message_iv = base64.b64decode(encrypted_message)  # Decode the base64 encoded message

        iv = encrypted_message_iv[:CryptoAES.block_size]  # Extract the IV
        encrypted_message = encrypted_message_iv[CryptoAES.block_size:]  # Extract the encrypted message

        cipher = CryptoAES.new(self.key, CryptoAES.MODE_CBC, iv)  # Create cipher object
        decrypted_message = unpad(cipher.decrypt(encrypted_message), CryptoAES.block_size).decode(
            'utf-8')  # Decrypt the message

        return decrypted_message

# def generate_key(key_size=16):
#     assert key_size in [16, 24, 32], "Key size must be either 16, 24, or 32 bytes"
#     return get_random_bytes(key_size)


# Example usage
if __name__ == "__main__":
    iv = get_random_bytes(AES.block_size)
    iv_hex = iv.hex()
#     key = generate_key()
#
#     # Convert the key to a base64 string for easier viewing and printing
#     key_base64 = base64.b64encode(key).decode('utf-8')
#
#     # Print the base64-encoded key
#     print("Base64 Encoded Key:", key_base64)
    # aes_cipher = AESCipher(key)
    # message = "Hello, world! This is a test message."
    #
    # encrypted = aes_cipher.encrypt_message(message)
    # print("Encrypted:", encrypted)
    #
    # decrypted = aes_cipher.decrypt_message(encrypted)
    # print("Decrypted:", decrypted)
