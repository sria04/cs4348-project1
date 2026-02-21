#!/usr/bin/env python3
"""
Encryption Program
Accepts commands via standard input to encrypt/decrypt strings
using a Vigenere cipher. Outputs results to standard output.

Commands:
    PASS <key>       - Set the passkey
    ENCRYPT <text>   - Encrypt text with current passkey
    DECRYPT <text>   - Decrypt text with current passkey
    QUIT             - Exit the program

Response types:
    RESULT [data]    - Command succeeded
    ERROR [message]  - Command failed
"""

import sys


def vigenere_encrypt(plaintext, key):
    """Encrypt plaintext using Vigenere cipher with given key.
    Assumes both plaintext and key are uppercase letters only."""
    result = []
    key_len = len(key)
    for i, ch in enumerate(plaintext):
        p = ord(ch) - ord('A')
        k = ord(key[i % key_len]) - ord('A')
        c = (p + k) % 26
        result.append(chr(c + ord('A')))
    return ''.join(result)


def vigenere_decrypt(ciphertext, key):
    """Decrypt ciphertext using Vigenere cipher with given key.
    Assumes both ciphertext and key are uppercase letters only."""
    result = []
    key_len = len(key)
    for i, ch in enumerate(ciphertext):
        c = ord(ch) - ord('A')
        k = ord(key[i % key_len]) - ord('A')
        p = (c - k) % 26
        result.append(chr(p + ord('A')))
    return ''.join(result)


def main():
    passkey = None

    for line in sys.stdin:
        line = line.strip()

        if not line:
            continue

        # Parse command and argument
        parts = line.split(None, 1)
        command = parts[0].upper()
        argument = parts[1] if len(parts) > 1 else ""

        if command == "QUIT":
            break
        elif command == "PASS":
            if argument:
                passkey = argument.upper()
                print("RESULT", flush=True)
            else:
                print("ERROR No passkey provided", flush=True)
        elif command == "ENCRYPT":
            if passkey is None:
                print("ERROR Password not set", flush=True)
            elif not argument:
                print("ERROR No text to encrypt", flush=True)
            else:
                encrypted = vigenere_encrypt(argument.upper(), passkey)
                print(f"RESULT {encrypted}", flush=True)
        elif command == "DECRYPT":
            if passkey is None:
                print("ERROR Password not set", flush=True)
            elif not argument:
                print("ERROR No text to decrypt", flush=True)
            else:
                decrypted = vigenere_decrypt(argument.upper(), passkey)
                print(f"RESULT {decrypted}", flush=True)
        else:
            print(f"ERROR Unknown command: {command}", flush=True)


if __name__ == "__main__":
    main()
    