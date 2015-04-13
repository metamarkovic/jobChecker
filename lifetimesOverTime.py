from __future__ import print_function
import os
import xml.etree.cElementTree as ET
import glob


class lifetimesOverTime():
    population_path = './EC14-Exp-51/population'

    def readConfig(self,population_path):
        for filename in glob.glob(os.path.join(population_path, '*.vxa')):
            tree = ET.ElementTree(file=filename)
            root = tree.getroot()

            lifetime = root.find('Simulator').find('StopCondition').find('StopConditionValue').text

            f = open('51' + '_' + 'lifetimes.txt','w')
            f.write(str(filename) + '   ' + str(lifetime) + '\n') # python will convert \n to os.linesep
            f.close()

    def __init__(self):
        self.readConfig(self.population_path)