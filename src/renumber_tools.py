import NXOpen
import NXOpen.CAM
from ui import RenumberToolUi
from utils import UI
from utils import BasicFunctions as BF
from locale.language_package import RenumberToolLocale as Text 


class RenumberTool:
    def __init__(self) -> None:
        self.toolNumber = RenumberToolUi.main()
        self.theSession = NXOpen.Session.GetSession()
        self.theUfSession = NXOpen.UF.UFSession.GetUFSession()
        self.workPart = self.theSession.Parts.Work
        self.theUI = NXOpen.UI.GetUI()

    def main(self):
        if self.toolNumber == None:
            UI.user_abort()
            return
        BF.set_undo_mark(BF.get_text(Text.undoMark), self.theSession)
        for item in self.workPart.CAMSetup.CAMGroupCollection:
            if type(item) == NXOpen.CAM.Tool:
                self.theUfSession.Param.SetIntValue(item.Tag, 1038, self.toolNumber)
                self.toolNumber += 1


if __name__ == "__main__":
    instance = RenumberTool()
    instance.main()
