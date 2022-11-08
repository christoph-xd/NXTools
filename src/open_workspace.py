import NXOpen
from utils import Checks
import os


class OpenWorkSpace:
    def __init__(self) -> None:
        self.theUI = NXOpen.UI.GetUI()
        self.theSession = NXOpen.Session.GetSession()

    def open(self):
        workPart = self.theSession.Parts.Work
        if not Checks.check_workpart(workPart):
            return
        full_path = self.theSession.Parts.Work.FullPath
        pathname = os.path.dirname(full_path)
        os.startfile(pathname)


if __name__ == '__main__':
    instance = OpenWorkSpace()
    instance.open()
