#!/usr/bin/env python3
"""
Driver Program
Main program that launches the logger and encryption programs,
communicates with them through pipes, and provides an interactive
menu to the user.

Usage: python3 driver.py <logfile>
"""

import sys
import subprocess
import os


def send_to_process(process, message):
    """Send a message to a subprocess via its stdin pipe."""
    process.stdin.write(message + "\n")
    process.stdin.flush()


def read_from_process(process):
    """Read a line of output from a subprocess via its stdout pipe."""
    line = process.stdout.readline().strip()
    return line


def log_message(logger_proc, action, message):
    """Send a log message to the logger process."""
    send_to_process(logger_proc, f"{action} {message}")


def validate_alpha(text):
    """Check that text contains only alphabetic characters."""
    return text.isalpha()


def get_string_from_user(history):
    """Prompt user to enter a new string or select from history.
    Returns the chosen string or None if cancelled."""
    print("\n  1. Enter a new string")
    print("  2. Use a string from history")
    choice = input("  Choice: ").strip()

    if choice == "1":
        text = input("  Enter string: ").strip()
        return text, True  # True means it's a new string
    elif choice == "2":
        if not history:
            print("  History is empty. Please enter a new string.")
            text = input("  Enter string: ").strip()
            return text, True
        else:
            print("\n  History:")
            for i, item in enumerate(history):
                print(f"    {i + 1}. {item}")
            print(f"    {len(history) + 1}. Cancel (enter a new string instead)")
            selection = input("  Select a number: ").strip()
            try:
                idx = int(selection)
                if 1 <= idx <= len(history):
                    return history[idx - 1], False  # False means from history
                elif idx == len(history) + 1:
                    text = input("  Enter string: ").strip()
                    return text, True
                else:
                    print("  Invalid selection.")
                    return None, False
            except ValueError:
                print("  Invalid input.")
                return None, False
    else:
        print("  Invalid choice.")
        return None, False


def get_password_from_user(history):
    """Prompt user to enter a new password or select from history.
    Returns the chosen password or None if cancelled."""
    print("\n  1. Enter a new password")
    print("  2. Use a string from history")
    choice = input("  Choice: ").strip()

    if choice == "1":
        text = input("  Enter password: ").strip()
        return text
    elif choice == "2":
        if not history:
            print("  History is empty. Please enter a new password.")
            text = input("  Enter password: ").strip()
            return text
        else:
            print("\n  History:")
            for i, item in enumerate(history):
                print(f"    {i + 1}. {item}")
            print(f"    {len(history) + 1}. Cancel (enter a new password instead)")
            selection = input("  Select a number: ").strip()
            try:
                idx = int(selection)
                if 1 <= idx <= len(history):
                    return history[idx - 1]
                elif idx == len(history) + 1:
                    text = input("  Enter password: ").strip()
                    return text
                else:
                    print("  Invalid selection.")
                    return None
            except ValueError:
                print("  Invalid input.")
                return None
    else:
        print("  Invalid choice.")
        return None


def print_menu():
    """Print the command menu."""
    print("\n--- Encryption System Menu ---")
    print("  password  - Set the encryption password")
    print("  encrypt   - Encrypt a string")
    print("  decrypt   - Decrypt a string")
    print("  history   - Show string history")
    print("  quit      - Exit the program")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 driver.py <logfile>", file=sys.stderr)
        sys.exit(1)

    log_filename = sys.argv[1]

    # Get the directory where driver.py is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Launch the logger process
    logger_proc = subprocess.Popen(
        [sys.executable, os.path.join(script_dir, "logger.py"), log_filename],
        stdin=subprocess.PIPE,
        text=True
    )

    # Launch the encryption process
    encrypt_proc = subprocess.Popen(
        [sys.executable, os.path.join(script_dir, "encrypt.py")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )

    # History of strings used during this session
    history = []

    # Log the start of the program
    log_message(logger_proc, "START", "Driver program started.")

    print("Welcome to the Encryption System!")

    while True:
        print_menu()
        command = input("\nEnter command: ").strip().lower()

        if command == "password":
            log_message(logger_proc, "COMMAND", "password")

            password = get_password_from_user(history)
            if password is None:
                print("  Operation cancelled.")
                log_message(logger_proc, "RESULT", "password command cancelled")
                continue

            # Validate: only letters allowed
            if not validate_alpha(password):
                print("  Error: Password must contain only letters (no spaces, numbers, or special characters).")
                log_message(logger_proc, "ERROR", "Invalid password input - non-alphabetic characters")
                continue

            # Send PASS command to encryption program
            send_to_process(encrypt_proc, f"PASS {password.upper()}")
            response = read_from_process(encrypt_proc)

            if response.startswith("RESULT"):
                print("  Password set successfully.")
                log_message(logger_proc, "RESULT", "Password set successfully")
            else:
                error_msg = response.split(None, 1)[1] if len(response.split(None, 1)) > 1 else "Unknown error"
                print(f"  Error: {error_msg}")
                log_message(logger_proc, "ERROR", error_msg)

        elif command == "encrypt":
            log_message(logger_proc, "COMMAND", "encrypt")

            text, is_new = get_string_from_user(history)
            if text is None:
                print("  Operation cancelled.")
                log_message(logger_proc, "RESULT", "encrypt command cancelled")
                continue

            # Validate: only letters allowed
            if not validate_alpha(text):
                print("  Error: Input must contain only letters (no spaces, numbers, or special characters).")
                log_message(logger_proc, "ERROR", "Invalid encrypt input - non-alphabetic characters")
                continue

            # Add to history if it's a new string
            if is_new:
                history.append(text.upper())

            # Send ENCRYPT command to encryption program
            send_to_process(encrypt_proc, f"ENCRYPT {text.upper()}")
            response = read_from_process(encrypt_proc)

            parts = response.split(None, 1)
            resp_type = parts[0] if parts else ""
            resp_data = parts[1] if len(parts) > 1 else ""

            if resp_type == "RESULT":
                print(f"  Encrypted: {resp_data}")
                history.append(resp_data)
                log_message(logger_proc, "RESULT", f"Encrypted text: {resp_data}")
            else:
                print(f"  Error: {resp_data}")
                log_message(logger_proc, "ERROR", resp_data)

        elif command == "decrypt":
            log_message(logger_proc, "COMMAND", "decrypt")

            text, is_new = get_string_from_user(history)
            if text is None:
                print("  Operation cancelled.")
                log_message(logger_proc, "RESULT", "decrypt command cancelled")
                continue

            # Validate: only letters allowed
            if not validate_alpha(text):
                print("  Error: Input must contain only letters (no spaces, numbers, or special characters).")
                log_message(logger_proc, "ERROR", "Invalid decrypt input - non-alphabetic characters")
                continue

            # Add to history if it's a new string
            if is_new:
                history.append(text.upper())

            # Send DECRYPT command to encryption program
            send_to_process(encrypt_proc, f"DECRYPT {text.upper()}")
            response = read_from_process(encrypt_proc)

            parts = response.split(None, 1)
            resp_type = parts[0] if parts else ""
            resp_data = parts[1] if len(parts) > 1 else ""

            if resp_type == "RESULT":
                print(f"  Decrypted: {resp_data}")
                history.append(resp_data)
                log_message(logger_proc, "RESULT", f"Decrypted text: {resp_data}")
            else:
                print(f"  Error: {resp_data}")
                log_message(logger_proc, "ERROR", resp_data)

        elif command == "history":
            log_message(logger_proc, "COMMAND", "history")

            if not history:
                print("\n  History is empty.")
            else:
                print("\n  String History:")
                for i, item in enumerate(history):
                    print(f"    {i + 1}. {item}")

            log_message(logger_proc, "RESULT", f"History displayed ({len(history)} items)")

        elif command == "quit":
            log_message(logger_proc, "COMMAND", "quit")
            log_message(logger_proc, "STOP", "Driver program exiting.")

            # Send QUIT to encryption program
            send_to_process(encrypt_proc, "QUIT")

            # Send QUIT to logger
            send_to_process(logger_proc, "QUIT")

            # Wait for child processes to finish
            encrypt_proc.wait()
            logger_proc.wait()

            print("Goodbye!")
            break

        else:
            print(f"  Unknown command: '{command}'. Please try again.")
            log_message(logger_proc, "ERROR", f"Unknown command: {command}")


if __name__ == "__main__":
    main()