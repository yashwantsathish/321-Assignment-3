from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Util import number
from Crypto.Hash import SHA256

# RSA key generation by  Alice
p = number.getPrime(1024)
q = number.getPrime(1024)
n = p * q
e = 65537  # given
d = pow(e, -1, (p-1)*(q-1))  # private key component

# Public and private keys for Alice
alice_public_key = (n, e)
alice_private_key = (n, d)

# Simulate RSA encryption by Bob
s = number.getRandomInteger(1000)  # random secret key
n, e = alice_public_key
c = pow(s, e, n)

# Mallory intercepts and modifies the ciphertext to be multiplied by 0
cmod = c * 0

# Mallory performs SHA256(0) to derive the symmetric key
val = 0
mallory_symmetric_key = str(val).encode()

mallory_symmetric_key = SHA256.new(mallory_symmetric_key)
mallory_symmetric_key = mallory_symmetric_key.hexdigest()[0:16]
# mallory_symmetric_key = hashlib.sha256(str(cmod).encode('utf-8')).digest()

# Simulate Alice sending the message
msg = "Hi Bob!"
iv = get_random_bytes(16)

# AES-CBC encryption using the derived symmetric key by Alice
cipher = AES.new(mallory_symmetric_key.encode(), AES.MODE_CBC, iv)
padded_m = pad(msg.encode(), AES.block_size)
c0 = cipher.encrypt(padded_m)

# Mallory attempts to decrypt c0 using the derived symmetric key
mallory_decipher = AES.new(mallory_symmetric_key.encode(), AES.MODE_CBC, iv)
mallory_msg = mallory_decipher.decrypt(c0)

mallory_msg = unpad(mallory_msg, AES.block_size)
mallory_msg = mallory_msg.decode()

# Demonstrate the attack
print("Original Message:", msg)
print("Original RSA Encrypted Ciphertext:", c)
print("Modified RSA Encrypted Ciphertext (with malleability attack):", cmod)
print("Derived Symmetric Key (from Mallory's perspective):", mallory_symmetric_key)
print("Encrypted AES-CBC with Derived Symmetric Key (by Mallory):", c0.hex())
print("Mallory Decrypted AES-CBC (with derived key from zero ciphertext):", mallory_msg)
