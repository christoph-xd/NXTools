import math
import NXOpen
import shutil
import os
import getpass
import time
import subprocess

theUI = NXOpen.UI.GetUI()
theSession = NXOpen.Session.GetSession()


def ask_workpart(workPart) -> bool:
    """_summary_

    Args:
        workPart: _description_

    Returns:
        bool: True for Part is open 
    """
    if workPart is None:
        theUI.NXMessageBox.Show(
            "Part", NXOpen.NXMessageBox.DialogType.Error, "A Part must be Opened.")
        return False
    return True


def main():

    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display

    if not ask_workpart(workPart):
        return

    full_path = theSession.Parts.Work.FullPath
    partname = os.path.basename(full_path)
    pathname = os.path.dirname(full_path)

    os.startfile(pathname)


if __name__ == '__main__':
    main()
