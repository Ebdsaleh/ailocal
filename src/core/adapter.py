# src/core/adapter.py
"""
This class is responsible for creating adapters
"""
import os
import json
import time
from src.core.paths import t5_adapters_dir, training_data_dir
from transformers import EncoderDecoderCache
from src.core.text_dataset import TextDataset, DataLoader
import torch
import torch.nn as nn
from torch.optim import AdamW
from transformers import T5ForConditionalGeneration, T5Tokenizer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

default_lora_config = LoraConfig(
    r=8,  # Rank of the low-rank matrices
    target_modules=['q', 'v'],  # Correct module names
    lora_alpha=16,  # Scaling factor for LoRA weights
    lora_dropout=0.1,  # Dropout for LoRA layers
    bias='none',  # Whether to add bias to LoRA layers
    task_type="SEQ_2_SEQ_LM",  # Task type (sequence-to-sequence language modeling)
)

class Adapter:
    global default_lora_config
    def __init__(self, name=None, lora_config=None):
        self.lora_config = None
        if lora_config is None:
            self.lora_config = default_lora_config
        else:
            self.lora_config = lora_config
        if name is None:
            self.name = "New Adapter"
        else:
            self.name = name
        self.adapter_dir = t5_adapters_dir
        self.full_file_name = None
        self.set_full_file_name()


    def create_adapter(self, model):
        model.model = prepare_model_for_kbit_training(model.model)
        return get_peft_model(model.model, self.lora_config)

    def set_name(self, name:str):
        if name is None or name.isdigit():
            return False
        else:
            self.name = name
            self.set_full_file_name()
            return True

    def set_full_file_name(self):
        filename = f"{self.name}.safetensors"
        full_file_name = os.path.join(t5_adapters_dir, filename)
        self.full_file_name = full_file_name

    def save_adapter(self, adapter):
        # Ensure the file name ends with .safetensors
        if not self.full_file_name.endswith(".safetensors"):
            self.full_file_name = os.path.splitext(self.full_file_name)[0] + ".safetensors"

        print(f"Request to save adapter at: {self.full_file_name}")
        adapter.save_pretrained(self.full_file_name, safe_serialization=True)  # Save in .safetensors format

    def prepare_data(self, model, filename: str):
        file_path = os.path.join(training_data_dir, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{filename}' not found in '{training_data_dir}'")

        with open(file_path, 'r', encoding="utf-8") as f:
            data = json.load(f)

        # Create dataset
        dataset = TextDataset(data, model.tokenizer)
        return dataset

    def train_adapter(self, model, training_data, epochs=3):
        # Clear GPU Cache
        torch.cuda.empty_cache()

        # Enable gradient checkpointing
        model.model.gradient_checkpointing_enable()

        # Create DataLoader
        dataloader = DataLoader(
            training_data,
            batch_size=2,  # Reduced batch size
            shuffle=True,
            num_workers=8,
            pin_memory=True,
        )

        # Create adapter
        adapter = self.create_adapter(model)
        device = model.device
        model.model.to(device)
        adapter.to(device)

        # Debugging: Check model parameters
        for name, param in adapter.named_parameters():
            if torch.isnan(param).any() or torch.isinf(param).any():
                print(f"Parameter {name} contains nan or inf values!")

        # Set up optimizer and loss function
        optimizer = AdamW([p for p in adapter.parameters() if p.requires_grad], lr=1e-5)  # Reduced learning rate
        loss_fn = nn.CrossEntropyLoss(ignore_index=-100)

        # Gradient accumulation steps
        gradient_accumulation_steps = 4

        for epoch in range(epochs):
            model.train()
            adapter.train()
            total_loss = 0
            epoch_start_time = time.time()

            for batch_idx, batch in enumerate(dataloader):
                batch_start_time = time.time()

                # Move batch to GPU
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                labels = batch["labels"].to(device)
                decoder_input_ids = batch["decoder_input_ids"].to(device)

                # Forward pass
                outputs = adapter(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels,
                    decoder_input_ids=decoder_input_ids,
                )
                logits = outputs.logits
                logits = logits.view(-1, logits.size(-1))
                labels = labels.view(-1)

                # Debugging: Check model outputs
                if torch.isnan(logits).any() or torch.isinf(logits).any():
                    print("Model outputs (logits) contain nan or inf values!")
                if torch.isnan(labels).any() or torch.isinf(labels).any():
                    print("Labels contain nan or inf values!")

                loss = loss_fn(logits, labels)
                loss = loss / gradient_accumulation_steps  # Normalize loss

                # Backward pass
                loss.backward()

                # Accumulate gradients
                if (batch_idx + 1) % gradient_accumulation_steps == 0:
                    optimizer.step()
                    optimizer.zero_grad()

                total_loss += loss.item()

                # Calculate time taken for the batch
                batch_time = time.time() - batch_start_time

                # Print loss and time for each batch
                print(
                    f"Epoch {epoch + 1}, Batch {batch_idx + 1}, Loss: {loss.item() * gradient_accumulation_steps}, Time: {batch_time:.2f} seconds")

            # Calculate time taken for the epoch
            epoch_time = time.time() - epoch_start_time

            # Print average loss and time for the epoch
            print(f"Epoch {epoch + 1}, Average Loss: {total_loss / len(dataloader)}, Time: {epoch_time:.2f} seconds")

        self.save_adapter(adapter)