"""
Bojo entry point script
"""

import inject
from bojo import __app_name__
from bojo.inject_config.di_config import base_config
from bojo.src import cli

def main():
    #config dependencies
    inject.configure(base_config)
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()