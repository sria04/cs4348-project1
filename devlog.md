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

### Session Notes — Driver Program Implementation

This is the most complex part. The driver needs to:
1. Spawn `logger.py` and `encrypt.py` as child processes
2. Connect to their stdin/stdout via pipes
3. Present an interactive menu to the user
4. Maintain a history of strings

**Subprocess setup:** I used `subprocess.Popen` with `stdin=subprocess.PIPE` and `stdout=subprocess.PIPE` (for the encryption program) and `text=True` for automatic string encoding. The logger only needs stdin (it writes to a file, not stdout). The encryption program needs both stdin and stdout pipes since we send commands and read responses.

**Finding the scripts:** I used `os.path.dirname(os.path.abspath(__file__))` to find the directory where `driver.py` lives. This way, it can locate `logger.py` and `encrypt.py` regardless of what directory the user runs the command from.

**Helper functions I created:**
- `send_to_process()` — writes a line to a subprocess's stdin and flushes
- `read_from_process()` — reads a line from a subprocess's stdout
- `log_message()` — convenience wrapper to send formatted log messages
- `get_string_from_user()` — handles the "new string or history?" menu for encrypt/decrypt
- `get_password_from_user()` — similar menu but passwords don't go into history
- `validate_alpha()` — checks input contains only letters using `str.isalpha()`

**Important design decisions:**
- The spec says "password" is used by the driver and "passkey" is used by the encryption program. So when the user types "password", the driver sends "PASS" to encrypt.py.
- Passwords are NOT stored in the history (per spec).
- Encrypted/decrypted results ARE stored in the history.
- Input is converted to uppercase before sending to the encryption program.
- The driver validates input before sending — only letters allowed, no spaces or special characters.

**The menu loop:** Each iteration prints the menu, reads a command, and dispatches to the appropriate handler. Every command and its result gets logged. On "quit", the driver sends QUIT to both child processes and waits for them to finish with `.wait()`.

### End of Session 1 Reflection

I accomplished my main goal — all three programs are implemented. The logger and encrypt programs work standalone when tested manually. The driver compiles and runs, spawning both children correctly.

Things that went well:
- The Vigenère cipher was straightforward to implement
- Python's subprocess module made pipe management clean
- The modular design with helper functions keeps driver.py readable

Things I need to do next session:
- Full integration testing (run the whole system end-to-end)
- Test edge cases (empty history, no password, invalid characters)
- Verify the log file output format is exactly right
- Make sure the quit sequence is clean (no zombie processes)

### Thoughts So Far
Had some time to think about potential issues since last session. One thing I want to verify is that the history behaves correctly — new strings entered for encrypt/decrypt get added, results get added, but passwords never do. Also want to make sure the "cancel" option works when browsing history.

### Plan for This Session
1. Run a full end-to-end test of the system
2. Test all the edge cases I can think of
3. Verify log file format matches the spec exactly
4. Clean up any issues found

### Session Notes — Integration Testing

Ran `python3 driver.py test.log` and tested the full workflow:

**Test 1: Basic encrypt flow**
- Entered "password" → chose "new" → typed "HELLO" → "Password set successfully"
- Entered "encrypt" → chose "new" → typed "HELLO" → got "OIWWC"
- Entered "history" → shows [1. HELLO, 2. OIWWC]

**Test 2: Decrypt round-trip**
- Entered "decrypt" → chose "history" → selected "OIWWC" → got "HELLO"
- History now has [1. HELLO, 2. OIWWC, 3. HELLO]

**Test 3: No password error**
- Started a fresh run, immediately tried "encrypt" with "TEST" → "ERROR: Password not set"

**Test 4: Invalid input**
- Tried to encrypt "Hello World!" → "Error: Input must contain only letters"
- Tried password "abc123" → same error
- Tried encrypt "Hello" → works fine, converted to uppercase

**Test 5: Case insensitivity**
- Set password "hello", encrypted "HELLO" → got same result as password "HELLO" encrypt "HELLO"

**Test 6: Quit sequence**
- Entered "quit" → "Goodbye!" printed, both child processes terminated cleanly
- No zombie processes left (checked with `ps`)

**Log file verification:**
Opened `test.log` after the run. Entries look like:
```
2025-02-21 14:05 [START] Driver program started.
2025-02-21 14:05 [COMMAND] password
2025-02-21 14:05 [RESULT] Password set successfully
2025-02-21 14:06 [COMMAND] encrypt
2025-02-21 14:06 [RESULT] Encrypted text: OIWWC
```
Format matches the spec: `YYYY-MM-DD HH:MM [ACTION] MESSAGE`

All tests pass. The system works correctly end-to-end.

### End of Session 2 Reflection

Everything works as expected. All the edge cases I tested pass. The pipe communication between the three processes is solid — no hangs, no buffering issues, no zombie processes.

The project is functionally complete. I still need to write the README for submission. Looking back, the hardest part was getting the pipe communication right (the flush issue in encrypt.py) and making sure the history logic matched the spec exactly (passwords not stored, results stored, cancel option available).

Overall I'm happy with how the code turned out. The separation into three programs with clean interfaces makes it easy to test each piece independently, which is exactly what IPC is about.

### Final Session — README and Submission Prep

Added a README.md describing all the files, how to run the program (`python3 driver.py <logfile>`), and notes for the TA. Double-checked that no external libraries are used — everything is from Python's standard library (sys, subprocess, os, datetime).

Verified `git status` shows a clean working tree. Project is ready for submission.
