#!/usr/bin/env python
from api.cli import cli
import os
from pathlib import Path

if __name__ == "__main__":
    directory = Path(__file__).parent
    os.chdir(directory)
    cli()
