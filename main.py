# main.py
"""
Entry point for the program. Might refactor later.
"""
import os
import json
from src.core.user_profile import UserProfile
from src.core.ai_profile import AiProfile
from src.core.paths import profiles_dir
from src.core.contructs import Gender, RelationshipType, Mood

def check_for_existing_user_profile():
    """
       Checks if there are any user profiles in the 'profiles' directory.
       Returns True if user profiles exist, otherwise False.
    """
    # Check if the user profile exists
    if os.path.exists(profiles_dir):
        # List all folders in the 'profiles' directory
        user_folders = [folder for folder in os.listdir(profiles_dir) if
                        os.path.isdir(os.path.join(profiles_dir, folder))]
        # Return True if any user folder exists
        if user_folders:
            return True
        else:
            return False
    else:
        return False


def check_or_create_user_profile():
    if check_for_existing_user_profile():
        print("User profile found. Loading Profile...")
        user_profile = load_user_profile()
    else:
        print("No user profile found. Creating new user profile...")
        user_profile = create_user_profile()
    return user_profile


def load_user_profile():
    """
    Loads the user profile from storage.
    """
    profiles_found = [folder for folder in os.listdir(profiles_dir) if
                      os.path.isdir(os.path.join(profiles_dir, folder))]

    if not profiles_found:
        print("No user profiles found.")
        return None

    # Display available profiles for the user to choose from
    print("Available user profiles:")
    for i, profile in enumerate(profiles_found, start=1):
        print(f"({i}) {profile}")

    while True:
        profile_index = input("Select a profile to load (Enter a number): ")
        if profile_index.isdigit():
            profile_index = int(profile_index)
            if 1 <= profile_index <= len(profiles_found):
                username = profiles_found[profile_index - 1]
                break
        print("Invalid input. Please enter a valid number.")

    # Load the user's JSON profile data
    user_profile_path = os.path.join(profiles_dir, username, f"{username}.json")

    if not os.path.exists(user_profile_path):
        print(f"Profile data file not found for {username}. Creating a new profile.")
        return UserProfile(username)

    with open(user_profile_path, 'r') as f:
        user_data = json.load(f)

    user_name = user_data["user_name"]
    gender = Gender[user_data["gender"]] if user_data["gender"] in Gender.__members__ else Gender.MALE
    default_profile_name = user_data["default_profile"]
    ai_profiles_data = user_data.get("ai_profiles", {})

    user_profile = UserProfile(user_name, gender)

    # Load AI profiles from storage
    for profile_name, ai_data in ai_profiles_data.items():
        ai_profile_path = os.path.join(profiles_dir, user_name, "ai", profile_name, "profile_data.json")

        if os.path.exists(ai_profile_path):
            with open(ai_profile_path, 'r') as f:
                ai_data = json.load(f)

            try:
                # Handling potential errors if enums are not valid
                relationship_type = RelationshipType[ai_data["relationship_type"]] if ai_data["relationship_type"] in RelationshipType.__members__ else RelationshipType.FRIEND
                mood = Mood[ai_data["mood"]] if ai_data["mood"] in Mood.__members__ else Mood.NEUTRAL

                ai_profile = AiProfile(
                    model_name="T5",  # Set default model
                    name=ai_data["name"],
                    relationship_type=relationship_type,
                    mood=mood,
                    user_profile=user_profile
                )
                user_profile.ai_profiles[profile_name] = ai_profile
            except KeyError as e:
                print(f"(file: main.py, function: load_user_profile) Error loading AI profile {profile_name}: Missing key {e}")
            except ValueError as e:
                print(f"(file: main.py, function: load_user_profile) Error processing AI profile {profile_name}: Invalid enum value {e}")

    # Set the default profile if it exists
    if default_profile_name and default_profile_name in user_profile.ai_profiles:
        user_profile.set_default_profile(default_profile_name)

    return user_profile



def choose_gender():
    gender_input = input("Enter your gender: Male/Female/Nonbinary/Trans: ").title()
    if gender_input[0] == "M":
        gender = Gender.MALE
    elif gender_input[0] == "F":
        gender = Gender.FEMALE
    elif gender_input[0] == "N":
        gender = Gender.NONBINARY
    elif gender_input[0] == "T":
        gender = Gender.TRANS
    else:
        print(f"Unknown input detected {gender_input}, defaulting to Male gender.")
        gender = Gender.MALE
    return  gender


def choose_username():
    username = input("Enter your desired username: ")
    return username


def choose_ai_name():
    name = input("Enter the name for the new AI: ")
    return name

def choose_relationship_type():
    relationship = input(f"Enter the relationship type (Friend, Romantic, Family, Mentor, Rival): ").title()
    if relationship == "Friend":
        return RelationshipType.FRIEND
    elif relationship == "Romantic":
        return RelationshipType.ROMANTIC
    elif relationship == "Family":
        return RelationshipType.FAMILY
    elif relationship == "Mentor":
        return RelationshipType.MENTOR
    elif relationship == "Rival":
        return RelationshipType.RIVAL
    else:
        print(f"Unknown input detected: {relationship}, relationship type set to Friend")
        return RelationshipType.FRIEND


def choose_mood():
    mood = input(f"Enter the starting mood (Happy, Sad, Angry, Calm, Excited, Neutral, Aroused): ").title()
    if mood == "Happy":
        return Mood.HAPPY
    elif mood == "Sad":
        return Mood.SAD
    elif mood == "Angry":
        return Mood.ANGRY
    elif mood == "Calm":
        return Mood.CALM
    elif mood == "Excited":
        return Mood.EXCITED
    elif mood == "Neutral":
        return Mood.NEUTRAL
    elif mood == "Aroused":
        return Mood.AROUSED
    else:
        print(f"Unknown input detected: {mood}, setting mood to Neutral")
        return Mood.NEUTRAL


def create_user_profile():
    """
    Creates a new user profile.
    """
    username = choose_username()
    gender = choose_gender()
    user_profile = UserProfile(username, gender)
    user_profile.save_profile()  # Save the newly created profile
    return user_profile


def select_or_create_ai_profile(user_profile):
    """
    Prompts the user to either select an existing AI profile or create a new one.
    """
    print("Choose an AI profile to chat with:")
    ai_profiles = user_profile.get_ai_profiles()

    if ai_profiles:
        # Show the user all existing AI profiles
        for i, ai in enumerate(ai_profiles.values(), start=1):  # FIX: Use .values()
            print(f"{i}. {ai.name}")  # FIX: Now accessing 'name' correctly

        print(f"{len(ai_profiles) + 1}. Create a new AI profile")

        while True:
            choice = input("Enter the number of the AI profile you want to chat with: ")
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(ai_profiles):
                    ai_profile = list(ai_profiles.values())[choice - 1]
                    break
                elif choice == len(ai_profiles) + 1:
                    ai_profile = create_ai_profile(user_profile)
                    break
            print("Invalid input. Please enter a valid number.")
    else:
        # No AI profiles exist, so we create a new one
        ai_profile = create_ai_profile(user_profile)

    user_profile.set_default_profile(ai_profile.name)  # FIX: Ensure default profile is set
    return ai_profile


def create_ai_profile(user_profile):
    """
    Prompts the user to create a new AI profile.
    """
    print("Creating a new AI profile.")
    name = choose_ai_name()
    gender = choose_gender()
    relationship_type = choose_relationship_type()
    mood = choose_mood()


    # Assuming you have pre-defined enums for RelationshipType and Mood
    ai_profile = AiProfile(
        model_name="T5", name=name, gender=gender, relationship_type=relationship_type, mood=mood, user_profile=user_profile)
    user_profile.add_ai_profile(ai_profile)  # Add the new AI profile to the user profile

    # Start the chat with the new AI profile
    return ai_profile


def run():
    user_profile = check_or_create_user_profile()
    # Load or create an AI profile for the user
    ai_profile = select_or_create_ai_profile(user_profile)
    print(ai_profile.get_profile_summary())
    # Start chatting with the selected AI profile
    ai_profile.chat()
    #ai_profile.save_profile()
    #user_profile.save_profile()

def main():
    print("AI Local launched...")
    run()


if __name__ == '__main__':
    main()