# src/core/context.py
"""
This class is responsible for generating the context for conversations.
"""


class Context:
    def __init__(self, ai_profile):
        """
        Initialize the context for the AI model.
        :param ai_profile: The AiProfile instance containing AI-specific details.
        """
        self.ai_profile = ai_profile
        self.personality = ""  # Placeholder for personality traits
        self.initial_context = None
        self.relationship_status = ai_profile.relationship_type
        self.mood = ai_profile.mood
        self.history = []  # Stores formatted conversation snippets
        self.prompts = []
        """Consider changing to a dict
        self.prompts = {
            "identity": [],
            "relationship": [],
            "mood": [],
            "history": []
        }"""
        self.create_initial_context()

    def update_mood(self, new_mood):
        """Update the AI's mood based on interactions."""
        self.mood = new_mood

    def add_to_history(self, user_message, ai_message, timestamp):
        """
        Append a user-AI interaction to the conversation history.
        """
        user_name = self.ai_profile.get_user_profile_name()
        ai_name = self.ai_profile.get_name()
        self.history.append({
            "timestamp": timestamp,
            f"{user_name}": user_message,
            f"{ai_name}": ai_message
        })

    def generate_context_string(self):
        """
        Build and return the formatted context string for the AI model.
        """
        history_text = "\nRecent conversation:\n"
        user_name = self.ai_profile.get_user_profile_name()
        ai_name = self.ai_profile.get_name()
        for entry in self.history[-5:]:  # Keep only the last 5 exchanges
            history_text += f"{user_name}: {entry[f'{user_name}']}\n"
            history_text += f"{ai_name}: {entry[f'{ai_name}']}\n"

        context_string = str(self.initial_context + history_text)
        #return personality_text + history_text
        return context_string

    def create_initial_context(self):
        name_text = f"Your name is {self.ai_profile.get_name()}.\n"
        gender_text = f"Your gender is {self.ai_profile.get_gender().value}.\n"
        user_name = self.ai_profile.get_user_profile_name()
        user_profile_text = f"The name of the person speaking to you is {user_name}"
        relationship_text = f"You're in a {self.ai_profile.get_relationship_type().value} relationship with {user_name}.\n"
        initial_context = str(name_text + gender_text + relationship_text + user_profile_text)
        self.initial_context = initial_context