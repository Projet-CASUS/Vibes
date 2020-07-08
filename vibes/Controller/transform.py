import numpy as np
import pandas as pd


class Transformation:
    def __init__(self):
        pass
    def __call__(self, input):
        return input


class ImportFile(Transformation):
    def __init__(self, type='csv'):
        self.type = type

    def __call__(self, filename):
        if self.type == 'csv':
            return pd.read_csv(filename, delimiter=';')
        else:
            return filename


class Filter(Transformation):
    def __init__(self, type=None):
        self.type = type

    def __call__(self, data):
        if self.type is None:
            return data
        elif type == "philippe":
            return "Philippe is a stud!"
        else:
            return None

class RangeSelection(Transformation):
    #Philippe Boudreau
    def __init__(self,first,last):
            self.first = first
            self.last = last
            self.NameArray = ["time", "x", "y", "z", "gforce"]
    def __call__(self,data):
        for x in range(0, len(self.NameArray)):
            self.data_separation(x,data)
        print(data)
        return data

    def data_separation(self,i,data):
        for x in range(0, self.last - self.first):
             data.loc[:,self.NameArray[i]][x] = data.loc[:, self.NameArray[i]][x + self.first]
