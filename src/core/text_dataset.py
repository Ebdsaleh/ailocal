# src/core/text_dataset.py

"""
    This class is responsible for creating a
    TextDataset from a JSON file, to be used in training an Adapter.
"""
import torch
from torch.utils.data import Dataset, DataLoader

class TextDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=512):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]

        # Tokenize user input
        encoding = self.tokenizer(
            item['user_input'],
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )

        # Tokenize AI response (for labels and decoder input)
        label_encoding = self.tokenizer(
            item['ai_response'],
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        # Prepare inputs and labels
        input_ids = encoding['input_ids'].squeeze(0)  # Remove batch dimension
        attention_mask = encoding['attention_mask'].squeeze(0)
        labels = label_encoding['input_ids'].squeeze(0)
        decoder_input_ids = label_encoding['input_ids'][:, :-1].squeeze(0)  # Shift labels left

        # Pad decoder_input_ids to match sequence length
        pad_token_id = self.tokenizer.pad_token_id
        decoder_input_ids = torch.nn.functional.pad(
            decoder_input_ids,
            (0, 1),  # Pad the last dimension (sequence length) by 1
            value=pad_token_id
        )

        # Flatten labels for CrossEntropyLoss
        labels = labels.view(-1)  # Shape: (sequence_length,)

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels,
            "decoder_input_ids": decoder_input_ids,
        }
