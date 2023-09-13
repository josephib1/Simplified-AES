#  Security -Simplified AES

## Introduction:

### AES:

AES, or the Advanced Encryption Standard, is a widely used symmetric encryption algorithm that is designed to provide secure and efficient data encryption and decryption. It was selected by the U.S. National Institute of Standards and Technology (NIST) in 2001 as a replacement for the aging Data Encryption Standard (DES).

AES operates on fixed-size blocks of data, typically 128 bits, and supports key sizes of 128, 192, and 256 bits. It uses a series of mathematical operations, including substitution, permutation, and mixing, to transform the input data and the encryption key into a ciphered output. The encryption process involves multiple rounds of these operations, making AES highly resistant to various cryptographic attacks.

### Simplifies-AES:

S-AES, or Simplified AES, is a reduced version of the AES algorithm. It is primarily used for educational purposes and for understanding the fundamental principles of AES. S-AES simplifies the complex structure of AES by reducing the block size to 8 bits and the key size to 16 bits. Consequently, it operates on a much smaller data space, making it easier to study and analyze the algorithm.

In S-AES, the encryption process consists of two main steps: the Substitution step and the Permutation step. During the Substitution step, the input bytes of the data and the key undergo substitution using a pre-defined substitution box (S-box). The Permutation step involves rearranging the bits of the output from the Substitution step using a simple permutation box (P-box). These steps are repeated for a fixed number of rounds to achieve the desired level of encryption.

While S-AES is not suitable for practical applications due to its limited block and key sizes, it serves as a useful learning tool to grasp the core concepts and principles of AES. Understanding S-AES can provide a foundation for studying and implementing the full AES algorithm, which is widely used to secure sensitive data in various domains, including finance, telecommunications, and e-commerce.


### Mini-EAS:

It is another version of simplified AES, typically created for educational or illustrative purposes. It might involve a smaller number of rounds, simplified key scheduling, or simplified substitution and permutation operations. The goal is to provide a simplified representation of the AES algorithm while retaining the basic principles and structure.

These simplified versions are often used as learning tools to help understand the core concepts of AES before diving into the more complex details of the full algorithm. However, it's important to note that such simplified versions are not suitable for real-world encryption as they may not offer the same level of security as the complete AES algorithm.
## Simplified AES structure:

S-AES operates on a block size of 8 bits (compared to 128 bits in AES) and uses a key size of 16 bits (compared to 128, 192, or 256 bits in AES). The algorithm consists of three main components: the Key Expansion, Encryption, and Decryption.

### 1-Key Expansion:

•	The 16-bit encryption key is expanded into two 8-bit round keys, Key1 and Key2. Each round key is generated from the original 16-bit key using a simple key schedule algorithm.
•	The key expansion process involves shifting the key bits and performing a simple substitution operation using a 4x4 S-box, which maps each 4-bit input to a 4-bit output.

### 2-Encryption:

•	The 8-bit plaintext block is divided into two 4-bit halves, Left and Right.
•	The encryption process consists of three rounds, each involving four steps: Substitution, Permutation, Mixing, and Key Addition.
•	Substitution: Each 4-bit half (Left and Right) undergoes substitution using the same S-box used in the key expansion. The S-box substitutes each 4-bit input with a corresponding 4-bit output.
•	Permutation: The output of the substitution step is rearranged using a fixed permutation box (P-box). The P-box determines the new arrangement of the bits within each 4-bit half.
•	Mixing: The 4-bit halves are mixed by performing an XOR operation with the current round key.
•	Key Addition: The round key is added to the mixed 4-bit halves.


### 3-Decryption:

•	The decryption process is similar to encryption but with the steps performed in reverse order.
•	The ciphertext is divided into two 4-bit halves, Left and Right.
•	The decryption process consists of three rounds, each involving Substitution, Permutation, Mixing, and Key Addition in reverse order.
•	The last round does not involve the Mixing step.
•	The resulting 4-bit halves are combined to obtain the plaintext block.
•	S-AES, while simpler than AES, retains some essential properties such as the use of substitution, permutation, and mixing operations. It allows for studying the basic concepts of block ciphers, including key expansion, confusion, diffusion, and the iterative nature of encryption and decryption rounds.

## Difference between S-AES and Mini-AES:

### Class Structure vs. Separate Functions:

S-AES: The code is implemented as a class named SimplifiedAES. It encapsulates the AES functionality within the class methods. This approach allows for better organization and encapsulation of the AES operations.
Mini-AES: The code is structured as a set of separate functions that perform individual AES operations. The functions can be called independently, but they lack the encapsulation provided by the class structure.
### Key Expansion:

S-AES: The first version includes a key expansion process, where the input key is expanded to generate round keys for each round of the AES algorithm. It uses specific round constants (Rcon1 and Rcon2) and performs XOR operations with the input key to derive the round keys.
Mini-AES: The second version does not explicitly include a key expansion process. It assumes that the key is already expanded or pre-generated externally.
### Nibble Substitution:

S-AES: The first version utilizes an S-Box and an inverse S-Box for nibble substitution. The S-Box (sBox) and inverse S-Box (sBoxI) are predefined lookup tables that map each nibble to a different nibble value. The substitution is performed using these lookup tables.
Mini-AES: The second version uses hardcoded nibble substitution lookup tables (nibbleSub and nibbleSub2). Instead of using predefined lookup tables, the nibble substitution is implemented as conditional statements that check each possible nibble value and replace it with the corresponding value. This approach is less efficient and less flexible than using lookup tables.
### Performance Considerations:

S-AES: The first version employs bitwise operations, such as shifting and XORing, and utilizes efficient data structures like lists and arrays. These operations and data structures can provide better performance in terms of execution speed and memory usage.
Mini-AES: The second version separates the AES operations into individual functions. While this modular approach provides flexibility, it may introduce function call overhead, leading to potentially slower execution compared to the first version.
### Security Implications:

Both versions of the simplified AES code are not suitable for secure cryptographic purposes. They are simplified versions intended for educational or illustrative purposes and lack the necessary security features of the full AES algorithm.
The use of a hardcoded lookup table in the second version may be considered less secure than the S-Box implementation in the first version. Hardcoded lookup tables can be more prone to analysis and attacks, whereas the S-Box implementation provides a more secure and mathematically defined substitution mechanism.

## Comparison:

In terms of security, the Simplified AES is generally considered to be more secure compared to the Mini AES. It incorporates a key expansion process, utilizes an S-Box for nibble substitution, and aligns with the cryptographic principles of the AES algorithm. These factors enhance its security properties.

However, it is crucial to emphasize that neither version should be used for real-world secure cryptographic applications. Both versions are simplified and lack the necessary security features of the full AES algorithm. For secure cryptographic operations, it is essential to use the full AES algorithm as standardized and implemented by experts.

Regarding performance, the Simplified AES may offer better performance compared to the Mini AES. The first version utilizes bitwise operations and efficient data structures, potentially resulting in faster execution and optimized memory usage. The second version, with its separate function approach, may introduce function call overhead and could be less performant.

In summary, while the Simplified AES is relatively more secure and may have better performance, it remains crucial to use the full AES algorithm for real-world secure cryptographic applications. The simplified versions are primarily used for learning and understanding the basic principles of AES encryption rather than practical usage. 

## ECB with S-AES:

To implement ECB mode with Simplified AES (S-AES), you don't need to add anything to S-AES itself. ECB is a mode of operation that determines how you use the underlying block cipher (S-AES in this case) to encrypt the data.
To use S-AES in ECB mode, you simply apply the S-AES algorithm independently to each block of plaintext without any additional modifications. The key and the plaintext block are inputted into S-AES, and you obtain the corresponding ciphertext block as the output. Repeat this process for each block of the plaintext.
Here's a step-by-step procedure to encrypt data using S-AES in ECB mode:
1.	Expand the encryption key and generate the round keys as you would in S-AES.
2.	Divide the plaintext message into fixed-size blocks, with each block being 16 bytes (128 bits) in the case of S-AES.
3.	If the last block is not 16 bytes long, pad it with appropriate padding (e.g., PKCS#7 padding) to reach the desired block size.
4.	Encrypt each plaintext block separately using S-AES with the generated round keys.
5.	Concatenate the resulting ciphertext blocks together to form the final ciphertext.
