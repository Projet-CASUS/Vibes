import vibes
import pandas as pd
import numpy as np


data = vibes.DataVibes("./test_files/test00.csv")
data.add_transformation(vibes.Filter, "philippe")
data.insert_transformation(vibes.Filter, 1, None)