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


class TraitType(Enum):
    OPEN_MINDED = "Open Minded"
    HIGH_SEX_DRIVE = "High Sex Drive"
    SEXUALLY_OPEN = "Sexually Open"
    PLAYFUL = "Playful"
    INTELLECTUAL = "Intellectual"
    ROMANTIC = "Romantic"
    OUTGOING = "Outgoing"
    OPTIMISTIC = "Optimistic"
    PESSIMISTIC = "Pessimistic"
    FLIRTY = "Flirty"
    OPINIONATED = "Opinionated"
    FUNNY = "Funny"
    CURIOUS = "Curious"
    ADVENTUROUS = "Adventurous"
    INTROVERTED = "Introverted"
    CYNICAL = "Cynical"
    CREATIVE = "Creative"


class InterestType(Enum):
    D_AND_D = "D&D"
    ROLEPLAY = "Roleplay"
    HISTORY = "History"
    MYTHOLOGY = "Mythology"
    SCIENCE = "Science"
    SCI_FI = "Sci Fi"
    SEXUAL_SUBMISSIVE = "Sexual - Submissive"
    SEXUAL_DOMINANT = "Sexual - Dominant"
    INDOORS = "Indoors"
    OUTDOORS = "Outdoors"
    CODING = "Coding"
    WRITING = "Writing"
    READING = "Reading"
    PHILOSOPHY = "Philosophy"
    SPIRITUAL = "Spiritual"
    BUSINESS = "Business"
    FITNESS = "Fitness"
    PSYCHOLOGY = "Psychology"
    MENTAL_HEALTH = "Mental Health"
    FOOD = "Food"
    DANCING = "Dancing"
    PLAYING_MUSIC = "Playing Music"
    TRAVELLING = "Travelling"
    ASTRONOMY = "Astronomy"
    ASTROLOGY = "Astrology"
    MEDITATION = "Meditation"



