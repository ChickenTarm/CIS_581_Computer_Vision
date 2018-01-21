'''
  File name: p2_train.py
  Author: Shraddha Jain
  Date: 12/11/2017
'''

import PyNet as net
import numpy as np
np.set_printoptions(threshold=np.nan)
from sklearn.metrics import accuracy_score
from p2_utils import *
import matplotlib.pyplot as plt



def train(my_model, data_set, label_set):

    losses = []
    accuracies = []

    for i in range (50000):

      data_set_cur, label_set_cur = randomShuffle(data_set, label_set)
      # predictions = []
      step =  data_set.shape[0]/batch_size
      for j in range (step):
        [data_bt, label_bt] = obtainMiniBatch(j,batch_size, data_set_cur, label_set_cur)
        loss, pred = my_model.forward(data_bt, label_bt)
        losses.append(loss);
        predictions = np.zeros(pred.shape)
        for p in range(pred.shape[0]):
            if pred[p] >= 0.5:
                predictions[p] = 1
            else:
                predictions[p] = 0

        my_model.backward(loss)
        my_model.update_param()
      accuracy = accuracy_score(label_set_cur, predictions)
      accuracies.append(accuracy)
      if (accuracy == 1):
          break;

    losses = np.asarray(losses)
    accuracies = np.asarray(accuracies)
    iteration = i+1
    print "\n\n\n***********************"


    return losses, accuracies, iteration





if __name__ == '__main__':
    batch_size = 64
    filename = "../dataset/p2/p21_random_imgs.npy"
    data_set = np.load(filename)
    filename = "../dataset/p2/p21_random_labs.npy"
    label_set = np.load(filename)

    #

    #*********************FULLY CONNECTED LAYER*********************#

    # *********************SIGMOID, L2 LOSS*************************#

    layer_list = [
        net.Flatten(),
        net.Linear(input_dim=16, output_dim=4),
        net.Sigmoid(),
        net.Linear(input_dim=4, output_dim=1),
        net.Sigmoid()

    ]


    loss_layer = net.L2_loss()
    optimizer = net.SGD_Optimizer(lr_rate=0.01, weight_decay=5e-4, momentum=0.99)
    my_model = net.Model(layer_list, loss_layer, optimizer)
    my_model.set_input_channel(1)

    losses1, accuracies1, iteration1 = train(my_model, data_set, label_set)

    plt.figure()
    plt.title("Loss, Sigmoid Activation with L2 Loss")
    plt.xlabel("Training Iterations")
    plt.ylabel("Loss")
    plt.plot(losses1, 'r--')
    plt.savefig('../figures/fig1.png')

    plt.figure()
    plt.title("Accuracies, Sigmoid Activation with L2 Loss")
    plt.xlabel("Training Iterations")
    plt.ylabel("Accuracy")
    plt.plot(accuracies1, 'r--')
    plt.savefig('../figures/fig2.png')

    # *********************SIGMOID, CROSS ENTROPY LOSS*************************#

    layer_list = [
        net.Flatten(),
        net.Linear(input_dim=16, output_dim=4),
        net.Sigmoid(),
        net.Linear(input_dim=4, output_dim=1),
        net.Sigmoid()

    ]


    loss_layer = net.Binary_cross_entropy_loss()
    optimizer = net.SGD_Optimizer(lr_rate=0.01, weight_decay=5e-4, momentum=0.99)
    my_model = net.Model(layer_list, loss_layer, optimizer)
    my_model.set_input_channel(1)

    losses2, accuracies2, iteration2 = train(my_model, data_set, label_set)

    plt.figure()
    plt.title("Loss, Sigmoid Activation with Binary Cross Entropy Loss")
    plt.xlabel("Training Iterations")
    plt.ylabel("Loss")
    plt.plot(losses2, 'r--')
    plt.savefig('../figures/fig3.png')

    plt.figure()
    plt.title("Accuracies, Sigmoid Activation with Binary Cross Entropy Loss")
    plt.xlabel("Training Iterations")
    plt.ylabel("Accuracy")
    plt.plot(accuracies2, 'r--')
    plt.savefig('../figures/fig4.png')

    # *********************RELU, L2 LOSS*************************#

    layer_list = [
        net.Flatten(),
        net.Linear(input_dim=16, output_dim=4),
        net.Relu(),
        net.Linear(input_dim=4, output_dim=1),
        net.Relu()

    ]

    loss_layer = net.L2_loss()
    optimizer = net.SGD_Optimizer(lr_rate=0.01, weight_decay=5e-4, momentum=0.99)
    my_model = net.Model(layer_list, loss_layer, optimizer)
    my_model.set_input_channel(1)

    losses3, accuracies3, iteration3 = train(my_model, data_set, label_set)

    plt.figure()
    plt.title("Loss, Relu Activation with L2 Loss")
    plt.xlabel("Training Iterations")
    plt.ylabel("Loss")
    plt.plot(losses3, 'r--')
    plt.savefig('../figures/fig5.png')

    plt.figure()
    plt.title("Accuracies, Relu Activation with L2 Loss")
    plt.xlabel("Training Iterations")
    plt.ylabel("Accuracy")
    plt.plot(accuracies2, 'r--')
    plt.savefig('../figures/fig6.png')

    # *********************RELU, CROSS ENTROPY LOSS*************************#



    layer_list = [
        net.Flatten(),
        net.Linear(input_dim=16, output_dim=4),
        net.Relu(),
        net.Linear(input_dim=4, output_dim=1),
        net.Sigmoid()

    ]


    loss_layer = net.Binary_cross_entropy_loss()
    optimizer = net.SGD_Optimizer(lr_rate=0.01, weight_decay=5e-4, momentum=0.99)
    my_model = net.Model(layer_list, loss_layer, optimizer)
    my_model.set_input_channel(1)


    losses4, accuracies4, iteration4 = train(my_model, data_set, label_set)
    plt.figure()
    plt.title("Loss, Relu Activation with Binary Cross Entropy Loss")
    plt.xlabel("Training Iterations")
    plt.ylabel("Loss")
    plt.plot(losses4, 'r--')
    plt.savefig('../figures/fig7.png')

    plt.figure()
    plt.title("Accuracies, Relu Activation with Binary Cross Entropy Loss")
    plt.xlabel("Training Iterations")
    plt.ylabel("Accuracy")
    plt.plot(accuracies4, 'r--')
    plt.savefig('../figures/fig8.png')

    #*************************************CNN************************************#

    filename = "../dataset/p2/p22_line_imgs.npy"
    data_set = np.load(filename)
    filename = "../dataset/p2/p22_line_labs.npy"
    label_set = np.load(filename)

    data_set = np.reshape(data_set, (data_set.shape[0],1,data_set.shape[1],data_set.shape[2]))
    print data_set.shape


    layer_list = [
        net.Conv2d(output_channel=16, kernel_size=7, padding=0, stride=(1,1)),
        net.BatchNorm2D(),
        net.Relu(),
        net.Conv2d(output_channel=8, kernel_size=7, padding=0, stride=(1,1)),
        net.BatchNorm2D(),
        net.Relu(),
        net.Flatten(),
        net.Linear(input_dim = 128, output_dim = 1),
        net.Sigmoid()
    ]

    loss_layer = net.Binary_cross_entropy_loss()
    optimizer = net.SGD_Optimizer(lr_rate=0.01, weight_decay=5e-4, momentum=0.99)
    my_model = net.Model(layer_list, loss_layer, optimizer)
    my_model.set_input_channel(1)

    losses4, accuracies4, iteration4 = train(my_model, data_set, label_set)

    print iteration1, iteration2, iteration3, iteration4
    plt.figure()
    plt.title("Loss, Relu Activation with Binary Cross Entropy Loss, CNN")
    plt.xlabel("Training Iterations")
    plt.ylabel("Loss")
    plt.plot(losses4, 'r--')
    plt.savefig('../figures/fig9.png')

    plt.figure()
    plt.title("Accuracies, Relu Activation with Binary Cross Entropy Loss, CNN")
    plt.xlabel("Training Iterations")
    plt.ylabel("Accuracy")
    plt.plot(accuracies4, 'r--')
    plt.savefig('../figures/fig10.png')
