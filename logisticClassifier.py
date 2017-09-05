import numpy as np
import math, pdb
#import matplotlib.pyplot as plt

import six
print six.__file__

def softMax(x):
    """
    SoftMax function: S(yi) = e^yi / Sigma j (e^yj)
    takes input of liner function scores
    :return:
    return probability per score
    """
    #TODO: change this to work with more than 1 dimential array
    # x_exp = [math.exp(num) for num in x]
    # sum_x_exp = sum(x_exp)
    # softmax = [round(i/sum_x_exp, 8) for i in x_exp]
    # print(softmax)

    # Or using Numpy builtin functions
    return np.exp(x) / np.sum(np.exp(x), axis=0)

def linerModel():
    """
    WX+B=Y
    :return:
    Logits (scores)
    """
    pass

def crossEntopy():
    """
    D(S,L)
    :return:
    distance between probability and 1-hot labling
    """
    pass

scores = np.array([1, 2, 3, 6])
print(softMax(scores))
