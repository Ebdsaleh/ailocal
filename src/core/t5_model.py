# src/core/t5_model.py
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
import re


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
