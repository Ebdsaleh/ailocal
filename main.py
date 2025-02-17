# main.py
"""
Entry point for the program.
"""
import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer, AutoModelForCausalLM, AutoTokenizer
from transformers import LlamaTokenizer
from src.core.paths import gpt2_dir, open_llama_dir, falcon_dir  # Import the new model paths


def download_model_if_needed(model_name, model_dir):
    """
    Checks if the GPT-2 model is already stored locally.
    If not, downloads and saves it to gpt2_dir.
    """
    if not os.path.exists(model_dir) or not os.listdir(model_dir):
        print("GPT-2 model not found. Downloading...")
        tokenizer = AutoModelForCausalLM.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

        # Save model and tokenizer to gpt2_dir
        tokenizer.save_pretrained(model_dir)
        model.save_pretrained(model_dir)
        print("GPT-2 model downloaded and saved.")
    else:
        print("GPT-2 model already exists. Loading from disk.")


# Ensure the model is available
download_model_if_needed("gpt2", gpt2_dir)
download_model_if_needed("openlm-research/open_llama_7b", open_llama_dir)
download_model_if_needed("falcon", falcon_dir)
# Load the tokenizer and model
gpt2_tokenizer = GPT2Tokenizer.from_pretrained(gpt2_dir)
gpt2_model = GPT2LMHeadModel.from_pretrained(gpt2_dir)
openllama_tokenizer = AutoTokenizer.from_pretrained(open_llama_dir)
openllama_model = AutoModelForCausalLM.from_pretrained(open_llama_dir)
falcon_tokenizer = AutoTokenizer.from_pretrained(falcon_dir)
falcon_model = AutoModelForCausalLM.from_pretrained(falcon_dir)

gpt2_model.eval()
openllama_model.eval()
falcon_model.eval()


# Add a padding token if it doesn't exist
def add_padding_token_if_needed(tokenizer, model):
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        model.resize_token_embeddings(len(tokenizer), mean_resizing=False)


def generate_response(prompt, model, tokenizer, max_length=100):
    # Tokenize the input and create attention_mask
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']

    # Generate response with attention_mask
    outputs = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=max_length,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        top_p=0.95,
        top_k=50,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id  # Explicitly set pad_token_id to eos_token_id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response


def main():
    print("AI Local launched...")

    # Let the user select the model
    print("Select model: [1] GPT-2 [2] OpenLLaMA [3] Falcon")
    model_choice = input("Choose your model (1/2/3): ")

    # Set the model and tokenizer based on user choice
    if model_choice == "1":
        model, tokenizer = gpt2_model, gpt2_tokenizer
    elif model_choice == "2":
        model, tokenizer = openllama_model, openllama_tokenizer
    elif model_choice == "3":
        model, tokenizer = falcon_model, falcon_tokenizer
    else:
        print("Invalid choice. Defaulting to GPT-2.")
        model, tokenizer = gpt2_model, gpt2_tokenizer

    print(f"Using {model_choice} model...")

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