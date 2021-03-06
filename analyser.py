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
    def __init__(self, logFileName, parentDir = None, runScheme = None, runArgs = None):
        '''
        Sets up the files to be run, then executes the analysis. Try to run from the parent directory to output/
        Arguments:
        logFileName -- String. The name of the log file to be read. Standard format is just the file name (no ext).
            Can also be the absolute path (with ext).
        parentDir -- String. The directory that is the relative parent to the /output/ with the logFile.
        runScheme -- List. The function names to run on the data, in order of running.
        runArgs -- List. List of dicts of the keyword args for the each function in runScheme.
        '''
        
        self.methods = {'SubtractBackground': SubtractBackground,
                        'Sum': Sum
                        }
        if not runScheme:
            # Default runScheme. Can also be used as template
            self.runScheme = ['SubtractBackground', 'Sum']
        else:
            self.runScheme = runScheme
            
        if not runArgs:
            # Default runArgs. Can also be used as template
            self.runArgs = [{'window':1000, 'inverted':True},
                            {}
                            ]
        else:
            self.runArgs = runArgs
            
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
        
        # Run for each file in the log
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
        
        x = np.loadtxt(fName, dtype = np.float32, skiprows=4, delimiter='\t', usecols = 1)
        for scheme, args in zip(self.runScheme[:-1], self.runArgs[-1]):
            x = self.methods[scheme](x, **args)
        return self.methods[self.runScheme[-1]](x, **self.runArgs[-1])
    
    def Plot3D(self):
        '''
        Does a 3D plot
        '''
        
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import cm
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(self.pos[0], self.pos[1], self.results, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
        plt.show()
        
    def Plot2D(self):
        '''
        Does a 2D plot.
        '''
        
        plt.plot(self.pos, self.results)
        plt.show()
        
    def Plot(self):
        '''
        Decide which plot to use. Quite simple.
        '''
        
        if self.is2DL:
            self.Plot3D()
        else:
            self.Plot2D()
        
    
if __name__=='__main__':
    
    a = Analyser('07-01-2018-131122-LogFile', parentDir=r'C:\Users\jia335\Documents\PS_Waveform_Averager')
    a.Plot3D()