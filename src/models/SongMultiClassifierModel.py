import torch
import torch.nn.functional as F

class SongMultiClassifierModel(torch.nn.Module):
    def __init__(self, n_inputs, dim=0):
        super(SongMultiClassifierModel, self).__init__()
        self.layer = torch.nn.Linear(n_inputs, n_inputs*2, bias = True)
        self.layer2 = torch.nn.Linear(n_inputs*2, n_inputs*3, bias = True)
        self.layer3 = torch.nn.Linear(n_inputs*3, n_inputs*2, bias = True)
        self.layer4 = torch.nn.Linear(n_inputs*2, n_inputs, bias = True)
        self.layer5 = torch.nn.Linear(n_inputs*2, 4)

        self.activation = torch.nn.Sigmoid()
        self.softmax = torch.nn.Softmax(dim=dim)
        
        
    
    def forward(self, X):
        X = self.layer(X)
        X = self.activation(X)
        X = self.layer2(X)
        X = self.activation(X)
        X = self.layer3(X)
        X = self.activation(X)
        x = self.layer4(X)
        X = self.activation(X)
        X = self.layer5(X)
        X = self.activation(X)
        X = self.softmax(X)
        return X

    
