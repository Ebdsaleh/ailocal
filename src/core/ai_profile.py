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
    def __init__(self, model_name, name="", gender=Gender.FEMALE, relationship_type=RelationshipType.FRIEND, mood=Mood.NEUTRAL, history=None, user_profile=None):
        """
        Initializes the AI profile with the given model, name, relationship type, and mood.
        The profile also knows to which user it belongs.
        """
        self.name = name
        self.model_name = model_name
        self.gender = gender
        self.relationship_type = relationship_type
        self.mood = mood
        self.history = history if history else []
        self.user_profile = user_profile  # Reference to the UserProfile this AI profile belongs to
        self.model = self.load_model()
        # Define the profile folder path using the user's name and AI profile name

        self.profile_folder = os.path.join(self.user_profile.profile_folder, "ai", self.name)
        # Create the profile folder if it doesn't exist
        if not os.path.exists(self.profile_folder):
            os.makedirs(self.profile_folder)
            print(f"Created new profile folder for {self.name} at {self.profile_folder}")

        # Load the profile data if available
        self.load_profile()

    def load_model(self):
        if self.model_name == "T5":
            model = T5Model(model_dir=t5_dir, ai_profile_name=self.name, user_profile_name=self.user_profile)
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
                    gender_str = profile_data.get('gender', self.gender.name)
                    self.gender = Gender[gender_str.upper()]
                    self.model_name = profile_data.get('model_name', self.model_name)
                    relationship_type_str = profile_data.get('relationship_type', self.relationship_type.name)
                    self.relationship_type = RelationshipType[relationship_type_str.upper()]
                    mood_str = profile_data.get('mood', self.mood.name)
                    self.mood = Mood[mood_str.upper()]

            # Load conversation history if the file exists
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"(file: ai_profile.py, method: load_profile) Error loading profile data: {e}")

    def save_profile(self):
        """
        Saves the AI profile data to a JSON file.
        """
        try:
            profile_data = {
                "name": self.name,
                "model_name": self.model_name,  # Save model name instead of model object
                "gender": self.gender.name,  # Save enum as a string
                "relationship_type": self.relationship_type.name,
                "mood": self.mood.name,
                "user_profile": self.user_profile.user_name
            }

            profile_file = os.path.join(self.profile_folder, "profile_data.json")

            with open(profile_file, "w") as f:
                json.dump(profile_data, f, indent=4)

            print(f"Profile saved for {self.name}.")
        except Exception as e:
            print(f"Error saving AI profile: {e}")

    def add_to_history(self, user_input, model_response):
        """
        Adds the user input and model response to the conversation history.
        """
        self.history.append({
            'user_input': user_input,
            'model_response': model_response
        })

        # Save history to a separate file (conversation_history.json)
        self.save_conversation_history()

    def save_conversation_history(self):
        """
        Saves the conversation history to a separate JSON file.
        """
        try:
            history_file = os.path.join(self.profile_folder, "conversation_history.json")
            with open(history_file, "w") as f:
                json.dump(self.history, f, indent=4)

            print(f"Conversation history saved for {self.name}.")
        except Exception as e:
            print(f"Error saving conversation history: {e}")

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
        return f"""
        AI Profile Loaded:
        -------------------
        Name: {self.name}
        Model: {self.model_name}
        Gender: {self.gender.value}
        Relationship Type: {self.relationship_type.value}
        Mood: {self.mood.value}
        User Profile: {self.user_profile.user_name}
        Chat History: {len(self.history)} messages
        -------------------
        """

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
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Ending conversation...")
                break

            context = self._build_context(user_input)
            model_response = self.model.generate_response(user_input, context)

            # Debugging
            print(f"DEBUG: Model response received: {model_response}")

            print(f"{self.name}: {model_response}")
            self.add_to_history(user_input, model_response)

    def _build_context(self, user_input):
        context = f"You are {self.name}, who has a {self.relationship_type} relationship with {self.user_profile}. You are currently in a {self.mood} mood, and you're responding in a friendly, playful, and emotionally rich tone. Your goal is to keep the conversation engaging and fun, with a touch of humor if possible."
        # context += " Respond naturally and engagingly in a friendly, conversational tone."

        history_context = "\n".join(
            [f"{entry['user_input']}\n{self.name}: {entry['model_response']}" for entry in self.history[-3:]]
        )

        if history_context:
            context += "\nHere is your recent conversation history:\n" + history_context

        context += f"\nUser: {user_input}\n{self.name}:"

        # Debugging
        print(f"DEBUG: Context being sent to model:\n{context}")

        return context

    def __repr__(self):
        history_length = len(self.history)  # Assuming self.history is a list or similar iterable
        user_profile_info = f"User Profile: {self.user_profile.user_name}"  # Adjust if necessary for your UserProfile class
        return (f"AiProfile(name={self.name}, model_name={self.model_name}, "
                f"relationship_type={self.relationship_type}, mood={self.mood}, "
                f"history_length={history_length}, {user_profile_info})")

#  Example of how to use the AiProfile class
# if __name__ == "__main__":
#     # Create a profile with the T5 model
#     profile = AiProfile(model="T5", name="Alice", gender="Female", relationship_type="Friend")
#
#     # Start a conversation with the profile
#     profile.chat()
