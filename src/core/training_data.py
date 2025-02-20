# src/core/training_data.py
"""
This class is responsible for creating and loading the training data to train the models and adapters
"""
import json
import os
from datetime import datetime
from src.core.paths import training_data_dir

class TrainingData:
    def __init__(self, data_file_name="training_data.json"):
        """
        Initialize the TrainingData class.
        :param data_file_name: Name of the file the training data will be stored.
        """
        self.data_dir = training_data_dir
        self.training_file = os.path.join(training_data_dir, data_file_name)
        self.history = self.load_existing_data()

        # Ensure the data directory exists
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def load_existing_data(self):
        """
        Load existing training data from the file, if it exists.
        """
        if os.path.exists(self.training_file):
            try:
                with open(self.training_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Warning: The training data file is not a valid JSON file, returning empty data.")
                return []
        return []

    def save_data(self):
        """
        Save the collected data to the training data file.
        """
        # Load existing data, if any
        if os.path.exists(self.training_file):
            try:
                with open(self.training_file, "r") as f:
                    existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
        else:
            existing_data = []

        # Append new history and clear it after saving
        existing_data.extend(self.history)
        with open(self.training_file, "w") as f:
            json.dump(existing_data, f, indent=4)

        # Clear history after saving to avoid duplicates
        self.history.clear()

    def add_entry(self, user_input, ai_response):
        """
        Add a new conversation entry to the training data.
        :param user_input: The input text from the user.
        :param ai_response: The AI's response to the input.
        """
        timestamp = datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "user_input": user_input,
            "ai_response": ai_response
        }
        self.history.append(entry)
        self.save_data()

    def format_entry_for_training(self, user_input, ai_response):
        """
        Format the conversation into the format needed for training the model.
        :param user_input: The input from the user.
        :param ai_response: The response from the AI.
        :return: The formatted entry for training.
        """
        formatted_entry = {
            "input": f"{user_input}",
            "output": f"{ai_response}"
        }
        return formatted_entry

    def create_training_data(self, user_input, ai_response):
        """
        Generate and save a training entry for the AI model.
        :param user_input: The input from the user.
        :param ai_response: The response from the AI.
        """
        formatted_entry = self.format_entry_for_training(user_input, ai_response)
        self.add_entry(user_input, ai_response)
        return formatted_entry

    def run(self):
        menu_screen = f"""
            *****************************************************************************
            *                       Training Data Menu                                  *
            *****************************************************************************
            *(1) Input New Data for file : '{self.training_file}'.                      *
            *(2) Quit Training Data Menu.                                               *
            *****************************************************************************"""
        while True:
            print(menu_screen)
            choice = input("Enter your selection:")
            if choice.isdigit():
                if choice == "1":
                    self.input_new_data()
                elif choice == "2":
                    print("Exiting program....")
                    break
            else:
                input("Invalid input detected. You must enter a number from the menu!")

    def input_new_data(self):
        """
               ask the user for inputs and outputs

               """
        while True:
            print("Input training data, (type :quit or :exit) to finish")
            user_input = input("User Input: ")
            if user_input.lower() == ":quit" or user_input.lower() == ":exit":
                print("exiting training")
                break
            ai_response = input("Ai Response:")
            if ai_response.lower() == ":quit" or ai_response.lower() == ":exit":
                print("exiting training")
                break
            # Add entry and save the changes
            entry = self.create_training_data(user_input, ai_response)
            print(f"Entry added successfully.\n{entry}")

