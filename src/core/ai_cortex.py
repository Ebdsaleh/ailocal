# src.core.ai_cortex.py

"""
This class is responsible for better message interpretation and
tonal inference along with mood adjustment.
"""
from src.core.contructs import Tone, Mood

class AiCortex:
    def __init__(self, brain=None):
        print("AiCortex is initializing")

    def adjust_mood(self, mood:Mood):
        new_mood = mood
        return new_mood

    def infer_tone(self, text:str):
        tonal_impressions = self.analyze_text(text)
        # Check the list for the most dominant tonal impressions in the text
        return Tone.NEUTRAL

    def analyze_text(self, text:str):
        impressions = []
        for word in text:
            if self.matches_tone_type(word):
                tone = self.get_tone_type(word)
                impressions.append(tone)
        return impressions

    def matches_tone_type(self, text:str):
        match = False
        happy_words = ["nice", "love", "happy", "glad", "warms"]
        for word in happy_words:
            if word in text:
                match = True
                return match
        return match

    def get_tone_type(self, text:str):
        tone_type = Tone.NEUTRAL
        happy_words = ["nice", "love", "happy", "glad", "warms"]
        for word in happy_words:
            if word in text:
                tone_type = Tone.JOVIAL
        return tone_type.name








