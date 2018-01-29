# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 11:04:52 2018

@author: jia335
"""

import numpy as np
from matplotlib import pyplot as plt
import os as os
from sep_funcs import *

class Analyser():
    '''
    The class to wrap up all the functionality of the Cherenkov separation. 
    Call this with the logFile name and it **should** figure out everything from there.
    '''
    def __init__(self, logFileName, parentDir = None):
        '''
        Sets up the files to be run, then executes the analysis. Try to run from the parent directory to output/
        Arguments:
        logFileName -- String. The name of the log file to be read. Standard format is just the file name (no ext).
            Can also be the absolute path (with ext).
        '''
        
        self.methods = {'SubtractBackground': SubtractBackground,
                        'Sum': Sum
                        }
        
        if parentDir:
            os.chdir(parentDir)
        self.files = []
        self.pos = None
        try:
            logFile = open('./output/{}.txt'.format(logFileName))
        except:
            try:
                logFile = open(logFileName)
            except:
                print('Cannot open file')
                return
        self.is2D = False
        for line in logFile:
            if '***2D***' in line:
                self.is2D = True
            elif 'txt' in line:
                self.files.append(line.split('\n')[0])
            elif 'xStart' in line:
                xStart = float(line.split('\t')[1])
            elif 'xStep' in line:
                xStep = float(line.split('\t')[1])
            elif 'yStart' in line:
                yStart = float(line.split('\t')[1])
            elif 'yStep' in line:
                yStep = float(line.split('\t')[1])
            elif 'n_x' in line:
                nx = int(line.split('\t')[1].split('.')[0])
            elif 'n_y' in line:
                ny = int(line.split('\t')[1].split('.')[0])
            elif 'Step (mm)' in line:
                delta = float(line.split('\t')[1])
            elif 'Start pos' in line:
                x0 = float(line.split('\t')[1])
            elif 'Stationary position' in line:
                y0 = float(line.split('\t')[1])
        logFile.close()
        
        self.results = []
        for file in self.files:
            self.results.append(self.RunFile('./output/' + file))
        self.results = np.array(self.results)
        
        if self.is2D:
            
            self.pos = np.array(np.meshgrid(np.arange(nx)*xStep+xStart, np.arange(ny)*yStep+yStart))
            self.results = self.results.reshape(self.pos[0].shape)
            
        else:
        
            self.pos = np.arange(len(self.files))*delta + x0
            
    def RunFile(self, fName):
        
        x = np.loadtxt(fName, dtype = np.float16, skiprows=4, delimiter='\t', usecols = 1)
        print(x.min(), x.max())
        x = self.methods['SubtractBackground'](x)
        return self.methods['Sum'](x)
    
    def Plot3D(self):
        
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import cm
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(self.pos[0], self.pos[1], self.results, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
        plt.show()
        
    
if __name__=='__main__':
    
    a = Analyser('07-01-2018-131122-LogFile', parentDir=r'C:\Users\jia335\Documents\PS_Waveform_Averager')
    a.Plot3D()