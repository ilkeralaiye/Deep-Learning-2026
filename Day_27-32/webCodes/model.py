import torch
import torch.nn as nn


# Must match exactly the architecture used during training
class CropProposer(nn.Module):

    def __init__(self):
        super().__init__()

        self.linearLayers = nn.Sequential(
            nn.Linear(in_features=7, out_features=16),
            nn.ReLU(),
            nn.Linear(in_features=16, out_features=16),
            nn.ReLU(),
            nn.Linear(in_features=16, out_features=22)
        )

    def forward(self, x):
        return self.linearLayers(x)


# Ordered list of crop labels — index must match training label encoding.
# sklearn's LabelEncoder sorts labels alphabetically, so index 0 = Apple, etc.
CROP_LABELS = [
    "Apple",       # 0
    "Banana",      # 1
    "Blackgram",   # 2
    "ChickPea",    # 3
    "Coconut",     # 4
    "Coffee",      # 5
    "Cotton",      # 6
    "Grapes",      # 7
    "Jute",        # 8
    "KidneyBeans", # 9
    "Lentil",      # 10
    "Maize",       # 11
    "Mango",       # 12
    "MothBeans",   # 13
    "MungBean",    # 14
    "Muskmelon",   # 15
    "Orange",      # 16
    "Papaya",      # 17
    "PigeonPeas",  # 18
    "Pomegranate", # 19
    "Rice",        # 20
    "Watermelon",  # 21
]


def load_model(path: str = "crop_model.pth") -> CropProposer:
    model = CropProposer()
    model.load_state_dict(torch.load(path, map_location=torch.device("cpu")))
    model.eval()
    return model
