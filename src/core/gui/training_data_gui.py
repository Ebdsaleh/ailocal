# src/core/gui/training_data_gui.py
"""
THIS IS A GUI IMPLEMENTATION OF Train
This class is responsible for creating and loading the training data to train the models and adapters
"""
import json
import os
from datetime import datetime
import dearpygui.dearpygui as dpg
from src.core.paths import training_data_dir


class TrainingDataGui:
    def __init__(self, data_file_name="training_data.json"):
        self.data_dir = training_data_dir
        self.training_file = os.path.join(training_data_dir, data_file_name)
        self.history = self.load_existing_data()

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def load_existing_data(self):
        if os.path.exists(self.training_file):
            try:
                with open(self.training_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Warning: Invalid JSON, returning empty data.")
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
        timestamp = datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "user_input": user_input,
            "ai_response": ai_response
        }
        self.history.append(entry)
        self.save_data()

    def create_training_data(self, user_input, ai_response):
        self.add_entry(user_input, ai_response)
        return {"input": user_input, "output": ai_response}

    def launch_gui(self):
        dpg.create_context()

        def exit_callback():
            if dpg.get_value("exit_confirm"):
                try:
                    dpg.stop_dearpygui()
                except Exception as e:
                    print(f"Error during shutdown: {e}")

        def submit_callback():
            user_input = dpg.get_value("user_input")
            ai_response = dpg.get_value("ai_response")
            if user_input and ai_response:
                self.create_training_data(user_input, ai_response)
                dpg.set_value("feedback", "Entry added successfully!")
                dpg.set_value("user_input", "")
                dpg.set_value("ai_response", "")
            else:
                dpg.set_value("feedback", "Both fields are required.")

        def view_entries_callback():
            dpg.delete_item("entries_window", children_only=True)
            for entry in self.load_existing_data():
                dpg.add_text(f"{entry['timestamp']}: {entry['user_input']} -> {entry['ai_response']}", parent="entries_window")

        with dpg.window(label="Training Data GUI", width=600, height=400):
            dpg.add_input_text(label="User Input", tag="user_input")
            dpg.add_input_text(label="AI Response", tag="ai_response")
            dpg.add_button(label="Add Entry", callback=submit_callback)
            dpg.add_text("", tag="feedback")
            dpg.add_button(label="View Entries", callback=view_entries_callback)
            dpg.add_child_window(tag="entries_window", width=580, height=150)
            dpg.add_button(label="Exit", callback=exit_callback)  # dpg.destroy_context
            dpg.add_checkbox(label="Confirm Exit", tag="exit_confirm")
        dpg.create_viewport(title="Training Data GUI", width=620, height=450)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
