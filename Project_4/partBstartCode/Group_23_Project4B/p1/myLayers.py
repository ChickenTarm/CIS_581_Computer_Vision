'''
  File name: myLayers.py
  Author: Hongrui Zheng
  Date: 11/28/17
'''
import numpy as np

'''
  Sigmoid layer
  - Input x: ndarray
  - Output y: nonlinearized result
'''
def Sigmoid(x):
  y = 1/(1+np.exp(-x))
  return y


'''
  Relu layer
  - Input x: ndarray 
  - Output y: nonlinearized result
'''
def Relu(x):
  y = np.max([0.0, x])
  return y


'''
  l2 loss layer
  - Input pred: prediction values
  - Input gt: the ground truth 
  - Output loss: averaged loss
'''
def L2_loss(pred, gt):
  loss = np.sum(np.square(pred-gt))/2
  try:
    loss = loss/pred.shape[0]
  except:
    pass
  return loss



'''
  Cross entropy loss layer
  - Input pred: prediction values
  - Input gt: the ground truth 
  - Output loss: averaged loss
'''
def Cross_entropy_loss(pred, gt):
  # if gt == 1:
  #   loss = -np.log(pred)
  # else:
  #   loss = -np.log(1-pred)
  loss = -(gt*np.log(pred)+(1-gt)*np.log(1-pred))
  try:
    loss = loss/pred.shape[0]
  except:
    pass
  return loss