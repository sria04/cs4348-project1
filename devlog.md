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