from Crypto.Hash import MD5
from Crypto.Hash import SHA256

# 1.MD5
message = b"Hello World"  # note the added 'b' here, in contrast with Pluralsight code
h = MD5.new()
h.update(message)
print(h.hexdigest())

# 2.SHA
message = b"Hello World"  # note the added 'b' here, in contrast with Pluralsight code
h = SHA256.new()
h.update(message)
print(h.hexdigest())

# 3.File Checksum
filename = "C:\Users\Kris\Desktop\PythonCourse\cryptography\test.txt"

# Read the contents of the file
with open("filename", "rb") as file:
    data = file.read()

# Create a SHA-256 hash object
hash_object = SHA256.new()

# Feed the data into the hash object
hash_object.update(data)

# Retrieve the checksum as a hexadecimal string
checksum = hash_object.hexdigest()

print("The SHA-256 checksum of", filename, "is:", checksum)

# alternatively, we can use various tools to generate the SHA256 hash
# e.g. on mac: shasum -a 256 file.txt
# openssl sha256 file.txt