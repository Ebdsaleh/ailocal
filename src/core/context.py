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
        self.relationship_status = ai_profile.relationship_type
        self.mood = ai_profile.mood
        self.history = []  # Stores formatted conversation snippets
        self.prompts = []


    def update_mood(self, new_mood):
        """Update the AI's mood based on interactions."""
        self.mood = new_mood

    def add_to_history(self, user_message, ai_message, timestamp):
        """
        Append a user-AI interaction to the conversation history.
        """
        self.history.append({
            "timestamp": timestamp,
            "user": user_message,
            "ai": ai_message
        })

    def generate_context_string(self):
        """
        Build and return the formatted context string for the AI model.
        """
        personality_text = f"You are {self.ai_profile.name}. "
        personality_text += f"You have a {self.relationship_status} relationship with {self.ai_profile.user_profile.user_name}. "
        personality_text += f"You are currently feeling {self.mood}. "

        history_text = "\nRecent conversation:\n"
        for entry in self.history[-5:]:  # Keep only the last 5 exchanges
            history_text += f"{self.ai_profile.user_profile.user_name}: {entry['user']}\n"
            history_text += f"{self.ai_profile.name}: {entry['ai']}\n"

        return personality_text + history_text