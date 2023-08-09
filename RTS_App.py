"""
This script will create the prototype application.
"""

from abaqusGui import *
import sys
from RTS_MainWindow import RapidTowSteeringMainWindow

# Initialize the application object.
#
app = AFXApp('ABAQUS/CAE', 'ABAQUS, Inc.')
app.init(sys.argv)

# Construct the main window.
#
RapidTowSteeringMainWindow(app)

# Create the application and run it.
#
app.create()
app.run()
