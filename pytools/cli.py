import sys


def main():
    """Main entry point for the command-line tool."""
    if len(sys.argv) > 1:
        print(f"Arguments: {sys.argv[1:]}")
    else:
        print("Welcome to pytools! Use '--help' for more information.")
