from abaqusGui import *
import modelForm
import rtsForm
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)
thisDir = os.path.join(thisDir, 'icons')

###########################################################################
# Class definition
###########################################################################

class RapidTowSteeringToolsetGui(AFXToolsetGui):
    [
        ID_MOD,
        ID_RTS,
    ] = range(AFXToolsetGui.ID_LAST, AFXToolsetGui.ID_LAST+2)
    
    def __init__(self):
        # Construct the base class.
        #
        AFXToolsetGui.__init__(self, 'Test Toolset')
        
        FXMAPFUNC(self, SEL_COMMAND, self.ID_MOD,   RapidTowSteeringToolsetGui.onCmdMOD)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_RTS,   RapidTowSteeringToolsetGui.onCmdRTS)
        self.model_form = modelForm.ModelForm(self)
        self.rts_form = rtsForm.RTSForm(self)
        
        # Toolbox buttons
        toolbar_group_1 = AFXToolbarGroup(self, title='RTS Design Toolset')

        ic = afxCreateIcon(os.path.join(thisDir, 'sc_homo_small.png'))
        self.modelBtn = AFXToolButton(p     = toolbar_group_1, 
                                    label = '\tSelect Model', 
                                    icon  = ic, 
                                    tgt   = self.model_form, 
                                    sel   = AFXMode.ID_ACTIVATE)
        

        ic = afxCreateIcon(os.path.join(thisDir, 'sc_import_k_small.png'))
        self.rtsBtn = AFXToolButton(p     = toolbar_group_1, 
                                    label = '\tRTS Parameters', 
                                    icon  = ic, 
                                    tgt   = self.rts_form, 
                                    sel   = AFXMode.ID_ACTIVATE)
        

    def getKernelInitializationCommand(self):

        return 'import modelMain\nimport rtsMain'

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def onCmdMOD(self, sender, sel, ptr):
        # Reload the form module and reconstruct the form so that any
        # changes to that module are updated.
        #
        reload(modelForm)
        self.model_form = modelForm.ModelForm(self)
        self.modelBtn.setTarget(self.model_form)
        getAFXApp().getAFXMainWindow().writeToMessageArea(
            'The modelForm has been reloaded.')

        return 1
    
    def onCmdRTS(self, sender, sel, ptr):
        # Reload the form module and reconstruct the form so that any
        # changes to that module are updated.
        #
        reload(rtsForm)
        self.rts_form = rtsForm.RTSForm(self)
        self.rtsBtn.setTarget(self.rts_form)
        getAFXApp().getAFXMainWindow().writeToMessageArea(
            'The RTSForm has been reloaded.')

        return 1