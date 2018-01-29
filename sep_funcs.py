# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 11:56:43 2018

@author: jia335

A collection of separation functions and misc tools that the analyser class can use
"""
import numpy as np

def SubtractBackground(x, window = 1000, inverted = True):
    '''
    Subtacts the background signal and returns the new signal
    Arguments:
    x -- An iterable containing the data.
    Keyword arguments:
    window -- An integer describing the amount of data to use to subtract.
    inverted -- A bool describing whether the data is inverted or not.
    Returns:
    output -- A np array of the background subtracted signal.
    '''
    output = np.array(x)
    bg = np.average(output[:window])
    output = output - bg
    if inverted:
        return output*-1
    return output

def Sum(x):
    '''
    Simple test analysis that just returns the sum of the data
    '''
    return np.sum(x)