from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64

from getpass import getpass

# Step 1: Prompt for the passphrase to decrypt the password
passphrase = getpass("Enter passphrase to decrypt the password: ").encode()

# Step 2: Load the salt and encrypted password from files
with open("salt.bin", "rb") as salt_file:
    salt = salt_file.read()  # Read the salt

with open("encrypted_password.bin", "rb") as enc_file:
    encrypted_password = enc_file.read()  # Read the encrypted password

# Step 3: Derive the key from the passphrase and salt (same process as encryption)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),   # Hash function used for key derivation
    length=32,                   # Desired length of the key (32 bytes)
    salt=salt,                   # Salt used during encryption
    iterations=100000,           # Number of iterations
    backend=default_backend()    # Backend used for cryptographic operations
)

# Derive the key from the passphrase and salt
key = base64.urlsafe_b64encode(kdf.derive(passphrase))  # The key must be base64 encoded

# Step 4: Decrypt the password using the derived key
fernet = Fernet(key)  # Create a Fernet object with the derived key
decrypted_password = fernet.decrypt(encrypted_password).decode()  # Decrypt the password

# Step 5: Display the decrypted password
print("Decrypted password:", decrypted_password)

decrypted_password = None

# Now you can use the decrypted password to, for example, send an email or access an account.
