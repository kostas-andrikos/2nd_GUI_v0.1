from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os
import json

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

class RapidTowSteeringDB(AFXDataDialog):
    
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'RTS Parameters',
            self.OK|self.APPLY|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')            

        applyBtn = self.getActionButton(self.ID_CLICKED_APPLY)
        applyBtn.setText('Apply')
            
        VFrame_1 = FXVerticalFrame(p=self, opts=LAYOUT_FILL_X|LAYOUT_FILL_Y, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        HFrame_1 = FXHorizontalFrame(p=VFrame_1, opts=LAYOUT_FILL_X, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        self.nrOfLayers = AFXSpinner(HFrame_1, 6, 'Number of Layers', form.nrLayersKw, 0)
        self.nrOfLayers.setRange(1, 100)
        self.nrOfLayers.setIncrement(1)
        AFXTextField(p=HFrame_1, ncols=8, labelText='Nominal Thickness: ', tgt=form.nomThickKw, sel=0)
        AFXTextField(p=HFrame_1, ncols=8, labelText='RTS Frequency: ', tgt=form.freqKw, sel=0)
        if isinstance(VFrame_1, FXHorizontalFrame):
            FXVerticalSeparator(p=VFrame_1, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        else:
            FXHorizontalSeparator(p=VFrame_1, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        VFrame_3 = FXVerticalFrame(p=VFrame_1, opts=LAYOUT_FILL_X, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        self.symmLamBtn = FXCheckButton(p=VFrame_3, text='Symmetric Laminate', tgt=form.symmetricLaminateKw, sel=0)
        vf = FXVerticalFrame(VFrame_3, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X,
            0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        table = AFXTable(p=vf, 
                        numVisRows=9, 
                        numVisColumns=5, 
                        numRows=5, 
                        numColumns=5, 
                        tgt=form.rtsParamsKw, 
                        sel=0, 
                        opts=AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        
        table.setPopupOptions(AFXTable.POPUP_COPY|AFXTable.POPUP_PASTE|AFXTable.POPUP_CLEAR_CONTENTS|AFXTable.POPUP_READ_FROM_FILE|AFXTable.POPUP_WRITE_TO_FILE)
        table.setLeadingRows(1)
        table.setLeadingColumns(1)
        for c in range(1, 4):
            table.setColumnWidth(c, 100)
            table.setColumnType(c, AFXTable.FLOAT)
        table.setColumnWidth(4, 100)
        table.setColumnType(4, AFXTable.LIST)
        table.setLeadingRowLabels('Phi\tT0\tT1\tMaterial')
        table.setStretchableColumn( table.getNumColumns()-1 )
        table.showHorizontalGrid(True)
        table.showVerticalGrid(True)

        # Make drop-down menus for the 'Material' column of the RTS Table.
        with open('tmp_dict.json', 'r') as file:
            dialog1_dict = json.load(file)
        material_keys = mdb.models[str(dialog1_dict['model_name'])].materials.keys()
        stackTableListID = table.addList(' \t' + '\t'.join(material_keys))
        table.setColumnListId(4, stackTableListID)
        self.table = table

    def processUpdates(self):
        # This method gets called continuously in order to check for updates; do not write time-consuming operations here.
        # Adjust table size based on number-of-layers spinner value
        if self.table.getNumRows() - 1 < self.nrOfLayers.getValue():
            self.table.insertRows(startRow=self.table.getNumRows(), numRows=1, notify=True)
        if self.table.getNumRows() - 1 > self.nrOfLayers.getValue():
            self.table.deleteRows(startRow=self.table.getNumRows() - 1, numRows=1, notify=True)

        # Make bottom-half rows of the rtsTable non-editable if symmetric-laminate button is checked. 
        for r in range(int(self.table.getNumRows() / 2) + 1, self.table.getNumRows()):
            for c in range(1, 5):
                if self.symmLamBtn.getCheck() == True:
                    self.table.setItemEditable(row=r, column=c, editable=False)
                else:
                    self.table.setItemEditable(row=r, column=c, editable=True)
                if self.table.getItemText(row=r, column=c,) <> '':
                    self.table.setItemEditable(row=r, column=c, editable=True)
        self.table.shadeReadOnlyItems(True)
        self.table.setLeadingColumnLabels('\t'.join(['Ply {0:02d}'.format(i) for i in range(1, self.table.getNumRows())]))
