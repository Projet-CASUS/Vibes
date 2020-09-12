import sys

import vibes.Controller.controller as cont
import os

# Lance le programme à son emplacement
program_folder = os.path.dirname(os.path.realpath(__file__))
os.chdir(program_folder)

control = cont.Controller("./test_files/test00.csv")

control.define_graphic(control.my_interface.time_window)
control.data_range_selections(0, 2500)
control.define_graphic(control.my_interface.time_window)
control.define_graphic(control.my_interface.fourier_window)
control.define_pipeline_browser()
#control.addTransform(None)

sys.exit(control.app.exec_())
#control.app.exec_()
#data = vibes.DataVibes("./test_files/test00.csv")
#data.add_transformation(vibes.ImportFile, "philippe")
#data.insert_transformation(vibes.Filter, 1, None)
