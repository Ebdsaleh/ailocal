# src/core/gpt2_model.py
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch


class GPT2Model:
    def __init__(self, model_dir, device="cuda" if torch.cuda.is_available() else "cpu"):
        self.device = device
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_dir, local_files_only=True)
        self.model = GPT2LMHeadModel.from_pretrained(model_dir, local_files_only=True)
        self.model.to(self.device)

        # Add padding token if not already set
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token  # Set padding token to eos_token
            self.model.resize_token_embeddings(len(self.tokenizer))  # Resize model embeddings to accommodate the padding token

    def generate_response(self, user_input, max_length=100):
        # Refined instructional prompt
        prompt = f"You are an AI assistant. If someone asks you for your name, provide your name or say 'I don't have a name.' Answer the question directly: {user_input}"

        # Tokenize the input and create attention_mask
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)

        # Explicitly handle attention mask
        input_ids = inputs['input_ids'].to(self.device)
        attention_mask = inputs.get('attention_mask', None).to(self.device) if 'attention_mask' in inputs else None

        # Generate response with adjusted parameters
        output_ids = self.model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=max_length,
            temperature=0.6,  # Lower randomness
            top_p=0.85,  # More coherent output
            top_k=50,  # Limit sampling to top 50 tokens
            repetition_penalty=1.2,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id  # Ensure padding token is treated correctly
        )

        response = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return response
