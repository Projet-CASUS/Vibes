import numpy as np
import pandas as pd


class Transformation:
    def __init__(self):
        self.first = 0
        self.last = None
    def __call__(self, input):
        return input


class ImportFile(Transformation):
    def __init__(self, type='csv'):
        self.type = type

    def __call__(self, filename):
        if self.type == 'csv':
            newData = pd.read_csv(filename, delimiter=';')
            self.last = len(newData)
            return newData
        else:
            return None


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
    def __init__(self):
            pass