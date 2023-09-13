import time
from PIL import Image
# simplified aes
class SimplifiedAES(object):

    # S-Box
    sBox = [0x9,0x4,0xA,0xB,
            0xD,0x1,0x8,0x5,
            0x6,0x2,0x0,0x3,
            0xC,0xE,0xF,0x7]

    # Inverse S-Box
    sBoxI = [0xA,0x5,0x9,0xB,
            0x1,0x7,0x8,0xF,
            0x6,0x0,0x2,0x3,
            0xC,0x4,0xD,0xE]

    def __init__(self, key):
        # Round keys: K0 = w0 + w1; K1 = w2 + w3; K2 = w4 + w5
        self.pre_round_key, self.round1_key, self.round2_key = self.key_expansion(key)
    def sub_word(self, word):
        return (self.sBox[(word >> 4)] << 4) + self.sBox[word & 0x0F]

    def rot_word(self, word):
        # Rotate word
        return ((word & 0x0F) << 4) + ((word & 0xF0) >> 4)

    def key_expansion(self, key):

        # Round constants
        Rcon1 = 0x80
        Rcon2 = 0x30

        # Calculating value of each word
        w = [None] * 6
        w[0] = (key & 0xFF00) >> 8
        w[1] = key & 0x00FF
        w[2] = w[0] ^ (self.sub_word(self.rot_word(w[1])) ^ Rcon1)
        w[3] = w[2] ^ w[1]
        w[4] = w[2] ^ (self.sub_word(self.rot_word(w[3])) ^ Rcon2)
        w[5] = w[4] ^ w[3]

        return (
            self.int_to_state((w[0] << 8) + w[1]),  # Pre-Round key
            self.int_to_state((w[2] << 8) + w[3]),  # Round 1 key
            self.int_to_state((w[4] << 8) + w[5]),  # Round 2 key
        )

    def gf_mult(self, a, b):
        #Galois field multiplication of a and b in GF(2^4) / x^4 + x + 1

        product = 0
        # Mask the unwanted bits
        a = a & 0x0F
        b = b & 0x0F
        # While both multiplicands are non-zero
        while a and b:

            # If LSB of b is 1
            if b & 1:

                # Add current a to product
                product = product ^ a

            # Update a to a * 2
            a = a << 1

            # If a overflows beyond 4th bit
            if a & (1 << 4):

                # XOR with irreducible polynomial with high term eliminated
                a = a ^ 0b10011

            # Update b to b // 2
            b = b >> 1

        return product

    def int_to_state(self, n):
        #Convert a 2-byte integer into a 4-element vector (state matrix)
        return [n >> 12 & 0xF, (n >> 4) & 0xF, (n >> 8) & 0xF, n & 0xF]

    def state_to_int(self, m):
        #Convert a 4-element vector (state matrix) into 2-byte integer
        return (m[0] << 12) + (m[2] << 8) + (m[1] << 4) + m[3]

    def add_round_key(self, s1, s2):
        #Add round keys in GF(2^4)
        return [i ^ j for i, j in zip(s1, s2)]

    def sub_nibbles(self, sbox, state):
        #Nibble substitution
        return [sbox[nibble] for nibble in state]

    def shift_rows(self, state):
        #Shift rows and inverse shift rows of state matrix
        return [state[0], state[1], state[3], state[2]]

    def mix_columns(self, state):
        #Mix columns transformation on state matrix
        return [
            state[0] ^ self.gf_mult(4, state[2]),
            state[1] ^ self.gf_mult(4, state[3]),
            state[2] ^ self.gf_mult(4, state[0]),
            state[3] ^ self.gf_mult(4, state[1]),
        ]

    def inverse_mix_columns(self, state):
        #Inverse mix columns transformation on state matrix
        return [
            self.gf_mult(9, state[0]) ^ self.gf_mult(2, state[2]),
            self.gf_mult(9, state[1]) ^ self.gf_mult(2, state[3]),
            self.gf_mult(9, state[2]) ^ self.gf_mult(2, state[0]),
            self.gf_mult(9, state[3]) ^ self.gf_mult(2, state[1]),
        ]

    def encrypt(self, plaintext):
        #Encrypt plaintext with given key
        state = self.add_round_key(self.pre_round_key, self.int_to_state(plaintext))

        state = self.mix_columns(self.shift_rows(self.sub_nibbles(self.sBox, state)))

        state = self.add_round_key(self.round1_key, state)

        state = self.shift_rows(self.sub_nibbles(self.sBox, state))

        state = self.add_round_key(self.round2_key, state)

        return self.state_to_int(state)

    def decrypt(self, ciphertext):
        #Decrypt ciphertext with given key
        state = self.add_round_key(self.round2_key, self.int_to_state(ciphertext))

        state = self.sub_nibbles(self.sBoxI, self.shift_rows(state))

        state = self.inverse_mix_columns(self.add_round_key(self.round1_key, state))

        state = self.sub_nibbles(self.sBoxI, self.shift_rows(state))

        state = self.add_round_key(self.pre_round_key, state)
        return self.state_to_int(state)

def ecb_encrypt_with_padding0(plaintext, key):
    block_size = 16

    # Convert plaintext to binary
    binary_plaintext = ''.join(format(ord(c), '08b') for c in plaintext)

    # Pad the binary plaintext if its length is not divisible by the block size
    if len(binary_plaintext) % block_size != 0:
        padding_length = block_size - (len(binary_plaintext) % block_size)
        binary_plaintext += padding_length * "0"

    # Divide the binary plaintext into blocks
    num_blocks = len(binary_plaintext) // block_size
    blocks = [binary_plaintext[i * block_size: (i + 1) * block_size] for i in range(num_blocks)]

    # Initialize AES object with the provided key
    aes = SimplifiedAES(key)

    # Encrypt each block
    ciphertext_blocks = []
    for block in blocks:
        plaintext_block = int(block, 2)  # Convert the binary string block to an integer
        ciphertext_block = aes.encrypt(plaintext_block)
        ciphertext_blocks.append(ciphertext_block)

    # Concatenate the ciphertext blocks
    ciphertext = ""
    for block in ciphertext_blocks:
        ciphertext += bin(block)[2:].zfill(block_size)  # Convert each block to binary and concatenate

    return ciphertext

def ecb_decrypt_with_padding0(ciphertext, key):
    block_size = 16
    padding_length = 0

    # Divide the ciphertext into blocks
    num_blocks = len(ciphertext) // block_size
    blocks = [ciphertext[i * block_size: (i + 1) * block_size] for i in range(num_blocks)]

    # Initialize AES object with the provided key
    aes = SimplifiedAES(key)

    # Decrypt each block
    decrypted_blocks = []
    for block in blocks:
        ciphertext_block = int(block, 2)  # Convert the binary string block to an integer
        decrypted_block = aes.decrypt(ciphertext_block)
        decrypted_blocks.append(decrypted_block)

    # Concatenate the decrypted blocks
    decrypted_plaintext = "".join([bin(block)[2:].zfill(block_size) for block in decrypted_blocks])

    # Remove any padding from the decrypted plaintext
    if padding_length > 0:
        decrypted_plaintext = decrypted_plaintext[:-padding_length]

    # Convert decrypted plaintext to ASCII
    decrypted_plaintext = ''.join(chr(int(decrypted_plaintext[i:i+8], 2)) for i in range(0, len(decrypted_plaintext), 8))

    return decrypted_plaintext

def readImage(filename):
    image = Image.open(filename)
    return image

def writeImage(filename, image):
    image.save(filename)

def ecb_encrypt_image_with_padding0(image_file, key):

    block_size = 16
    padding_length = 0

    # Read the image file
    image = Image.open(image_file)
    print(image.mode)
    print(image.size)

    # Separate color channels
    channels = image.split()

    encrypted_channels = []
    for channel in channels:
        # Get the pixel values of the channel
        pixels = channel.getdata()

        # Convert the pixel values to binary
        binary_pixels = ''.join(format(pixel, '08b') for pixel in pixels)

        # Pad the binary pixels if its length is not divisible by the block size
        if len(binary_pixels) % block_size != 0:
            padding_length = block_size - (len(binary_pixels) % block_size)
            binary_pixels += padding_length * "0"

        # Divide the binary pixels into blocks
        num_blocks = len(binary_pixels) // block_size
        blocks = [binary_pixels[i * block_size: (i + 1) * block_size] for i in range(num_blocks)]

        # Initialize AES object with the provided key
        aes = SimplifiedAES(key)

        # Encrypt each block
        ciphertext_blocks = []
        for block in blocks:
            plaintext_block = int(block, 2)  # Convert the binary string block to an integer
            ciphertext_block = aes.encrypt(plaintext_block)
            ciphertext_blocks.append(ciphertext_block)

        # Convert the ciphertext blocks to binary pixels
        binary_ciphertext = "".join([bin(block)[2:].zfill(block_size) for block in ciphertext_blocks])

        # Remove any padding from the binary ciphertext
        if padding_length > 0:
            binary_ciphertext = binary_ciphertext[:-padding_length]

        # Convert the binary ciphertext to pixel values
        pixels = [int(binary_ciphertext[i:i+8], 2) for i in range(0, len(binary_ciphertext), 8)]

        # Create a new channel with the encrypted pixel values
        encrypted_channel = Image.new("L", channel.size)
        encrypted_channel.putdata(pixels)

        # Append the encrypted channel to the list
        encrypted_channels.append(encrypted_channel)

    # Merge the encrypted channels back into an image
    encrypted_image = Image.merge(image.mode, encrypted_channels)

    return encrypted_image

def ecb_decrypt_image_with_padding0(image_file, key):
    block_size = 16
    padding_length = 0

    # Read the image file
    image = Image.open(image_file)

    # Separate color channels
    channels = image.split()

    decrypted_channels = []
    for channel in channels:
        # Get the pixel values of the channel
        pixels = channel.getdata()

        # Convert the pixel values to binary
        binary_pixels = ''.join(format(pixel, '08b') for pixel in pixels)

        # Divide the binary pixels into blocks
        num_blocks = len(binary_pixels) // block_size
        blocks = [binary_pixels[i * block_size: (i + 1) * block_size] for i in range(num_blocks)]

        # Initialize AES object with the provided key
        aes = SimplifiedAES(key)

        # Decrypt each block
        decrypted_blocks = []
        for block in blocks:
            ciphertext_block = int(block, 2)  # Convert the binary string block to an integer
            decrypted_block = aes.decrypt(ciphertext_block)
            decrypted_blocks.append(decrypted_block)

        # Convert the decrypted blocks to binary pixels
        binary_decrypted = "".join([bin(block)[2:].zfill(block_size) for block in decrypted_blocks])

        # Remove any padding from the binary decrypted pixels
        if padding_length > 0:
            binary_decrypted = binary_decrypted[:-padding_length]

        # Convert the binary decrypted pixels to pixel values
        pixels = [int(binary_decrypted[i:i+8], 2) for i in range(0, len(binary_decrypted), 8)]

        # Create a new channel with the decrypted pixel values
        decrypted_channel = Image.new("L", channel.size)
        decrypted_channel.putdata(pixels)

        # Append the decrypted channel to the list
        decrypted_channels.append(decrypted_channel)

    # Merge the decrypted channels back into an image
    decrypted_image = Image.merge(image.mode, decrypted_channels)

    return decrypted_image


key = 0b1100001111110000

def readPlaintextFromFile(filename):
    with open(filename, 'r') as file:
        plaintext = file.read()
    return plaintext

def writeCiphertextToFile(filename, ciphertext):
    with open(filename, 'w') as file:
        file.write(ciphertext)

# a brute-force attack would involve trying all possible 16-bit keys (2^16 = 65,536)
# to decrypt a given ciphertext until the correct key is found.
def brute_force_attack(ciphertext, expected_plaintext):
    start_time = time.time()
    for key in range(65536):
        decrypted = ecb_decrypt_with_padding0(ciphertext, key);
        # Compare the decrypted plaintext with the expected result
        if decrypted == expected_plaintext:
            end_time = time.time()
            elapsed_time = end_time - start_time
            return key, elapsed_time


# Encryption
plaintext = readPlaintextFromFile("plaintext.txt")
start_time = time.time()
ciphertext = ecb_encrypt_with_padding0(plaintext, key)
encryption_time = time.time() - start_time
print("Encryption Time:", encryption_time)
writeCiphertextToFile("ciphertext.txt", ciphertext)

# Decryption
start_time = time.time()
ciphertext = readPlaintextFromFile("ciphertext.txt")
decrypted_plaintext = ecb_decrypt_with_padding0(ciphertext, key)
print("Decription Time:", encryption_time)
writeCiphertextToFile("decryption.txt", decrypted_plaintext)

# 0111011100001111
# lezem yetla3 hayda bel mini tele3
# 1011111010101010

# # Encryption
# image_file = "test.jpg"
# encrypted_image = ecb_encrypt_image_with_padding0(image_file, key)
# writeImage("encrypted_image.png", encrypted_image)
#
# # Decryption
# image_file = "encrypted_image.png"
# decrypted_image = ecb_decrypt_image_with_padding0(image_file, key)
# writeImage("decrypted_image.png", decrypted_image)

key, elapsed_time = brute_force_attack(ciphertext, plaintext)
print("Brute-force attack successful. Key found:", format(key, '016b'))
print("Time taken:", elapsed_time, "seconds")
