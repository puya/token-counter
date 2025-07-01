#!/usr/bin/env python3
"""
Entry point for running token_counter as a module.
Enables: python -m token_counter
"""

from token_counter.cli import app

if __name__ == "__main__":
    app()