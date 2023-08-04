import json
import os
from pathlib import Path

import NXOpen

from utils import Checks


class OpenWorkSpace:
    def __init__(self, isDebug: bool = False) -> None:
        self.theUI = NXOpen.UI.GetUI()
        self.theSession = NXOpen.Session.GetSession()
        self.isDebug = isDebug

        if self.isDebug:
            self.theUI.NXMessageBox.Show(
                "Debug Mode",
                NXOpen.NXMessageBox.DialogType.Information,
                str("The Debug Mode is switched one!"),
            )

    def open(self):
        workPart = self.theSession.Parts.Work
        if not Checks.check_workpart(workPart):
            return
        full_path = self.theSession.Parts.Work.FullPath
        pathname = os.path.dirname(full_path)
        os.startfile(pathname)


if __name__ == "__main__":
    isDebug = False
    instance = OpenWorkSpace(isDebug)
    instance.open()
