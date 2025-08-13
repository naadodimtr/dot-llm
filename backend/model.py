import torch
import torch.nn as nn

class DotLLMConfig:
    def __init__(self, vocab_size, hidden_size=64):
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size

class DotLLM(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.embedding = nn.Embedding(config.vocab_size, config.hidden_size)
        self.fc = nn.Linear(config.hidden_size, 2)  # 2 outputs: space (0) or dot (1)

    def forward(self, x):
        embed = self.embedding(x)
        return self.fc(embed)

    def generate(self, idx):
        logits = self(idx)
        return torch.argmax(logits, dim=-1)
