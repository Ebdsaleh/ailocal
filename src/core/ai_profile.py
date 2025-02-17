# src/core/ai_profile.py
"""
This class is used for creating an AI's profile that users can chat with.
Each AI profile belongs to a specific user, and it's stored under the user's folder in the 'ai' subfolder.
"""
import os
import json
from src.core.contructs import Gender, RelationshipType, Mood
from src.core.paths import profiles_dir, t5_dir
from src.core.t5_model import T5Model


class AiProfile:
    def __init__(self, model, name="", gender=Gender.FEMALE, relationship_type=RelationshipType.FRIEND, mood=Mood.NEUTRAL, history=None, user_profile=None):
        """
        Initializes the AI profile with the given model, name, relationship type, and mood.
        The profile also knows to which user it belongs.
        """
        self.model = self.load_model(model)
        self.name = name
        self.gender = gender
        self.relationship_type = relationship_type
        self.mood = mood
        self.history = history if history else []
        self.user_profile = user_profile  # Reference to the UserProfile this AI profile belongs to

        # Define the profile folder path using the user's name and AI profile name
        self.profile_folder = os.path.join(self.user_profile.profile_folder, "ai", self.name)

        # Create the profile folder if it doesn't exist
        if not os.path.exists(self.profile_folder):
            os.makedirs(self.profile_folder)
            print(f"Created new profile folder for {self.name} at {self.profile_folder}")

        # Load the profile data if available
        self.load_profile()

    def load_model(self, model_name):
        if model_name == "T5":
            model = T5Model(model_dir=t5_dir)
            return model

    def load_profile(self):
        """
        Loads the profile data (name, relationship_type, mood, and conversation history)
        from the profile folder if the files exist.
        """
        try:
            profile_file = os.path.join(self.profile_folder, "profile_data.json")
            history_file = os.path.join(self.profile_folder, "conversation_history.json")

            # Load profile data if the file exists
            if os.path.exists(profile_file):
                with open(profile_file, 'r') as f:
                    profile_data = json.load(f)
                    self.name = profile_data.get('name', self.name)
                    self.relationship_type = RelationshipType(profile_data.get('relationship_type', self.relationship_type.name))
                    self.mood = Mood(profile_data.get('mood', self.mood.name))

            # Load conversation history if the file exists
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    self.history = json.load(f)

        except Exception as e:
            print(f"Error loading profile data: {e}")

    def save_profile(self):
        """
        Saves the profile data (name, relationship_type, mood) and conversation history
        to the profile folder as JSON files.
        """
        try:
            profile_data = {
                'name': self.name,
                'relationship_type': self.relationship_type.name,
                'mood': self.mood.name,
                'user_profile': self.user_profile.user_name  # Reference to the user's profile name
            }

            # Save the profile data to a JSON file
            profile_file = os.path.join(self.profile_folder, "profile_data.json")
            with open(profile_file, 'w') as f:
                json.dump(profile_data, f, indent=4)

            # Save the conversation history to a JSON file
            history_file = os.path.join(self.profile_folder, "conversation_history.json")
            with open(history_file, 'w') as f:
                json.dump(self.history, f, indent=4)

            print(f"Profile and history saved for {self.name}.")

        except Exception as e:
            print(f"Error saving profile data: {e}")

    def add_to_history(self, user_input, model_response):
        """
        Adds the user input and model response to the conversation history.
        """
        self.history.append({
            'user_input': user_input,
            'model_response': model_response
        })
        self.save_profile()  # Save profile after adding to history

    def update_profile(self, name=None, relationship_type=None, mood=None):
        """
        Updates the user's profile details (name, relationship_type, mood).
        """
        if name:
            self.name = name
        if relationship_type:
            self.relationship_type = relationship_type
        if mood:
            self.mood = mood
        self.save_profile()  # Save profile after updating

    def get_profile_summary(self):
        """
        Returns a string summary of the profile, including name, relationship type, and mood.
        """
        return f"Name: {self.name}, Relationship Type: {self.relationship_type.value}, Mood: {self.mood.value}"

    def clear_history(self):
        """
        Clears the conversation history.
        """
        self.history = []
        self.save_profile()  # Save profile after clearing history

    def get_conversation_history(self):
        """
        Returns the entire conversation history.
        """
        return self.history

    def chat(self):
        """
        Initiates a conversation with the AI model, taking user input and using the model to generate a response.
        This method can be customized based on the profile's context (name, relationship type, mood).
        """
        print(f"{self.name}: Hello! How can I assist you today? (Type 'exit' to quit)")

        while True:
            # Take user input
            user_input = input("You: ")

            # If the user types 'exit', end the conversation
            if user_input.lower() == 'exit':
                print("Ending conversation...")
                break

            # Generate a response from the model, using the conversation history for context
            context = self._build_context(user_input)
            model_response = self.model.generate_response(user_input, context)

            # Print model's response
            print(f"{self.name}: {model_response}")

            # Add the user input and response to history
            self.add_to_history(user_input, model_response)

    def _build_context(self, user_input):
        """
        Builds a conversational context for the AI, integrating history in a natural way.
        """
        context = f"You are {self.name}, who has a {self.relationship_type.value.lower()} relationship with {self.user_profile.user_name}. You are currently in a {self.mood.value.lower()} mood."
        context += " Respond naturally and engagingly in a friendly, conversational tone."

        # Format conversation history correctly
        history_context = "\n".join(
            [f"{entry['user_input']}\n{self.name}: {entry['model_response']}" for entry in self.history[-5:]]
        )

        if history_context:
            context += "\nHere is your recent conversation history:\n" + history_context

        # Add the most recent user input for context
        context += f"\nUser: {user_input}\n{self.name}:"

        # Detecting and handling action-based input (narrative)
        if "*" in user_input:  # This is a simple heuristic for narrative-style inputs
            context += " Respond with a comment on the situation or ask a follow-up question."

        return context

#  Example of how to use the AiProfile class
# if __name__ == "__main__":
#     # Create a profile with the T5 model
#     profile = AiProfile(model="T5", name="Alice", gender="Female", relationship_type="Friend")
#
#     # Start a conversation with the profile
#     profile.chat()
