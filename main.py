# main.py
"""
Entry point for the program. Might refactor a bit later on.
"""
import os
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
    username = input("Enter your username: ")
    # Assuming UserProfile can be loaded by username
    user_profile = UserProfile(username)
    user_profile.load_profile()
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
        for i, ai in enumerate(ai_profiles):
            print(f"{i + 1}. {ai.name}")
        print(f"{len(ai_profiles) + 1}. Create a new AI profile")

        choice = int(input("Enter the number of the AI profile you want to chat with: "))

        if choice == len(ai_profiles) + 1:
            ai_profile = create_ai_profile(user_profile)
        else:
            ai_profile = ai_profiles[choice - 1]
    else:
        # No AI profiles exist, so we create a new one
        ai_profile = create_ai_profile(user_profile)

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
        model="T5", name=name, gender=gender, relationship_type=relationship_type, mood=mood, user_profile=user_profile)
    user_profile.add_ai_profile(ai_profile)  # Add the new AI profile to the user profile

    # Start the chat with the new AI profile
    return ai_profile


def run():
    user_profile = check_or_create_user_profile()
    # Load or create an AI profile for the user
    ai_profile = select_or_create_ai_profile(user_profile)
    # Start chatting with the selected AI profile
    ai_profile.chat()
    #ai_profile.save_profile()
    #user_profile.save_profile()

def main():
    print("AI Local launched...")
    run()


if __name__ == '__main__':
    main()