import json
from locale.language_package import RenumberToolLocale as Text
from pathlib import Path

import NXOpen
import NXOpen.CAM

from ui import RenumberToolUi
from utils import UI
from utils import BasicFunctions as BF
from utils import Checks


class RenumberTool:
    def __init__(self) -> None:
        self.theSession = NXOpen.Session.GetSession()
        self.theUfSession = NXOpen.UF.UFSession.GetUFSession()
        self.workPart = self.theSession.Parts.Work
        self.theUI = NXOpen.UI.GetUI()

        self.therenumber_tool = None
        try:
            self.therenumber_tool = RenumberToolUi.renumber_tool()
            self.therenumber_tool.Show()
            self.toolNumber = self.therenumber_tool.toolNumber
        except Exception as ex:
            # ---- Enter your exception handling code here -----
            NXOpen.UI.GetUI().NXMessageBox.Show(
                "Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex)
            )
        finally:
            if self.therenumber_tool != None:
                self.therenumber_tool.Dispose()
                self.therenumber_tool = None

    def main(self):
        if self.toolNumber == None:
            UI.user_abort()
            return
        for item in self.workPart.CAMSetup.CAMGroupCollection:
            if type(item) == NXOpen.CAM.Tool:
                self.theUfSession.Param.SetIntValue(item.Tag, 1038, self.toolNumber)
                self.toolNumber += 1


if __name__ == "__main__":
    instance = RenumberTool()
    instance.main()
