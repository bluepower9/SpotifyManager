from data.SongClassifierModel import SongClassifierModel
from data.SongClassifierModel2 import SongClassifierModel2
from data.SongClassifierModel3 import SongClassifierModel3
from data.SongMultiClassifierModel import SongMultiClassifierModel
from data.CSVDataSet import CSVDataSet
from torch.utils.data import DataLoader
from torch.utils.data import random_split
import torch
from test import run_test, getmaxitem


dataset = CSVDataSet('./data/data.csv')
savepath = './models/weights/weights5'
MODELTYPE = SongMultiClassifierModel
input_size = 9
dim = 0

train, test = random_split(dataset, [round(len(dataset)*3/4), round(len(dataset)/4)])
train_dl = DataLoader(train, batch_size = len(train), shuffle = True)
test_dl = DataLoader(test, batch_size = 1, shuffle = False)
full_dl = DataLoader(dataset, batch_size = len(dataset), shuffle = True)


use = train_dl

#model to use

model = MODELTYPE(input_size, dim = dim)

'''
print('loading weights...')
model.load_state_dict(torch.load(savepath))
print('successfully loaded weights')
'''

criterion = torch.nn.MSELoss()
optimizer = torch.optim.AdamW(model.parameters(), lr = 0.01)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size = 1000, gamma = 0.1)


for epoch in range(1000000):
    total_loss = 0
    true_loss= 0
    for  i,(inputs, targets) in enumerate(use):
        optimizer.zero_grad()
        yhat = model(inputs.float())
        loss = criterion(yhat, targets.float())

        #calculate how many model got correct.
        for i in range(len(yhat)):
            maxyhat = getmaxitem(yhat[i])
            maxtarget = getmaxitem(targets[i])
            #checks if index of the maximum values are the same indicating a correct match.
            #print(maxyhat, maxtarget)
            if maxyhat[0] != maxtarget[0]:
                true_loss+=1

        total_loss += loss.item()
        loss.backward()
        optimizer.step()

    if epoch%100 == 0 or epoch == 0:
        print('saving model...')
        torch.save(model.state_dict(), savepath)

    test = run_test(test_dl = test_dl, savepath = savepath, print_values=False, modeltype=MODELTYPE, input_size=input_size)
    print('epoch: ', epoch, 'batch loss: ', total_loss*100, ' training data loss: ',true_loss*100/len(use.dataset), ' test data loss: ', test*100)
    #scheduler.step()
    
