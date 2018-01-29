# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 11:04:52 2018

@author: jia335
"""

class Analyser():
    
    def __init__(self, logFileName):
        '''
        Sets up the files to be run, then executes the analysis. Try to run from the parent directory to output/
        Arguments:
        logFileName -- String. The name of the log file to be read. Standard format is just the file name (no ext). Can also be the absolute path (with ext).
        '''
        
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
            if 'txt' in line:
                self.files.append(line.split('\n')[0])
            if 'xStart' in line:
                xStart = float(line.split('\t')[1])
            if 'xStep' in line:
                xStep = float(line.split('\t')[1])
            if 'yStart' in line:
                yStart = float(line.split('\t')[1])
            if 'yStep' in line:
                yStep = float(line.split('\t')[1])
            if 'n_x' in line:
                nx = int(line.split('\t')[1].split('.')[0])
            if 'n_y' in line:
                ny = int(line.split('\t')[1].split('.')[0])
        logFile.close()
        
        