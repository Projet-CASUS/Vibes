import sys

from qwt import QwtPlot, QwtPlotCurve

import vibes
import vibes.Controller.controller as ContLivesMatter
import pandas as pd
import numpy as np


control = ContLivesMatter.Controller("./test_files/test00.csv")
control.data_range_selections(2000,2500)
control.show_of_time_graphic()
control.show_of_pipeline()

#control.addTransform(None)


sys.exit(control.app.exec_())
#control.app.exec_()
#data = vibes.DataVibes("./test_files/test00.csv")
#data.add_transformation(vibes.ImportFile, "philippe")
#data.insert_transformation(vibes.Filter, 1, None)