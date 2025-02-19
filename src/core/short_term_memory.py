# src/core/short_term_memory.py

from src.core.memory import Memory


class ShortTermMemory(Memory):
    def __init__(self, max_history=50):
        super().__init__()
        self.max_history = max_history

    def add_message(self, sender, message, timestamp=None):
        super().add_message(sender, message, timestamp)
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)

