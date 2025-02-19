# src/core/ai_brain.py
"""
This class is responsible for giving more of a personality to the AiProfile
"""

import re
from src.core.ai_cortex import AiCortex
from src.core.short_term_memory import ShortTermMemory
from src.core.long_term_memory import LongTermMemory

class AiBrain:
    def __init__(self, ai_profile=None):
        print("AiBrain is initializing...")
        self.ai_profile = ai_profile
        self.short_term_memory = ShortTermMemory()
        self.long_term_memory = LongTermMemory()
        self.cortex = None

    def initialize_cortex(self):
        self.cortex = AiCortex(self)
        self.load_history_from_profile()

    def get_cortex(self):
        return self.cortex

    def load_history_from_profile(self):
        if self.ai_profile:
            if self.ai_profile.history != []:
                for entry in self.ai_profile.history:
                    timestamp = entry['timestamp']
                    user_name = self.ai_profile.user_profile.user_name
                    ai_name = self.ai_profile.name
                    user_message = entry[user_name]
                    ai_message = entry[ai_name]
                    print(f"timestamp: {timestamp}\n{user_name}: {user_message}\n{ai_name}: {ai_message}")
                    self.short_term_memory.add_message(user_name, user_message, timestamp)
                    self.short_term_memory.add_message(ai_name, ai_message, timestamp)
                    self.long_term_memory.add_message(user_name, user_message, timestamp)
                    self.long_term_memory.add_message(ai_name, ai_message, timestamp)

    def infer_tone(self, text: str):
        return self.cortex.infer_tone(text)

    def adjust_mood(self):
        self.ai_profile.mood = self.cortex.adjust_mood(self.ai_profile.mood)

    def process_input(self, user_input):
        self.update_memory(user_input)

    def update_memory(self, user_input):
       self.update_short_term_memory(user_input)
       self.update_long_term_memory(user_input)

    def update_short_term_memory(self, user_input):
        self.short_term_memory.add_message(
            f"{self.ai_profile.user_profile.user_name}", user_input
        )
        response = self.ai_profile.model.generate_response(user_input)
        self.short_term_memory.add_message(f"{self.ai_profile.name}", response)
        return response

    def update_long_term_memory(self, user_input):
        self.long_term_memory.add_message(
            f"{self.ai_profile.user_profile.user_name}", user_input
        )
        response = self.ai_profile.model.generate_response(user_input)
        self.long_term_memory.add_message(f"{self.ai_profile.name}", response)
        return response

    def chat(self):
        """
        Initiates a conversation with the AI model, taking user input and using the model to generate a response.
        This method can be customized based on the profile's context (name, relationship type, mood).
        """
        print(f"{self.ai_profile.name}: Hello! How can I assist you today? (Type 'exit' to quit)")
        user_name = self.ai_profile.user_profile.user_name
        ai_name = self.ai_profile.name
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Ending conversation...")
                break

            context = self.build_context(user_input)
            model_response = self.generate_response(user_input, context)

            # Debugging
            print(f"DEBUG: Model response received: {model_response}")

            print(f"{self.ai_profile.name}: {model_response}")
            self.ai_profile.add_to_history(user_input, model_response)
            latest_entry = self.ai_profile.history[-1]
            self.short_term_memory.add_message(latest_entry[user_name],user_input, latest_entry['timestamp'] )
            self.short_term_memory.add_message(latest_entry[ai_name], model_response, latest_entry['timestamp'])
            self.long_term_memory.add_message(latest_entry[user_name], user_input, latest_entry['timestamp'])
            self.long_term_memory.add_message(latest_entry[ai_name], model_response, latest_entry['timestamp'])

    def build_context(self, user_input):
        user_name = self.ai_profile.user_profile.user_name
        ai_name = self.ai_profile.name
        inferred_tone = self.infer_tone(user_input)
        context = f"""You are {self.ai_profile.name}, who has a {self.ai_profile.relationship_type} relationship with {self.ai_profile.user_profile.user_name}.
               You are currently in a {self.ai_profile.mood} mood, and you're responding in a friendly, playful, and emotionally rich tone.
               Your goal is to keep the conversation engaging and fun, with a touch of humor if possible.
               The user’s message seems to have a {inferred_tone.name.lower()} tone.
               """

        # context += " Respond naturally and engagingly in a friendly, conversational tone."

        history_context = "\n".join(
            [f"{entry[user_name]}\n{self.ai_profile.name}: {entry[ai_name]}" for entry in self.ai_profile.history[-10:]]
        )

        if history_context:
            context += "\nHere is your recent conversation history:\n" + history_context

        context += f"\n{user_name}: {user_input}\nRespond naturally and engagingly in conversational tone that is inline with your mood"
        # Debugging
        print(f"DEBUG: Context being sent to model:\n{context}")

        return context

    def generate_response(self, user_input, context):
        # Generate response using the model or a more advanced technique
        user_name = self.ai_profile.user_profile.user_name
        response = self.ai_profile.model.generate_response(user_input, context)
        # Remove unintended echoes of the user's name
        response = re.sub(rf"\b{re.escape(user_name)}:\s*", "", response).strip()

        return response