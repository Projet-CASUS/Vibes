import numpy as np
import pandas as pd


class Transformation:
    def __init__(self):
        pass
    def __call__(self, input):
        return input


class ImportFile(Transformation):
    def __init__(self, type='csv'):
        super().__init__()
        self.type = type

    def __call__(self, filename):
        if self.type == 'csv':
            return pd.read_csv(filename, delimiter=';')
        else:
            return filename


class frenquency_transformation():
    pass

class Filter(Transformation):
    def __init__(self, type=None):
        super().__init__()
        self.type = type

    def __call__(self, data):
        """
        TODO Louis-Philippe
        :param data:
        :return:
        """
        if self.type is None:
            return data
        elif type == "philippe":
            return "Philippe is a stud!"
        else:
            return None

class RangeSelection(Transformation):
    """
    TODO philippe
    """
    def __init__(self,first,last):
        super().__init__()
        self.first = first
        self.last = last
        self.NameArray = ["time", "x", "y", "z", "gforce"]
        self.type = "RangeSelection"
        self.savedUpData =[[0 for x in range(len(self.NameArray))] for i in range((self.last - self.first))]
    def __call__(self,data):
        for x in range(0, len(self.NameArray)):
            self.data_relocation(x,data)
        newData = pd.DataFrame(self.savedUpData, columns=['time','x','y','z','gforce'])
        return newData

    def data_relocation(self,i,data):
        for x in range(0, self.last - self.first):
             self.savedUpData[x][i] = data.loc[:, self.NameArray[i]][x + self.first]

    def merge(self):
        """
        merge time together
        :return:
        """
        pass
class FiltreParralele():
    """
    TODO Louis-Philippe
    """
    pass