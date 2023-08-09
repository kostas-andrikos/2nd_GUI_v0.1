from abaqusGui import *
import numpy as np

class RTSForm(AFXForm):
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(self, 'main', 'rtsMain')

        self.nrLayersKw = AFXIntKeyword(self.cmd, 'nrLayers', True, 4)
        self.nomThickKw = AFXFloatKeyword(self.cmd, 'nomThick', True, 0.18)
        self.symmetricLaminateKw = AFXBoolKeyword(self.cmd, 'symmetricLaminate', AFXBoolKeyword.TRUE_FALSE, True, False)
        self.rtsParamsKw = AFXTableKeyword(self.cmd, 'rtsParams', True)
        for c in range(3):
            self.rtsParamsKw.setColumnType(c, AFXTABLE_TYPE_FLOAT)
        self.rtsParamsKw.setColumnType(3, AFXTABLE_TYPE_STRING)
        self.freqKw = AFXIntKeyword(self.cmd, 'freq', True, 4)

    def error_callback(self, message):
        showAFXErrorDialog(getAFXApp().getAFXMainWindow(), message)

    def warning_callback(self, message):
        showAFXWarningDialog(getAFXApp().getAFXMainWindow(), message)

    def getFirstDialog(self):

        import rtsDB
        return rtsDB.RapidTowSteeringDB(self)
    
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False