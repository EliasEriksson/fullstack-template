#!/usr/bin/env python
from cli import cli
import os
from pathlib import Path

if __name__ == "__main__":
    directory = Path(__file__).parent
    os.chdir(directory)
    print(f"working directory{directory.absolute()}")
    print("\n".join((str(path.absolute()) for path in directory.iterdir())))
    cli()
