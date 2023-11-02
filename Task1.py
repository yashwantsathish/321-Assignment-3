import Crypto

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# set the parameters p and g
# p = 37
# g = 5

p = "B10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371"
g = "A4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5"

p = int(p, 16)
g = int(g, 16)

# alice picks a random private key a
a = 19

# bob picks a random private key b
b = 37

# calculate A and B
A = (g ** a) % p
B = (g ** b) % p

# calculate secret keys
alice_secret = (B ** a) % p
bob_secret = (A ** b) % p

# convert secret key to bytes to use in calculating keys
alice_bytes = str(alice_secret).encode()
bob_bytes = str(bob_secret).encode()

# calculate symmetric keys
h1 = SHA256.new()
h1.update(alice_bytes)

h2 = SHA256.new()
h2.update(bob_bytes)

# retrieve digest values and confirm that they are same
alice_key = h1.hexdigest()
bob_key = h2.hexdigest()

alice_key = alice_key[0:16]
bob_key = bob_key[0:16]

if alice_key == bob_key:
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

# Decrypt (Bob) with Symmetric Key
cipher2 = AES.new(bob_key.encode(), AES.MODE_CBC, iv1)
message1 = cipher2.decrypt(ciphertext)

message1 = unpad(message1, AES.block_size)
message1 = message1.decode()

print(message1)

#Bob -> Alice Message Encryption
# Generate ciphertext for Bob -> Alice
cipher1 = AES.new(bob_key.encode(), AES.MODE_CBC, iv2)

padded_m1 = pad(m1.encode(), AES.block_size)
ciphertext = cipher1.encrypt(padded_m1)

# Decrypt (Alice) with Symmetric Key
cipher2 = AES.new(alice_key.encode(), AES.MODE_CBC, iv2)
message2 = cipher2.decrypt(ciphertext)

message2 = unpad(message2, AES.block_size)
message2 = message2.decode()

print(message2)
