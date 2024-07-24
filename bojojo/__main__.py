"""
Bojo entry point script
"""

import inject
from bojojo import __app_name__
from bojojo.inject_config.di_config import base_config
from bojojo.src import cli

def main():
    #config dependencies
    inject.configure(base_config())
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()