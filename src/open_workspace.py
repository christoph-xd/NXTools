import os
import json
from pathlib import Path
import NXOpen

from utils import Checks


class OpenWorkSpace:
    def __init__(self, lic: str, isDebug: bool = False) -> None:
        self.theUI = NXOpen.UI.GetUI()
        self.theSession = NXOpen.Session.GetSession()
        self.isDebug = isDebug
        self.lic = lic

        if self.isDebug:
            self.theUI.NXMessageBox.Show("Debug Mode", NXOpen.NXMessageBox.DialogType.Information, str(
                "The Debug Mode is switched one!"))

    def open(self):
        workPart = self.theSession.Parts.Work
        if not Checks.check_workpart(workPart):
            return
        full_path = self.theSession.Parts.Work.FullPath
        pathname = os.path.dirname(full_path)
        os.startfile(pathname)


if __name__ == '__main__':
    isDebug = False
    config_file = Path(__file__).parent

    with open(f'{config_file}/config.json', 'r') as f:
        config = json.load(f)
        workspace_json = config['open_workspace']
        lic = config['license']

    if Checks.check_nx_version(int(workspace_json['version_max']), int(workspace_json['version_min'])):
        if Checks.check_lic(lic, isDebug):
            instance = OpenWorkSpace(lic, isDebug)
            instance.open()
