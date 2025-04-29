"""
ScreenTranslator - A tool for translating text from screen captures.
"""

import sys
from screentranslator.app import run_application


def main():
    """Entry point for the screen translator application."""
    return run_application(sys.argv[1:])


if __name__ == '__main__':
    main()
