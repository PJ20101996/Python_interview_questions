from cryptography.fernet import Fernet

# Generate a new encryption key
key = Fernet.generate_key()
print("Encryption Key (store this safely):", key.decode())

# Initialize Fernet with the key
f = Fernet(key)

# Replace these with any new credentials you want to encrypt
username = b"Jagadish"
password = b"Ammananna"

# Encrypt the credentials
encrypted_user = f.encrypt(username)
encrypted_pass = f.encrypt(password)

print("Encrypted USER:", encrypted_user.decode())
print("Encrypted PASS:", encrypted_pass.decode())
