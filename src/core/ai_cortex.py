# src.core.ai_cortex.py

"""
This class is responsible for better message interpretation and
tonal inference along with mood adjustment.
"""
from src.core.contructs import Tone, Mood

class AiCortex:
    def __init__(self, brain=None):
        print("AiCortex is initializing")
        self.brain = brain
        self.jovial_words = {"nice", "love", "happy", "glad", "warms"}
        self.somber_words = {"sad", "upset", "down", "cry", "heartbroken"}
        self.aggressive_words = {"angry", "mad", "furious", "rage", "irritated"}

    def adjust_mood(self, mood: Mood) -> Mood:
        # Placeholder for mood adjustments based on conversation
        return mood

    def infer_tone(self, text: str) -> Tone:
        for word in text.split():
            if word in self.jovial_words:
                return Tone.JOVIAL
            elif word in self.somber_words:
                return Tone.SOMBER
            elif word in self.aggressive_words:
                return Tone.AGGRESSIVE
        return Tone.NEUTRAL

