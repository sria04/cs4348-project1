# CS4348 Project 1 - Encryption System

## Description
An inter-process communication system consisting of three programs that communicate through pipes: a driver (user interface), an encryption program (Vigenère cipher backend), and a logger.

## Files

- **driver.py** - The main program. Launches the logger and encryption programs as child processes, connects to them via pipes, and provides an interactive command menu to the user.
- **encrypt.py** - The encryption backend. Accepts commands via stdin to set a passkey and encrypt/decrypt strings using the Vigenère cipher. Outputs results to stdout.
- **logger.py** - The logging program. Reads log messages from stdin and writes timestamped entries to a log file.
- **devlog.md** - Development log documenting the design process, session notes, and reflections.
- **README.md** - This file.

## How to Run

All three programs are written in Python 3 and require no external libraries.

To run the system:

```
python3 driver.py <logfile>
```

For example:

```
python3 driver.py activity.log
```

This will:
1. Start the logger (writing to `activity.log`)
2. Start the encryption program
3. Present an interactive menu

## Commands

- **password** - Set the encryption passkey. Only letters are allowed.
- **encrypt** - Encrypt a string using the current passkey. Only letters are allowed.
- **decrypt** - Decrypt a string using the current passkey. Only letters are allowed.
- **history** - Display all strings used during this session.
- **quit** - Exit the program.

## Notes for the TA

- The driver, logger, and encryption programs are three separate processes communicating through pipes using Python's `subprocess` module.
- All input is converted to uppercase internally since the Vigenère cipher is case insensitive.
- Input validation ensures only alphabetic characters are accepted for passwords, encryption, and decryption.
- Passwords are never directly logged.
- The history stores all strings entered for encryption/decryption as well as the results.
- The log file is appended to (not overwritten) so multiple runs are preserved.
