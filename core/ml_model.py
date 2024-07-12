import torch
import torch.nn as nn
import torch.nn.functional as F
import wandb
import os


class ImageParamModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(1, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 24)
        self.optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
        self.current_outputs = None

        # Initialize weights to break symmetry
        self.apply(self._init_weights)

        # Initialize wandb
        wandb.init(project="lambda-visualizer")

        # Load model if exists
        if os.path.exists('model_weights.pth'):
            self.load_state_dict(torch.load('model_weights.pth'))
            print("Loaded existing model weights.")

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            torch.nn.init.xavier_uniform_(module.weight)
            if module.bias is not None:
                module.bias.data.fill_(0.01)

    def forward(self, x):
        x = torch.sin(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))
        return x

    def infer(self, seed):
        with torch.no_grad():
            seed_tensor = torch.tensor([[seed]], dtype=torch.float32)
            return self.forward(seed_tensor).numpy()

    def generate_params(self, base_seed, num_params=4):
        seeds = [base_seed + i * 1000 for i in range(num_params)]
        seed_tensor = torch.tensor([[s] for s in seeds], dtype=torch.float32)
        self.current_outputs = self.forward(seed_tensor)
        return self.current_outputs.detach().numpy()

    def update_model(self, selected_index):
        if self.current_outputs is None:
            raise ValueError("No current outputs to train on.")

        selected_outputs = self.current_outputs[selected_index::2]
        other_outputs = self.current_outputs[1 - selected_index::2]

        # Calculate contrastive loss
        margin = 1.0
        distance = F.pairwise_distance(selected_outputs[0].unsqueeze(0), selected_outputs[1].unsqueeze(0))
        other_distance = F.pairwise_distance(other_outputs[0].unsqueeze(0), other_outputs[1].unsqueeze(0))

        loss = distance.pow(2) + torch.clamp(margin - other_distance, min=0).pow(2)

        # Backpropagate and update model
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Log to wandb
        wandb.log({
            "train/loss": loss.item(),
            "image/avg_z": self.current_outputs[:, 11:19].mean().item(),
            "image/avg_quadrant": self.current_outputs[:, 19:21].mean().item(),
            "image/avg_flip": self.current_outputs[:, 21].mean().item(),
            "image/avg_rotation": self.current_outputs[:, 22:23].mean().item(),
        })

        # Log individual binary bits
        for i in range(11):
            wandb.log({f"lambda/binary_bit_{i}": self.current_outputs[:, i].mean().item()})

        # Save model
        torch.save(self.state_dict(), 'model_weights.pth')

        # Clear current outputs
        self.current_outputs = None
