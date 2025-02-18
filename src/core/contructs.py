# src/core/constructs.py
"""
This file holds the Identity constructs of user's and AI personality profiles.
"""
from enum import Enum

# Enum for Relationship Types
class RelationshipType(Enum):
    FRIEND = "Friend"
    ROMANTIC = "Romantic"
    FAMILY = "Family"
    MENTOR = "Mentor"
    RIVAL = "Rival"

# Enum for Moods
class Mood(Enum):
    HAPPY = "Happy"
    SAD = "Sad"
    ANGRY = "Angry"
    CALM = "Calm"
    EXCITED = "Excited"
    NEUTRAL = "Neutral"
    AROUSED = "Aroused"

class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    NONBINARY = "NonBinary"
    TRANS = "Trans"

class Tone(Enum):
    NEUTRAL = "Neutral"
    AGGRESSIVE = "Aggressive"
    SOMBER = "Somber"
    SEDUCTIVE = "Seductive"
    JOVIAL = "Jovial"
    COMPASSIONATE = "Compassionate"
    EMPATHETIC = "Empathetic"
    SARCASTIC = "Sarcastic"
    SYMPATHETIC = "Sympathetic"
    SERIOUS = "Serious"
    DISTRESSING = "Distressing"
    CURIOUS = "Curious"
    HOPEFUL = "Hopeful"
    SKEPTICAL = "Skeptical"
    APOLOGETIC = "Apologetic"
    CONFUSED = "Confused"
    CYNICAL = "Cynical"
    INQUISITIVE = "Inquisitive"
    REFLECTIVE = "Reflective"

