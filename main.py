import sys

from IPython.external.qt_for_kernel import QtGui

import vibes.Controller.controller as cont
import os
import vibes.View.qt_view as view
import vibes.transformations.differentiel as df

# Lance le programme à son emplacement
app = view.instanciate_qt_application()
program_folder = os.path.dirname(os.path.realpath(__file__))
os.chdir(program_folder)

filename = QtGui.QFileDialog.getOpenFileName()[0]
control = cont.Controller(filename,"controller_qt")

#control.addTransform(None)

sys.exit(app.exec_())
#control.app.exec_()
#data = vibes.DataVibes("./test_files/test00.csv")
#data.add_transformation(vibes.ImportFile, "philippe")
#data.insert_transformation(vibes.Filter, 1, None)
