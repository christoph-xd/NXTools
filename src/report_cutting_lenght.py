import json
from pathlib import Path
import NXOpen
import NXOpen.CAM
import NXOpen.Gateway

from utils import Checks, Getters, lw


class ReportCuttingLength:
    def __init__(self, isDebug: bool) -> None:
        self.theSession = NXOpen.Session.GetSession()
        self.theUI = NXOpen.UI.GetUI()
        self.isDebug = isDebug

        if self.isDebug:
            self.theUI.NXMessageBox.Show("Debug Mode", NXOpen.NXMessageBox.DialogType.Information, str(
                "The Debug Mode is switched one!"))

    def main(self):
        workPart = self.theSession.Parts.Work

        if self.isDebug:
            lw(type(workPart))

        if not Checks.check_workpart(workPart):
            return

        if not Checks.check_setup():
            return

        num = self.theUI.SelectionManager.GetNumSelectedObjects()
        objects1 = [NXOpen.CAM.CAMObject.Null] * num

        if num == 0:
            self.theUI.NXMessageBox.Show("Object", NXOpen.NXMessageBox.DialogType.Information, str(
                "One Object must be Selected in the ONT."))
            return

        unit = Getters.get_base_unit(workPart)

        for i in range(num):
            if self.isDebug:
                lw(objects1)
            objects1[i] = self.theUI.SelectionManager.GetSelectedTaggedObject(
                i)
            object = objects1[i]

            if self.isDebug:
                lw(type(object))

            if workPart.CAMSetup.IsOperation(object):
                tool_info = Getters.get_tool_information(object)
                if self.isDebug:
                    lw(tool_info)
                operation_info = Getters.get_operation_information(object)
                if self.isDebug:
                    lw(operation_info)
                lw("\n***************************************************")
                lw(f"Operation Name         :  {operation_info['name']}")
                lw(f"Tool Name              :  {tool_info['name']}")
                lw(
                    f"G1 Length / Time       :  {operation_info['g1']} / {operation_info['g1_time']}sec")
                lw(
                    f"G0 Length / Time       :  {operation_info['g0']} / {operation_info['g0_time']}sec")
                lw("***************************************************")


if __name__ == '__main__':
    isDebug = False
    config_file = Path(__file__).parent
    with open(f'{config_file}/config.json', 'r') as f:
        config = json.load(f)
        versions = config['report_cutting_length']
    if Checks.check_nx_version(int(versions['version_max']), int(versions['version_min'])):
        report = ReportCuttingLength(isDebug)
        report.main()
