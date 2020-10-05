import torch
import torch.nn.functional as F

class SongClassifierModel3(torch.nn.Module):
    def __init__(self, n_inputs):
        super(SongClassifierModel3, self).__init__()
        self.layer = torch.nn.Linear(n_inputs, n_inputs*2, bias = True)
        self.activation = torch.nn.Sigmoid()
        self.layer2 = torch.nn.Linear(n_inputs*2, 1, bias = True)
        
    
    def forward(self, X):
        X = self.layer(X)
        X = self.activation(X)
        X = self.layer2(X)
        X = self.activation(X)
        return X

    
