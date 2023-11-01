import Crypto

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

# set the parameters p and g
p = 37
g = 5

# alice picks a random private key a
a = 6

# bob picks a random private key b
b = 15

# calculate A and B
A = (g ** a) % p
B = (g ** b) % p

# calculate secret keys
alice_secret = (B ** a) % p
bob_secret = (A ** b) % p

print(alice_secret)
print(bob_secret)

# convert secret key to bytes to use in calculating keys
alice_bytes = str(alice_secret).encode()
bob_bytes = str(bob_secret).encode()

# calculate symmetric keys
h1 = SHA256.new()
h1.update(alice_bytes)

h2 = SHA256.new()
h2.update(bob_bytes)

# retrieve digest values and confirm that they are same
alice_digest = h1.hexdigest()
bob_digest = h2.hexdigest()

alice_digest = alice_digest[0:16]
bob_digest = bob_digest[0:16]

if alice_digest == bob_digest:
    print("same symmetric key k")