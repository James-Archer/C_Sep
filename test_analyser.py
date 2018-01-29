# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 12:51:34 2018

@author: jia335

Tests for the analyser
"""

from analyser import Analyser
import numpy as np

def test_basic_data():
    '''
    Makes sure that the analyser can still correctly read a basic file set. 
    '''
    a = Analyser('test-LogFile',
                 parentDir=r'C:\Users\jia335\projects\c_sep\test_dir',
                 runScheme = ['SubtractBackground', 'Sum'],
                 runArgs = [{'window':5, 'inverted':False}, {}]
                 )
    assert np.all(a.results == (np.zeros_like(a.results)+10))