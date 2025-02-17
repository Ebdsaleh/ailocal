# src/core/paths.py
"""
This file holds the paths for the program.
"""
import os
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
src_dir = os.path.join(root_dir, "src")
models_dir = os.path.join(src_dir,"core", "models")
gpt2_dir = os.path.join(models_dir, "gpt2")