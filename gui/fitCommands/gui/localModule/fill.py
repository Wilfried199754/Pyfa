import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.localAdd import CalcAddLocalModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory, ModuleInfo
from service.fit import Fit


class GuiFillWithLocalModulesCommand(wx.Command):

    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, 'Fill with Local Modules')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID

    def Do(self):
        added_modules = 0
        while True:
            cmd = CalcAddLocalModuleCommand(fitID=self.fitID, newModInfo=ModuleInfo(itemID=self.itemID), commit=False)
            if not self.internalHistory.submit(cmd):
                break
            added_modules += 1
        eos.db.commit()
        Fit.getInstance().recalc(self.fitID)
        success = added_modules > 0
        wx.PostEvent(
            gui.mainFrame.MainFrame.getInstance(),
            GE.FitChanged(fitID=self.fitID, action='modadd', typeID=self.itemID) if success else GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.commit()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(
            gui.mainFrame.MainFrame.getInstance(),
            GE.FitChanged(fitID=self.fitID, action='moddel', typeID=self.itemID) if success else GE.FitChanged(fitID=self.fitID))
        return success
