import torch
import torch.nn as nn
import torch.optim as optim
from backend.model import DotLLM, DotLLMConfig

# Load your data
with open('dot_dataset.txt', 'r', encoding='utf-8') as f:
    data = f.read().split('\n')

# Create character mappings
chars = sorted(set(''.join(data)))
stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}

# Convert data to ids
X = []
Y = []
for i in range(0, len(data), 2):
    if i+1 < len(data):
        x = [stoi[c] for c in data[i]]
        y = [0 if c == ' ' else 1 for c in data[i+1]]
        if len(x) == len(y):
            X.append(torch.tensor(x, dtype=torch.long))
            Y.append(torch.tensor(y, dtype=torch.long))

# Model parameters
vocab_size = len(chars)
hidden_size = 64
config = DotLLMConfig(vocab_size, hidden_size)
model = DotLLM(config)

# Training parameters
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters())
num_epochs = 100
batch_size = 32

# Training loop
for epoch in range(num_epochs):
    total_loss = 0
    for i in range(0, len(X), batch_size):
        batch_X = X[i:i+batch_size]
        batch_Y = Y[i:i+batch_size]
        
        # Pad sequences in the batch to the same length
        max_len = max(len(x) for x in batch_X)
        batch_X = torch.nn.utils.rnn.pad_sequence(batch_X, batch_first=True, padding_value=0)
        batch_Y = torch.nn.utils.rnn.pad_sequence(batch_Y, batch_first=True, padding_value=0)
        
        optimizer.zero_grad()
        output = model(batch_X)
        loss = criterion(output.view(-1, 2), batch_Y.view(-1))
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {total_loss:.4f}")

# Save the trained model
torch.save({
    'model_state_dict': model.state_dict(),
    'config': config.__dict__,
    'stoi': stoi,
    'itos': itos
}, 'dotllm_model_final.pt')

print("Training completed and model saved.")
