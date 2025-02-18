# src/core/user_profile.py
"""
This class is used for managing a User's profiles, which can contain multiple AiProfiles.
It stores and manages different AI personalities, relationship types, and moods.
"""
import os
import json
from src.core.paths import profiles_dir
from src.core.ai_profile import AiProfile
from src.core.contructs import Gender, Mood, RelationshipType
class UserProfile:
    def __init__(self, user_name, gender):
        """
        Initializes the user profile with the given user's name.
        """
        self.user_name = user_name
        self.gender = gender
        self.ai_profiles = {}  # Dictionary to store AiProfiles
        self.default_profile = None  # Store the default profile for chatting
        self.profile_folder = os.path.join(profiles_dir, self.user_name)

        # Create the user's folder if it doesn't exist
        if not os.path.exists(self.profile_folder):
            os.makedirs(self.profile_folder)
            print(f"Created new user folder for {self.user_name} at {self.profile_folder}")

        # Load the user profile data if available
        self.load_profile()

    def add_ai_profile(self, ai_profile):
        """
        Adds a new AiProfile to the user's profile collection.
        """
        if ai_profile.name in self.ai_profiles:
            print(f"Profile with the name {ai_profile.name} already exists.")
        else:
            self.ai_profiles[ai_profile.name] = ai_profile
            print(f"Added new AI profile: {ai_profile.name}")
            self.save_profile()

    def remove_profile(self, profile_name):
        """
        Removes an AI profile from the user's profile collection.
        """
        if profile_name in self.ai_profiles:
            del self.ai_profiles[profile_name]
            print(f"Removed AI profile: {profile_name}")
            self.save_profile()
        else:
            print(f"Profile with the name {profile_name} does not exist.")

    def set_default_profile(self, profile_name):
        """
        Sets the default AI profile for the user.
        """
        if profile_name in self.ai_profiles:
            self.default_profile = self.ai_profiles[profile_name]
            print(f"Set default profile to: {profile_name}")
        else:
            print(f"Profile with the name {profile_name} does not exist.")

    def get_default_profile(self):
        """
        Returns the default AI profile.
        """
        return self.default_profile

    def save_profile(self):
        """
        Saves the user profile and all AI profiles to the user's folder as JSON files.
        """
        try:
            # Save the user profile data (including AI profiles) to a JSON file
            user_profile_file = os.path.join(self.profile_folder, f"{self.user_name}.json")
            user_data = {
                "user_name": self.user_name,
                "default_profile": self.default_profile.name if self.default_profile else None,
                "ai_profiles": {name: profile.name for name, profile in self.ai_profiles.items()}
            }

            with open(user_profile_file, 'w') as f:
                json.dump(user_data, f, indent=4)

            print(f"User profile saved for {self.user_name}.")

        except Exception as e:
            print(f"Error saving user profile: {e}")

    def load_profile(self):
        """
        Loads the user profile data from the user's folder, including AI profiles.
        """
        try:
            user_profile_file = os.path.join(self.profile_folder, f"{self.user_name}.json")

            if os.path.exists(user_profile_file):
                with open(user_profile_file, 'r') as f:
                    user_data = json.load(f)

                    self.user_name = user_data.get('user_name', self.user_name)
                    default_profile_name = user_data.get('default_profile')
                    ai_profiles_data = user_data.get('ai_profiles', {})

                    # Load the AI profiles
                    for profile_name in ai_profiles_data:
                        # Assuming the AI model folder is pre-loaded, you can instantiate them here
                        ai_profile = AiProfile(model="T5", name=profile_name)  # Placeholder for model type
                        self.ai_profiles[profile_name] = ai_profile

                    # Set the default profile if specified
                    if default_profile_name and default_profile_name in self.ai_profiles:
                        self.default_profile = self.ai_profiles[default_profile_name]

            else:
                print("No user profile data found, starting with an empty profile.")
        except Exception as e:
            print(f"Error loading user profile: {e}")

    def get_profile_summary(self):
        """
        Returns a summary of the user profile, including the default profile's name.
        """
        default_profile_name = self.default_profile.name if self.default_profile else "None"
        return f"User: {self.user_name}, Default Profile: {default_profile_name}"

    def get_ai_profiles(self):
        return self.ai_profiles
