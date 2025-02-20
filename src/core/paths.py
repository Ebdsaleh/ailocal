# src/core/paths.py
"""
This file holds the paths for the program.
"""
import os
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
src_dir = os.path.join(root_dir, "src")
models_dir = os.path.join(src_dir,"core", "models")
gpt2_dir = os.path.join(models_dir, "gpt2")
open_llama_dir = os.path.join(models_dir,"openllama")
falcon_dir = os.path.join(models_dir, "falcon", "7b")
gpt_neo_dir = os.path.join(models_dir, "gpt-neo", "safe")
t5_dir = os.path.join(models_dir, "t5", "safe")
profiles_dir = os.path.join(root_dir,"profiles")
adapters_dir = os.path.join(src_dir, "core", "adapters")
t5_adapters_dir = os.path.join(adapters_dir, "t5")
training_data_dir = os.path.join(src_dir,"core", "training data")