import json
import NXOpen
import NXOpen.CAM
from ui import RenumberToolUi
from utils import UI, Checks
from utils import BasicFunctions as BF
from locale.language_package import RenumberToolLocale as Text
from pathlib import Path

class RenumberTool:
    def __init__(self) -> None:
        
        self.theSession = NXOpen.Session.GetSession()
        self.theUfSession = NXOpen.UF.UFSession.GetUFSession()
        self.workPart = self.theSession.Parts.Work
        self.theUI = NXOpen.UI.GetUI()
        
                
        self.therenumber_tool = None
        try:
            self.therenumber_tool =  RenumberToolUi.renumber_tool()
            self.therenumber_tool.Show()
            self.toolNumber = self.therenumber_tool.toolNumber
        except Exception as ex:
        # ---- Enter your exception handling code here -----
            NXOpen.UI.GetUI().NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))
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
    config_file = Path(__file__).parent
    with open(f"{config_file}/config.json", "r") as f:
        config = json.load(f)
        versions = config["renumber_tools"]
    if Checks.check_nx_version(int(versions["version_max"]), int(versions["version_min"])):
        instance = RenumberTool()
        instance.main()
