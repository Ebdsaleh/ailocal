# src/core/adapter_manager.py
"""
This class is responsible for adding and removing adapters to the model.
"""

import os
from src.core.adapter import Adapter
from src.core.paths import t5_adapters_dir

class AdapterManager:
    def __init__(self):
        """Initialize the AdapterManager and keep track of available adapters."""
        self.adapters = {}  # Dictionary to store loaded adapters by their name

    def create_and_save_adapter(self, name, description=None):
        """
        Create and save a new adapter.

        :param name: The name of the adapter to create.
        :param description: Optional description for the adapter.
        :return: Path to the saved adapter.
        """
        adapter = Adapter(name, description)
        return adapter.create_adapter()

    def load_adapter(self, name):
        """
        Load an adapter by its name.

        :param name: The name of the adapter to load.
        :return: Adapter instance.
        """
        adapter_path = os.path.join(t5_adapters_dir, f"{name}.adapter")

        if os.path.exists(adapter_path):
            adapter = Adapter(name)
            adapter.load_adapter(adapter_path)
            self.adapters[name] = adapter
            return adapter
        else:
            raise FileNotFoundError(f"Adapter '{name}' not found at {adapter_path}")

    def apply_adapter_to_model(self, name, model):
        """
        Apply a loaded adapter to the model.

        :param name: The name of the adapter to apply.
        :param model: The model to which the adapter should be applied.
        """
        if name in self.adapters:
            adapter = self.adapters[name]
            adapter.apply_to_model(model)
            print(f"Adapter '{name}' applied to the model.")
        else:
            raise KeyError(f"Adapter '{name}' not loaded. Please load the adapter first.")

    def get_all_adapters(self):
        """Return a list of all loaded adapter names."""
        return list(self.adapters.keys())

    def remove_adapter(self, name):
        """Remove an adapter from the manager."""
        if name in self.adapters:
            del self.adapters[name]
            print(f"Adapter '{name}' removed.")
        else:
            raise KeyError(f"Adapter '{name}' not found in the manager.")

