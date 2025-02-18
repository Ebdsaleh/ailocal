# src/core/ai_brain.py
"""
This class is responsible for giving more of a personality to the AiProfile
"""

from src.core.ai_profile import AiProfile
from src.core.ai_cortex import AiCortex


class AiBrain:
    def __init__(self, ai_profile=None):
        print("AiBrain is initializing...")
        self.ai_profile = ai_profile
        self.cortex = AiCortex(self)

    def get_cortex(self):
        return self.cortex