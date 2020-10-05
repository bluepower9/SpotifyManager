from data.SongClassifierModel import SongClassifierModel
from data.SongClassifierModel2 import SongClassifierModel2
from data.CSVDataSet import CSVDataSet
from torch.utils.data import DataLoader
from torch.utils.data import random_split
import torch

dataset = CSVDataSet('./data/data.csv')
savepath = './models/weights/weights2'

print(len(dataset))

train, test = random_split(dataset, [round(len(dataset)/2), len(dataset) - round(len(dataset)/2)])
train_dl = DataLoader(train, batch_size = 32, shuffle = True)
test_dl = DataLoader(test, batch_size = 1, shuffle = False)
full_dl = DataLoader(dataset, batch_size = len(dataset), shuffle = True)
input_size = 9


def getmaxitem(items):
    index = 0
    maxitem = items[0]
    for i in range(len(items)):
        if items[i].item() > maxitem.item():
            index = i
            maxitem = items[i]
    return index, maxitem

def run_test(test_dl = test_dl, savepath = savepath, print_values = True, modeltype = SongClassifierModel, input_size = input_size):
    model = modeltype(9)
    #print('loading weights...')
    model.load_state_dict(torch.load(savepath))
    #print('successfully loaded weights')
    criterion = torch.nn.MSELoss()


    total_loss = 0
    for  i,(inputs, targets) in enumerate(test_dl):
        yhat = model(inputs.float())
        target = targets
        #print(i, yhat)
        test = 'Correct'
        maxyhat = getmaxitem(yhat[0])
        maxtarget = getmaxitem(targets[0])
        #checks if index of the maximum values are the same indicating a correct match.
        if maxyhat[0] != maxtarget[0]:
            total_loss += 1
            test = 'Incorrect'
        if print_values:
            print(test, ' predicted: ', round(yhat.item(), 3), ' actual: ', target.item())
        #print(loss.item())
    
    return total_loss/len(test_dl)


if __name__ == '__main__':
    print('loss: ', run_test())

