# src/core/memory.py

import json
from datetime import datetime

class Memory:
    def __init__(self):
        self.conversation_history = []

    def add_message(self, sender, message, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        self.conversation_history.append(
            {"timestamp": timestamp, "sender": sender, "message": message}
        )

    def get_conversation_history(self, limit=None):
        return self.conversation_history[-limit:] if limit else self.conversation_history

    def clear_memory(self):
        self.conversation_history = []
