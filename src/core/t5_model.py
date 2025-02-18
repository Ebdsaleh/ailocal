# src/core/t5_model.py
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch


class T5Model:
    def __init__(self, model_dir, device="cuda" if torch.cuda.is_available() else "cpu"):
        """
        Initialize the T5 model and tokenizer.
        :param model_dir: Path to the directory containing the model files.
        :param device: Device to run the model on (CPU or GPU).
        """
        self.device = device
        self.tokenizer = T5Tokenizer.from_pretrained(model_dir, local_files_only=True)
        self.model = T5ForConditionalGeneration.from_pretrained(model_dir, local_files_only=True)
        self.model.to(self.device)

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
        input_text = f"{context} {prompt}"
        inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to(self.device)

        output_ids = self.model.generate(
            inputs.input_ids,
            max_length=max_length,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.2,
            do_sample=True
        )

        response = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return response


