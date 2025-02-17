# main.py
"""
Entry point for the program.
"""
import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from src.core.paths import gpt2_dir  # Import gpt2_dir path


def download_gpt2_if_needed():
    """
    Checks if the GPT-2 model is already stored locally.
    If not, downloads and saves it to gpt2_dir.
    """
    if not os.path.exists(gpt2_dir) or not os.listdir(gpt2_dir):
        print("GPT-2 model not found. Downloading...")
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        model = GPT2LMHeadModel.from_pretrained("gpt2")

        # Save model and tokenizer to gpt2_dir
        tokenizer.save_pretrained(gpt2_dir)
        model.save_pretrained(gpt2_dir)
        print("GPT-2 model downloaded and saved.")
    else:
        print("GPT-2 model already exists. Loading from disk.")


# Ensure the model is available
download_gpt2_if_needed()
# Load the tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

def generate_response(prompt, model, tokenizer, max_length=100):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs,
        max_length=max_length,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        top_p=0.95,
        top_k=50,
        temperature=0.7,
        do_sample=True
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response


def main():
    print("AI Local launched...")

    # Chat loop
    print("Chatbot: Hello! How can I assist you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye!")
            break
        response = generate_response(user_input, model, tokenizer)
        print(f"Chatbot: {response}")

if __name__ == '__main__':
    main()
