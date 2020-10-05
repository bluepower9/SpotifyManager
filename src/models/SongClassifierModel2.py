import torch
import torch.nn.functional as F

class SongClassifierModel2(torch.nn.Module):
    def __init__(self, n_inputs):
        super(SongClassifierModel2, self).__init__()
        self.layer = torch.nn.Linear(n_inputs, n_inputs*3)
        self.activation = torch.nn.Sigmoid()
        self.layer2 = torch.nn.Linear(n_inputs*3, n_inputs*2)
        self.layer3 = torch.nn.Linear(n_inputs*2, 1)
        
    
    def forward(self, X):
        X = self.layer(X)
        X = self.activation(X)
        X = self.layer2(X)
        X = self.activation(X)
        X = self.layer3(X)
        X = self.activation(X)
        return X

    
