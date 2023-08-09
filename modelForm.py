from abaqusGui import *
import numpy as np 
# Note: The above form of the import statement is used for the prototype
# application to allow the module to be reloaded while the application is
# still running. In a non-prototype application you would use the form:
# from myDB import MyDB

class ModelForm(AFXForm):
    def __init__(self, owner):
        AFXForm.__init__(self, owner)
        
        self.cmd = AFXGuiCommand(self, 'main', 'modelMain')
        pickedDefault = ''
        self.radioButtonGroups = {}

        self.methodKw = AFXIntKeyword(self.cmd, 'method', True, 1)
        self.model_nameKw = AFXStringKeyword(self.cmd, 'model_name', True)
        self.part_nameKw = AFXStringKeyword(self.cmd, 'part_name', True)
        self.mesh_fileKw = AFXStringKeyword(self.cmd, 'mesh_file', True)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import modelDB
        return modelDB.ModelDB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

 
    

    # def issueCommands(self, *args):
    #     # Since this is a prototype application, just write the command to
    #     # the Message Area so it can be visually verified. If you have
    #     # defined a "real" command, then you can comment out this method to
    #     # have the command issued to the kernel.
    #     #
    #     # In a non-prototype application you normally do not need to write
    #     # the issueCommands() method.
    #     #
    #     cmd_str1 = self.cmd.getCommandString()
    #     # cmd_str1 = cmd_str1.replace(', ,',',False,')
    #     # cmd_str1 = cmd_str1.replace(', ,',',False,')
    #     # cmd_str1 = cmd_str1.replace(',)',',False)')
    #     # cmd_str1 = cmd_str1.replace('(,False','(False,False')

    #     b = ('import modelMain\n'
    #          + 'reload(modelMain)\n'
    #          + cmd_str1)

    #     with open('tmp_MODELcmd.py', 'w') as f:
    #         f.write(b)
    #     try:
    #         sendCommand(r'execfile("tmp_MODELcmd.py")',
    #                     writeToReplay=False, writeToJournal=True)
    #     except Exception as e:
    #         msg = r'ERROR: For debugging purposes run: execfile(r"tmp_MODELcmd.py")'
    #         sendCommand(r"""print(r'{}')""".format(msg))
    #         raise RuntimeError(str(e) + '\n' + msg)
    #     self.deactivateIfNeeded()
    #     return TRUE
