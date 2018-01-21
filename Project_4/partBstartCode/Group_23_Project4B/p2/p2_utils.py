'''
  File name: p2_utils.py
  Author: Shraddha Jain
  Date: 12/11/2017
'''
import numpy as np
from sklearn.utils import shuffle
np.set_printoptions(threshold=np.nan)


def randomShuffle(data_set, label_set):

    data_set, label_set  = shuffle(data_set,  label_set, random_state=0)

    return data_set, label_set


def obtainMiniBatch(value, batch_size, data_set, label_set):


    data_bt = data_set[value*batch_size:(value*batch_size+batch_size), :]
    label_bt = label_set[value*batch_size:(value*batch_size+batch_size)]

    return  data_bt, label_bt