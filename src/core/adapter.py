# src/core/adapter.py
"""
This class is responsible for creating adapters
"""
import os
import json
from src.core.paths import t5_adapters_dir


class Adapter:
    def __init__(self, name, description=None):
        """
        Initialize the adapter with a name and optional description.

        :param name: The name of the adapter (e.g., "RomanticAdapter").
        :param description: A brief description of what this adapter is meant to do.
        """
        self.name = name
        self.description = description or "No description provided."
        self.adapter_file = f"{self.name}.adapter"
        self.training_data = []  # Placeholder for the training data

    def create_adapter(self):
        """
        Creates an adapter file by serializing the current adapter properties.
        Saves it as a .adapter file.

        :return: The path to the saved adapter file.
        """
        adapter_data = {
            "name": self.name,
            "description": self.description,
            "training_data": self.training_data  # Store the training data
        }

        # Assuming adapters will be stored in a directory 'adapters/'
        adapter_path = os.path.join(t5_adapters_dir, self.adapter_file)
        os.makedirs(os.path.dirname(adapter_path), exist_ok=True)
        with open(adapter_path, 'w') as f:
            json.dump(adapter_data, f, indent=4)

        print(f"Adapter '{self.name}' saved to: {adapter_path}")
        return adapter_path

    def load_adapter(self, adapter_file):
        """
        Load an existing adapter from a file.

        :param adapter_file: Path to the .adapter file to load.
        """
        with open(adapter_file, 'r') as f:
            adapter_data = json.load(f)

        self.name = adapter_data['name']
        self.description = adapter_data['description']
        self.training_data = adapter_data['training_data']

        print(f"Adapter '{self.name}' loaded from {adapter_file}.")

    def apply_to_model(self, model):
        """
        Apply the adapter's training data to a given model.

        :param model: The model to which the adapter should be applied.
        """
        print(f"Applying adapter '{self.name}' to the model.")

        # Logic to apply the training data from the adapter to the model
        # This can involve adjusting model behavior, adding tokens, or fine-tuning the model
        # For now, this function is just a placeholder.
        pass
