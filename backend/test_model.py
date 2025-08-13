import torch
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from backend.model import DotLLM, DotLLMConfig


def load_latest_model():
    checkpoint_dir = os.path.join(os.path.dirname(__file__), '..')
    if not os.path.exists(checkpoint_dir):
        print("No checkpoints directory found. Please train the model first.")
        return None, None, None, None

    checkpoint_files = [f for f in os.listdir(checkpoint_dir) if f.endswith('.pt')]
    if not checkpoint_files:
        print("No checkpoint files found. Please train the model first.")
        return None, None, None, None

    latest_checkpoint = max(checkpoint_files, key=lambda x: int(x.split('_')[-1].split('.')[0]) if 'step' in x else 0)
    checkpoint_path = os.path.join(checkpoint_dir, latest_checkpoint)
    
    print(f"Loading checkpoint: {checkpoint_path}")
    checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))
    
    config = DotLLMConfig(**checkpoint['config'])
    mdl = DotLLM(config)
    mdl.load_state_dict(checkpoint['model_state_dict'])
    mdl.eval()

    stoi = checkpoint['stoi']
    itos = checkpoint['itos']
    chars = [itos[i] for i in sorted(itos.keys())]

    print(f"Loaded model with vocabulary size: {len(chars)}")

    return mdl, chars, stoi, itos

# Load the latest model and character mappings
model, chars, stoi, itos = load_latest_model()

if model is None:
    print("Exiting due to missing model.")
    exit()

print(f"Vocabulary size: {len(chars)}")

def generate_dots(model, input_text):
    model.eval()
    input_ids = torch.tensor([stoi.get(c, 0) for c in input_text], dtype=torch.long).unsqueeze(0)
    with torch.no_grad():
        output_ids = model.generate(input_ids)
    
    output_text = ''.join(['.' if id.item() == 1 else ' ' for id in output_ids[0]])
    
    print(f"Input:        {input_text}")
    print(f"Model output: {output_text}")
    
    return output_text

# Example usage
input_text = "Hello, World!"
output = generate_dots(model, input_text)

# Interactive mode
print("\nEnter text to convert to dots (or 'quit' to exit):")
while True:
    user_input = input("> ")
    if user_input.lower() == 'quit':
        break
    output = generate_dots(model, user_input)

print("Thank you for using DotLLM!")
