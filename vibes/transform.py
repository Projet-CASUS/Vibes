import numpy as np
import pandas as pd


class Transformation:
    def __init__(self):
        pass

    def __call__(self, input):
        return input


class ImportFile (Transformation):
    def __init__(self, type='csv'):
        super().__init__()
        self.type = type

    def __call__(self, filename):
        if self.type == 'csv':
            return pd.read_csv(filename, delimiter=';')
        else:
            return None


class Filter (Transformation):
    def __init__(self, type=None):
        super().__init__()
        self.type = type

    def __call__(self, data):
        if type is None:
            return data
        elif type == "philippe":
            return "Philippe is a nerd!"
        else:
            return None
