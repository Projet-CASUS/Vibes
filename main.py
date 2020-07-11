import vibes
import vibes.Controller.controller as ContLivesMatter
import pandas as pd
import numpy as np
import os

# Lance le programme à son emplacement
program_folder = os.path.dirname(os.path.realpath(__file__))
os.chdir(program_folder)

control = ContLivesMatter.Controller("./test_files/test00.csv")
#control.addTransform(None)
#data = vibes.DataVibes("./test_files/test00.csv")
#data.add_transformation(vibes.ImportFile, "philippe")
#data.insert_transformation(vibes.Filter, 1, None)
