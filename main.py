#!/usr/bin/env python
from cli import cli
import os
from pathlib import Path

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    cli()
