import sys

import vibes.Controller.controller as cont
import os
import vibes.View.qt_view as view

# Lance le programme à son emplacement
app = view.instanciate_qt_application()
program_folder = os.path.dirname(os.path.realpath(__file__))
os.chdir(program_folder)

control = cont.Controller("./test_files/100.0Hz_20.0sec.csv")
control.time_range_selections(0, 2500)


#control.addTransform(None)

sys.exit(app.exec_())
#control.app.exec_()
#data = vibes.DataVibes("./test_files/test00.csv")
#data.add_transformation(vibes.ImportFile, "philippe")
#data.insert_transformation(vibes.Filter, 1, None)
