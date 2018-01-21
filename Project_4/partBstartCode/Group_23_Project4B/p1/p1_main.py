'''
  File name: p1_main.py
  Author: Hongrui Zheng
  Date: 11/28/2017
'''
import numpy as np
import myLayers as layers
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# calculating for the matrices
# init
x = np.array([1.0])[np.newaxis]
W = np.arange(-1,1,0.01)
b = np.arange(-1,1,0.01)
# fully connected
y = np.empty((len(W), len(b)))
for i in xrange(len(W)):
	for j in xrange(len(b)):
		y[i,j] = W[i]*x + b[j]
W, b = np.meshgrid(W, b)
# activation
sig_y = np.reshape(np.asarray([layers.Sigmoid(y_curr) for y_row in y for y_curr in y_row])[np.newaxis], (200,200))
relu_y = np.reshape(np.asarray([layers.Relu(y_curr) for y_row in y for y_curr in y_row])[np.newaxis], (200,200))

# losses
gt = 0.5
# l2
l2_sig = np.reshape(np.asarray([layers.L2_loss(sig_curr, gt) for sig_row in sig_y for sig_curr in sig_row])[np.newaxis], (200, 200))
l2_relu = np.reshape(np.asarray([layers.L2_loss(relu_curr, gt) for relu_row in relu_y for relu_curr in relu_row])[np.newaxis], (200,200))
# ce
ce_sig = np.reshape(np.asarray([layers.Cross_entropy_loss(sig_curr, gt) for sig_row in sig_y for sig_curr in sig_row])[np.newaxis], (200,200))
ce_relu = np.reshape(np.asarray([layers.Cross_entropy_loss(relu_curr, gt) for relu_row in relu_y for relu_curr in relu_row])[np.newaxis], (200,200))

# backward gradient
# l2
l2_sig_back = (sig_y-gt)*x
l2_relu_back = (relu_y-gt)*x
# ce
ce_sig_back = (sig_y-gt)*x
ce_relu_back = (relu_y-gt)*x

# plotting
fig = plt.figure()
ax = plt.subplot(251, projection='3d')
ax.plot_surface(X=W, Y=b, Z=sig_y, cmap=cm.coolwarm,linewidth=0.01, antialiased=False)
ax.set_title('Sigmoid', fontsize=10)
ax = plt.subplot(252, projection='3d')
ax.plot_surface(X=W, Y=b, Z=relu_y,cmap=cm.coolwarm,linewidth=0.01, antialiased=False)
ax.set_title('Relu', fontsize=10)
ax = plt.subplot(253, projection='3d')
ax.plot_surface(X=W, Y=b, Z=l2_sig, cmap=cm.coolwarm, linewidth=0.01, antialiased=False)
ax.set_title('Sigmoid L2 Loss', fontsize=10)
ax = plt.subplot(254, projection='3d')
ax.plot_surface(X=W, Y=b, Z=l2_relu, cmap=cm.coolwarm, linewidth=0.01, antialiased=False)
ax.set_title('Relu L2 Loss', fontsize=10)
ax = plt.subplot(255, projection='3d')
ax.plot_surface(X=W, Y=b, Z=l2_sig_back, cmap=cm.coolwarm, linewidth=0.01, antialiased=False)
ax.set_title('Sigmoid L2 Loss Backward Gradient', fontsize=10)
ax = plt.subplot(256, projection='3d')
ax.plot_surface(X=W, Y=b, Z=l2_relu_back, cmap=cm.coolwarm, linewidth=0.01, antialiased=False)
ax.set_title('Relu L2 Loss Backward Gradient', fontsize=10)
ax = plt.subplot(257, projection='3d')
ax.plot_surface(X=W, Y=b, Z=ce_sig, cmap=cm.coolwarm, linewidth=0.01, antialiased=False)
ax.set_title('Sigmoid Cross Entropy Loss', fontsize=10)
ax = plt.subplot(258, projection='3d')
ax.plot_surface(X=W, Y=b, Z=ce_relu, cmap=cm.coolwarm, linewidth=1, antialiased=False)
ax.set_title('Relu Cross Entropy Loss', fontsize=10)
ax = plt.subplot(259, projection='3d')
ax.plot_surface(X=W, Y=b, Z=ce_sig_back, cmap=cm.coolwarm, linewidth=0.01, antialiased=False)
ax.set_title('Sigmoid Cross Entropy Loss Backward Gradient', fontsize=10)
ax = plt.subplot(2, 5, 10, projection='3d')
ax.plot_surface(X=W, Y=b, Z=ce_relu_back, cmap=cm.coolwarm, linewidth=0.01, antialiased=False)
ax.set_title('Relu Cross Entropy Loss Backward Gradient', fontsize=10)
plt.show()

