import vibes
import vibes.Controller.controller as ContLivesMatter
import pandas as pd
import numpy as np

control = ContLivesMatter.Controller("./test_files/test00.csv")
#control.addTransform(None)
control.dataRangeSelections(1,2)
#data = vibes.DataVibes("./test_files/test00.csv")
#data.add_transformation(vibes.ImportFile, "philippe")
#data.insert_transformation(vibes.Filter, 1, None)