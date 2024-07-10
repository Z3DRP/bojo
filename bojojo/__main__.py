"""
Bojo entry point script
"""

from bojojo import __app_name__
from bojojo.src import cli

def main():
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()