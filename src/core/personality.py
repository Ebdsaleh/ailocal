# src/core/personality.py
"""
This class is responsible for holding the collection of personality traits of the AiProfile
"""
from src.core.contructs import TraitType, InterestType


class Personality:
    def __init__(self, max_traits=5, max_interests=8):
        self.traits = []
        self.interests = []
        self.max_traits = max_traits
        self.max_interests = max_interests


    def add_trait(self, trait:TraitType):
        if len(self.traits) < self.max_traits:
            self.traits.append(trait)

    def get_traits(self):
        return self.traits

    def add_interest(self, interest:InterestType):
        if len(self.interests) < self.max_interests:
            self.interests.append(interest)

