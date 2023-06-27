# File: /cherryAI/utils/code_generator.py

from transformers import GPT2LMHeadModel, GPT2Tokenizer

MODEL_NAME = 'gpt2'

# Load pretrained model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)

def generate_code(prompt, max_length=9000, do_sample=True, temperature=0.7):
    """
    Generate code given a prompt using GPT-2.
    """

    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=max_length, do_sample=do_sample, temperature=temperature)

    # decode the output and return it
    output = tokenizer.decode(outputs[0])

    return output
