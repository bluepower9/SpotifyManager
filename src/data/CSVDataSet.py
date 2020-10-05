from torch.utils.data import Dataset
import pandas as pd

class CSVDataSet(Dataset):
    def __init__(self, path):
        data = pd.read_csv(path)
        self.x = [x[:-4] for x in data.values[1:]]
        self.y = [x[-4:] for x in data.values[1:]]
        #self.y = self.y.values.reshape((len(self.y), 1))

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return [self.x[idx], self.y[idx]]