'''
  File name: p3_train.py
  Author:
  Date:
'''

import PyNet as net
from p3_utils import *
from p3_dataloader import *


'''
  network architecture construction
  - Stack layers in order based on the architecture of your network
'''

layer_list = [
                net.Conv2d(.........),
                net.BatchNorm2D(.....),
                net.Relu()
                ......
             ]

'''
  Define loss function
'''
loss_layer = net.Loss_Function_name(......)

'''
  Define optimizer 
'''
optimizer = net.optimizer_name(.......)


'''
  Build model
'''
my_model = net.Model(layer_list, loss_layer, optimizer)

'''
  Define the number of input channel and initialize the model
'''
my_model.set_input_channel(...)


'''
  Input possible pre-trained model
'''
my_model.load_model('preMolde.pickle')


'''
  Main training process
  - train N epochs, each epoch contains M steps, each step feed a batch-sized data for training,
    that is, total number of data = M * batch_size, each epoch need to traverse all data.
'''

# obtain data 
[data_set, label_set] = dataloader(.....)

'''
  pre-process data
  1. normalization
  2. convert ground truth data 
  3. resize data into the same size
'''

for i in range (max_epoch_num):
  '''
    random shuffle data 
  '''
  data_set_cur, label_set_cur = randomShuffle(data_set, label_set) # design function by yourself


  step = ...  # step is a int number
  for j in range (step):
    # obtain a mini batch for this step training
    [data_bt, label_bt] = obtainMiniBatch(....)  # design function by yourself

    # feedward data and label to the model
    loss, pred = my_model(data_bt, label_bt)

    # backward loss
    my_model.backward(.....)

    # update parameters in model
    my_model.update_param()


  '''
    save trained model, the model should be saved as a pickle file
  '''
  if i % save_interval == 0:
    my_model.save_model(str(i) + '.pickle')
