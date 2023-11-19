from Crypto.Util import number

# Generating key pair

# Generate two random prime numbers
p = number.getPrime(1024)
q = number.getPrime(1024)

# Calculate n and phi
n = p*q
phi = (p-1) * (q-1)

# Choose e = 65537
e = 65537

# Calculate d (multiplicative inverse inverse of e)
d = pow(e, -1, phi)

# Encryption

# Encrypt message using public key (e, n)
msg = "bradley beal"

#Turning msg into hex msg (int)
hex_msg = int(msg.encode('utf-8').hex(), 16)

encrypted_msg = pow(hex_msg, e, n)

# Decryption 

# Decrypt the ciphertext using the private key (d, n)
decrypted_msg = pow(encrypted_msg, d, n)

print(msg)
# print("hex: " + str(hex_msg))
# print("Encrypted message: " + str(encrypted_msg))
decrypted_msg = bytes.fromhex(hex(decrypted_msg)[2:]).decode('utf-8')
print("Decrypted message: " + str(decrypted_msg))
