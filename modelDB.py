from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class ModelDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        self.form = form

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Select Model',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)


        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')

        GroupBox_1 = FXGroupBox(p=self, text='Select a method', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        FXRadioButton(p=GroupBox_1, text='Model from database', tgt=form.methodKw, sel=1)
        FXRadioButton(p=GroupBox_1, text='Import mesh file', tgt=form.methodKw, sel=2)

        self.swt_method = FXSwitcher(self, 0, 0,0,0,0, 0,0,0,0)

        # ----------------------------------------------------------------------
        GroupBox_2 = FXGroupBox(p=self.swt_method, text='Inputs', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        VAligner_1 = AFXVerticalAligner(p=GroupBox_2, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)


        self.RootComboBox_1 = AFXComboBox(p=VAligner_1, ncols=0, nvis=1, text='Model:', tgt=form.model_nameKw, sel=0)
        self.RootComboBox_1.setMaxVisible(10)

        names = mdb.models.keys()
        names.sort()
        for name in names:
            self.RootComboBox_1.appendItem(name)
        if not form.model_nameKw.getValue() in names:
            form.model_nameKw.setValue( names[0] )
        msgCount = 99
        form.model_nameKw.setTarget(self)
        form.model_nameKw.setSelector(AFXDataDialog.ID_LAST+msgCount)
        msgHandler = str(self.__class__).split('.')[-1] + '.onComboBox_1PartsChanged'
        exec('FXMAPFUNC(self, SEL_COMMAND, AFXDataDialog.ID_LAST+%d, %s)' % (msgCount, msgHandler) )


        # Parts combo
        #
        self.ComboBox_1 = AFXComboBox(p=VAligner_1, ncols=0, nvis=1, text='Part:', tgt=form.part_nameKw, sel=0)
        self.ComboBox_1.setMaxVisible(10)
        
        # ----------------------------------------------------------------------
        GroupBox_3 = FXGroupBox(p=self.swt_method, text='Inputs', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        VAligner_2 = AFXVerticalAligner(p=GroupBox_3, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        
        # Model combo
        # Since all forms will be canceled if the  model changes,
        # we do not need to register a query on the model.
        #
        # self.RootComboBox_2 = AFXComboBox(p=VAligner_2, ncols=0, nvis=1, text='Import to: ', tgt=form.rf_model_nameKw, sel=0)
        # self.RootComboBox_2.setMaxVisible(10)

        # names = mdb.models.keys()
        # names.sort()
        # for name in names:
        #     self.RootComboBox_2.appendItem(name)
        # if not form.rf_model_nameKw.getValue() in names:
        #     form.rf_model_nameKw.setValue( names[0] )

        
        fileHandler = Import_meshDBFileHandler(form, 'mesh_file', 'Text File (*.txt)')
        fileTextHf = FXHorizontalFrame(p=VAligner_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        fileTextHf.setSelector(99)
        AFXTextField(p=fileTextHf, ncols=32, labelText='Mesh file: ', tgt=form.mesh_fileKw, sel=0,
            opts=AFXTEXTFIELD_STRING|LAYOUT_CENTER_Y)
        icon = afxGetIcon('fileOpen', AFX_ICON_SMALL )
        FXButton(p=fileTextHf, text='	Select File\nFrom Dialog', ic=icon, tgt=fileHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=1, pr=1, pt=1, pb=1)
            
#        AFXTextField(p=VAligner_2, ncols=32, labelText='Section name: ', tgt=form.rf_section_nameKw, sel=0)
        
        # fileHandler = Import_meshDBFileHandler(form, 'rf_layup_file', 'Layups (*.xml)')
        # fileTextHf = FXHorizontalFrame(p=VAligner_2, opts=0, x=0, y=0, w=0, h=0,
        #     pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # # Note: Set the selector to indicate that this widget should not be
        # #       colored differently from its parent when the 'Color layout managers'
        # #       button is checked in the RSG Dialog Builder dialog.
        # fileTextHf.setSelector(99)
        # AFXTextField(p=fileTextHf, ncols=32, labelText='Layup file: ', tgt=form.rf_layup_fileKw, sel=0,
        #     opts=AFXTEXTFIELD_STRING|LAYOUT_CENTER_Y)
        # icon = afxGetIcon('fileOpen', AFX_ICON_SMALL )
        # FXButton(p=fileTextHf, text='	Select File\nFrom Dialog', ic=icon, tgt=fileHandler, sel=AFXMode.ID_ACTIVATE,
        #     opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=1, pr=1, pt=1, pb=1)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def show(self):

        AFXDataDialog.show(self)

        # Register a query on materials
        #
        self.currentModelName = getCurrentContext()['modelName']
        self.form.model_nameKw.setValue(self.currentModelName)
        mdb.models[self.currentModelName].materials.registerQuery(self.updateComboBox_1Parts)

        # Register a query on amplitudes
        #
#        self.currentModelName = getCurrentContext()['modelName']
#        self.form.rf_model_nameKw.setValue(self.currentModelName)
#        mdb.models[self.currentModelName].amplitudes.registerQuery(self.updateComboBox_2Amplitudes)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def hide(self):

        AFXDataDialog.hide(self)

        mdb.models[self.currentModelName].materials.unregisterQuery(self.updateComboBox_1Parts)

#        mdb.models[self.currentModelName].amplitudes.unregisterQuery(self.updateComboBox_2Amplitudes)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def processUpdates(self):
        
        if self.form.methodKw.getValue() == 1:
            self.swt_method.setCurrent(0)
        elif self.form.methodKw.getValue() == 2:
            self.swt_method.setCurrent(1)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def onComboBox_1PartsChanged(self, sender, sel, ptr):

        self.updateComboBox_1Parts()
        return 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def updateComboBox_1Parts(self):

        modelName = self.form.model_nameKw.getValue()

        # Update the names in the Materials combo
        #
        self.ComboBox_1.clearItems()
        names = mdb.models[modelName].parts.keys()
        names.sort()
        for name in names:
            self.ComboBox_1.appendItem(name)
        if names:
            if not self.form.part_nameKw.getValue() in names:
                self.form.part_nameKw.setValue( names[0] )
        else:
            self.form.part_nameKw.setValue('')

        self.resize( self.getDefaultWidth(), self.getDefaultHeight() )

#    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    def onComboBox_2AmplitudesChanged(self, sender, sel, ptr):
#
#        self.updateComboBox_2Amplitudes()
#        return 1
#
#    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    def updateComboBox_2Amplitudes(self):
#
#        modelName = self.form.rf_model_nameKw.getValue()
#
#        # Update the names in the Amplitudes combo
#        #
#        self.ComboBox_2.clearItems()
#        names = mdb.models[modelName].amplitudes.keys()
#        names.sort()
#        for name in names:
#            self.ComboBox_2.appendItem(name)
#        if names:
#            if not self.form.amplitudeNameKw.getValue() in names:
#                self.form.amplitudeNameKw.setValue( names[0] )
#        else:
#            self.form.amplitudeNameKw.setValue('')
#
#        self.resize( self.getDefaultWidth(), self.getDefaultHeight() )



###########################################################################
# Class definition
###########################################################################

class Import_meshDBFileHandler(FXObject):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form, keyword, patterns='*'):

        self.form = form
        self.patterns = patterns
        self.patternTgt = AFXIntTarget(0)
        exec('self.fileNameKw = form.%sKw' % keyword)
        self.readOnlyKw = AFXBoolKeyword(None, 'readOnly', AFXBoolKeyword.TRUE_FALSE)
        FXObject.__init__(self)
        FXMAPFUNC(self, SEL_COMMAND, AFXMode.ID_ACTIVATE, Import_meshDBFileHandler.activate)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def activate(self, sender, sel, ptr):

       fileDb = AFXFileSelectorDialog(getAFXApp().getAFXMainWindow(), 'Select a File',
           self.fileNameKw, self.readOnlyKw,
           AFXSELECTFILE_ANY, self.patterns, self.patternTgt)
       fileDb.setReadOnlyPatterns('*.odb')
       fileDb.create()
       fileDb.showModal()