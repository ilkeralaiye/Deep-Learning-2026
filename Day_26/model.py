from torch import nn


class IrisClassifier(nn.Module):

    def __init__(self):
        super().__init__()

        self.linearLayers = nn.Sequential(
            nn.Linear(in_features=4, out_features=10),
            nn.ReLU(),
            nn.Linear(in_features=10, out_features=10),
            nn.ReLU(),
            nn.Linear(in_features=10, out_features=3)
        )

    def forward(self, x):
        return self.linearLayers(x)
