from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

# set the parameters p and g
p = 37  # Shared prime
g = 5   # Shared base

# Alice and Bob generate their private keys
a = 37
b = 15

#Mallory Modified Values
#g = 1
#g = p
g = p-1
    
# Calculate public values A and B
A = (g ** a) % p
B = (g ** b) % p

# calculate shared secret keys using mallory modified values
alice_secret = (B ** a) % p
bob_secret = (A ** b) % p

# convert secret key to bytes to use in calculating keys
alice_bytes = str(alice_secret).encode()
bob_bytes = str(bob_secret).encode()

# calculate symmetric key
h1 = SHA256.new()
h1.update(alice_bytes)

h2 = SHA256.new()
h2.update(bob_bytes)

alice_key = h1.hexdigest()
bob_key = h2.hexdigest()

alice_key = alice_key[0:16]
bob_key = bob_key[0:16]

# print(alice_key)
# print(bob_key)

if alice_key == bob_key:
    symm_key = alice_key
    print("same symmetric key k")

# Setup for AES 
m0 = "Hi Bob!"
m1 = "Hi Alice!"

iv1 = get_random_bytes(16)
iv2 = get_random_bytes(16)

#Alice -> Bob Message Encryption
# Generate ciphertext for Alice -> Bob
cipher1 = AES.new(alice_key.encode(), AES.MODE_CBC, iv1)

padded_m0 = pad(m0.encode(), AES.block_size)
ciphertext = cipher1.encrypt(padded_m0)

# Decrypt m0 (Mallory) with Symmetric Key
cipher2 = AES.new(symm_key.encode(), AES.MODE_CBC, iv1)
message1 = cipher2.decrypt(ciphertext)

message1 = unpad(message1, AES.block_size)
message1 = message1.decode()

print(message1)

#Bob -> Alice Message Encryption
# Generate ciphertext for Bob -> Alice
cipher1 = AES.new(bob_key.encode(), AES.MODE_CBC, iv2)

padded_m1 = pad(m1.encode(), AES.block_size)
ciphertext = cipher1.encrypt(padded_m1)

# Decrypt m1 (Mallory) with Symmetric Key
cipher2 = AES.new(symm_key.encode(), AES.MODE_CBC, iv2)
message2 = cipher2.decrypt(ciphertext)

message2 = unpad(message2, AES.block_size)
message2 = message2.decode()

print(message2)


