from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import os
from getpass import getpass

# Step 1: Get the passphrase from the user securely
# The passphrase will be used to derive a key for encryption
passphrase = getpass("Enter a passphrase to secure your email password: ").encode()

# Step 2: Generate a salt for key derivation (this will be stored along with the encrypted password)
salt = os.urandom(16)  # 16 bytes of random data to be used as the salt

# Step 3: Derive a key using PBKDF2HMAC (Key Derivation Function)
# PBKDF2HMAC uses the passphrase and salt to generate a key suitable for encryption.
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),   # Hash function to use in key derivation
    length=32,                   # Desired length of the key (32 bytes)
    salt=salt,                   # Salt generated in Step 2
    iterations=100000,           # The number of iterations to make the process slower and more secure
    backend=default_backend()    # Backend to use (default backend in cryptography)
)

# Step 4: Derive the key from the passphrase and salt
key = base64.urlsafe_b64encode(kdf.derive(passphrase))  # Base64-encode the derived key for use with Fernet encryption

# Step 5: Encrypt the password using the derived key
email_password = b"Chatbot123"  # Replace this with your actual email password
fernet = Fernet(key)  # Create a Fernet encryption object with the derived key
encrypted_password = fernet.encrypt(email_password)  # Encrypt the password

# Step 6: Save the encrypted password and salt to separate files
with open("encrypted_password.bin", "wb") as enc_file:
    enc_file.write(encrypted_password)  # Save the encrypted password

with open("salt.bin", "wb") as salt_file:
    salt_file.write(salt)  # Save the salt used for key derivation

print("Password encrypted and saved successfully!")
