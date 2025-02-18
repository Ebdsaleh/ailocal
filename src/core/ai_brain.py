# src/core/ai_brain.py
"""
This class is responsible for giving more of a personality to the AiProfile
"""

from src.core.ai_cortex import AiCortex


class AiBrain:
    def __init__(self):
        print("AiBrain is initializing...")
        self.cortex = AiCortex()
