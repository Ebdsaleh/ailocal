# src/core/t5_model.py
import os.path

from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
import re
from peft import PeftModel, PeftConfig, get_peft_model
from src.core.paths import t5_adapters_dir


class T5Model:
    def __init__(self, model_dir, ai_profile_name="", user_profile_name="", device="cuda" if torch.cuda.is_available() else "cpu"):
        """
        Initialize the T5 model and tokenizer.
        :param model_dir: Path to the directory containing the model files.
        :param device: Device to run the model on (CPU or GPU).
        """
        self.device = device
        self.tokenizer = T5Tokenizer.from_pretrained(model_dir, local_files_only=True, legacy=False)
        self.model = T5ForConditionalGeneration.from_pretrained(model_dir, local_files_only=True)
        self.model.to(self.device)
        self.ai_profile_name = ai_profile_name
        self.user_profile_name = user_profile_name
        self.adapters_path = t5_adapters_dir
        self.active_adapters = []
        self.active_peft_models = {}

    def check_for_cuda(self):
        print(f"Cuda is available?: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"Cuda device to use: {torch.cuda.get_device_name(0)}")
            print(f"Cuda version found: {torch.version.cuda}")  # Should return '11.8'
            print(f"Confirmed device is set to {self.device}")

    def eval(self):
        self.model.eval()

    def train(self):
        self.model.train()

    def load_adapter(self, full_file_name=None, category: str = None):
        """
        Load a specific adapter into the model.
        :param full_file_name: name of the adapter file, the path will already be known to the model.
        :param category: used for storing the peft_model in the self.active_peft_models dict
        """
        if full_file_name is None or full_file_name.isdigit():
            return False
        if category is None or category.isdigit():
            return False

        # Load the adapter using Hugging Face's API
        adapter = PeftModel.from_pretrained(self.model, full_file_name, safe_serialization=True)
        self.model.load_adapter(full_file_name)  # Load the adapter using Hugging Face's API
        self.active_adapters.append(full_file_name)
        self.active_peft_models[category] = adapter

        # Freeze the weights of the original model
        for param in self.model.parameters():
            param.requires_grad = False

        print(f"Loaded adapter: {full_file_name}, category: {category}")
        return True

    def load_adapters(self):
        """
        Load all adapters from the adapter directory and set them to active.
        """
        for adapter_file in os.listdir(self.adapters_path):
            if adapter_file.endswith(".adapter"):
                adapter_path = os.path.join(self.adapters_path, adapter_file)
                self.load_adapter(adapter_path)
        # Activate all loaded adapters
        if self.active_adapters:
            self.model.set_active_adapters(self.active_adapters)

    def generate_response(self, prompt, context="", max_length=600):
        """
        Generate a response based on the input prompt.
        :param prompt: Input text.
        :param context: Input text to provide a better response from the model
        :param max_length: Maximum length of the generated response.
        :return: Generated response as a string.
        """
        if context == "":
            context = "Answer as a helpful AI assistant:"

        # Prepare input text
        input_text = f"### CONTEXT:\n{context}\n\n### USER: {self.user_profile_name} asks: {prompt}\n\n### RESPONSE: Please reply appropriately."

        inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to(self.device)

        # Keep generating until we get a non-empty response
        while True:
            output_ids = self.model.generate(
                inputs.input_ids,
                max_length=max_length,
                num_return_sequences=1,
                #temperature=0.5,
                #top_p=0.35,
                #repetition_penalty=5.0,
                do_sample=False
            )

            response = self.tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
            response = re.sub(rf"^({self.ai_profile_name}|{self.user_profile_name}):\s*", "",
                              response).strip()  # Remove unwanted name prefixes
            response = re.sub(r"\n+", " ", response).strip()  # Remove multiple newlines and excess spaces

            # If the response is not empty, return it
            if response:
                return response
            else:
                print("Generated an invalid response, retrying...")
