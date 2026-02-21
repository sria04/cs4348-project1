# Development Log - CS4348 Project 1

### Thoughts So Far
Just received the project specification for Project 1. This is an Operating Systems course project focused on inter-process communication using pipes. I need to build three separate programs:

1. A **logger** that writes timestamped messages to a log file
2. An **encryption program** that implements a Vigenère cipher
3. A **driver program** that spawns the other two as child processes, connects via pipes, and provides a user-facing menu

I'm choosing Python for this project. Python's `subprocess` module handles pipe-based IPC cleanly, and since we don't need external libraries, it should work fine on the cs1/cs2 machines.

The key OS concept here is inter-process communication (IPC) through pipes. The driver will be the parent process that creates two child processes and redirects their stdin/stdout through pipes. This is basically a client-server pattern at the process level.

The Vigenère cipher is a polyalphabetic substitution cipher — it's like a Caesar cipher but the shift amount changes with each letter based on a repeating keyword. For example, with key "ABC", the first letter shifts by 0, the second by 1, the third by 2, then it repeats. The formula is:
- Encrypt: `C = (P + K) mod 26`
- Decrypt: `P = (C - K) mod 26`

### Plan for This Session
I want to start with the simplest program and work my way up:
1. Implement `logger.py` first — it's the most straightforward (read stdin, format, write to file)
2. Implement `encrypt.py` — the Vigenère cipher logic plus the command parsing
3. Start sketching out `driver.py` — the subprocess spawning and pipe setup

My goal is to at least have the logger and encryption program working standalone by the end of this session.

### Session Notes — Logger Implementation

Started with `logger.py`. The required log format is `YYYY-MM-DD HH:MM [ACTION] MESSAGE`.

My approach:
- The program takes one command line argument: the log file name
- It reads lines from stdin in a loop
- Each line is parsed by splitting on whitespace — the first word becomes the ACTION, everything after becomes the MESSAGE
- I use Python's `datetime.now().strftime("%Y-%m-%d %H:%M")` for the timestamp
- The formatted entry is written to the file and flushed immediately (important so entries appear in real time, not buffered)
- The loop breaks when it receives "QUIT"

I opened the file in append mode ("a") so that multiple runs don't overwrite previous logs. Tested it manually by piping some echo commands into it and checking the output file — looks correct.

### Session Notes — Encryption Program Implementation

Moved on to `encrypt.py`. This program needs to:
- Read commands from stdin (PASS, ENCRYPT, DECRYPT, QUIT)
- Remember the current passkey between commands
- Output responses prefixed with RESULT or ERROR

For the Vigenère cipher itself, I wrote two functions:
- `vigenere_encrypt(plaintext, key)`: For each character, compute `(P + K) mod 26`
- `vigenere_decrypt(ciphertext, key)`: For each character, compute `(C - K) mod 26`

The key repeats cyclically using modulo on the index: `key[i % key_len]`.

I decided to handle everything in uppercase internally since the spec says we can assume one case. Both the passkey and the text are converted to uppercase with `.upper()` before processing.

Verified against the spec's example:
- ENCRYPT HELLO with no password → ERROR Password not set
- PASS HELLO → RESULT
- ENCRYPT HELLO with key HELLO:
  - H(7)+H(7)=14=O
  - E(4)+E(4)=8=I
  - L(11)+L(11)=22=W
  - L(11)+L(11)=22=W
  - O(14)+O(14)=28 mod 26=2=C
  - Result: OIWWC — matches the spec!

One important detail: I use `flush=True` in every `print()` call. Without this, Python might buffer the output and the driver wouldn't receive responses in time through the pipe. This cost me about 15 minutes of debugging before I realized why my test wasn't getting output.
