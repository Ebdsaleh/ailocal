# src/core/adapter_manager.py
"""
This class is responsible for adding and removing adapters to the model.
"""

import os

from peft import get_peft_model

from src.core.adapter import Adapter, default_lora_config
from src.core.paths import t5_adapters_dir
import torch
import peft
class AdapterManager:
    def __init__(self):
        self.adapter_dir = t5_adapters_dir
        self.adapters = {}

    def create_new_adapter(self, adapter_name, model, lora_config=default_lora_config):
        new_adapter = Adapter(model, lora_config)
        new_adapter.set_name(adapter_name)
        print(f"Creating new adapter: {new_adapter.name}, file path: {new_adapter.full_file_name}")
        return new_adapter

    def load_adapter(self, model, adapter_name:str, category:str=None):
        if adapter_name is None or adapter_name.isdigit():
            return False
        if category is None or category.isdigit():
            return False
        filename = f"{adapter_name}.bin"
        full_file_name = os.path.join(self.adapter_dir, filename)
        model.load_adapter(full_file_name, category)

