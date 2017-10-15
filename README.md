# Polymorphic-Cipher
An attempt at making a polymorphic cipher. The polymorphism will be based off of the number of iterations it takes the decimal value of the binary representation of the key to reach 1 when run through the Collatz function. Well, at least as a start to ordering the substitution and transposition ciphers.

Perhaps a more simple explanation is required?
1. Recieve key as plaintext.
2. Convert to binary.
3. Convert to decimal value.
4. Run decimal value through collatz function while keeping count of iterations.
5. Use the iteration value for determining the order of the substitution and transposition. 
  a. This should make it more difficult to crack due to the "last on, first off" rule.
  b. It should be noted that doing two XOR back-to-back will result in the plaintext being returned.
