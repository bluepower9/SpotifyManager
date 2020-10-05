import torch
import torch.nn.functional as F

class SongClassifierModel(torch.nn.Module):
    def __init__(self, n_inputs):
        super(SongClassifierModel, self).__init__()
        #weight2
        self.conv1 = torch.nn.Conv1d(1, 32, 2, 1)
        self.conv2 = torch.nn.Conv1d(32, 64 , 2, 1)
        #weight3
        #self.conv1 = torch.nn.Conv1d(1, 12, 2, 1)
        #self.conv2 = torch.nn.Conv1d(12, 24 , 2, 1)
        self.layer = torch.nn.Linear(192, n_inputs)
        self.activation = torch.nn.Sigmoid()
        self.layer2 = torch.nn.Linear(n_inputs, 1)
    
    def forward(self, X):
        X = X.unsqueeze(1)
        X = self.conv1(X)
        X = F.relu(X)
        X = self.conv2(X)
        X = F.relu(X)

        X = F.max_pool1d(X, 2)
        X = torch.flatten(X, 1)
        X = self.layer(X)
        X = F.relu(X)
        X = self.layer2(X)
        X = F.relu(X)
        return X

    
