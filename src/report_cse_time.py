import json
import math
from pathlib import Path

import NXOpen
import NXOpen.CAM
import NXOpen.UF

from utils import Checks, Getters, lw

# import NXOpen.Utilities


class ReportCSETime:
    def __init__(self) -> None:
        self.theSession = NXOpen.Session.GetSession()
        self.theUfSession = NXOpen.UF.UFSession.GetUFSession()
        self.theUI = NXOpen.UI.GetUI()

    def report_time(self):
        workPart = self.theSession.Parts.Work

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

        for i in range(num):
            objects1[i] = self.theUI.SelectionManager.GetSelectedTaggedObject(
                i)
            operation = objects1[i]

            cseMaterialCuttingTime = self.theUfSession.Param.AskDoubleValue(
                operation.Tag, 10250)
            cseAirCuttingTime = self.theUfSession.Param.AskDoubleValue(
                operation.Tag, 10251)
            csePositioningMixedTime = self.theUfSession.Param.AskDoubleValue(
                operation.Tag, 10252)
            cseDraggingTime = self.theUfSession.Param.AskDoubleValue(
                operation.Tag, 10253)
            cseDelayTime = self.theUfSession.Param.AskDoubleValue(
                operation.Tag, 10254)
            cseWaitTime = self.theUfSession.Param.AskDoubleValue(
                operation.Tag, 10255)
            cseToolChangeTime = self.theUfSession.Param.AskDoubleValue(
                operation.Tag, 10256)
            csePositioningLinearTime = self.theUfSession.Param.AskDoubleValue(
                operation.Tag, 10257)
            csePositioningRotaryTime = self.theUfSession.Param.AskDoubleValue(
                operation.Tag, 10258)
            lw(self.convertTime(cseMaterialCuttingTime))
            lw(self.convertTime(cseAirCuttingTime))

    def convertTime(self, time_to_convert):
        try:
            hours = math.floor(time_to_convert / 60.0)
            minutes = math.floor(
                (time_to_convert / 60.0 - math.floor(hours)) * 60.0)
            seconds = math.floor(
                ((time_to_convert / 60.0 - math.floor(hours)) * 60.0 - math.floor(minutes)) * 60.0)
            machTime = str(hours).zfill(2) + ":" + \
                str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
        except Exception as e:
            lw(f"Unable to Convert Time. Error : {e}")
            machTime = "00:00:00"
        return machTime


if __name__ == '__main__':
    config_file = Path(__file__).parent
    with open(f'{config_file}/config.json', 'r') as f:
        config = json.load(f)
        report_json = config['report_cse_time']
        lic = config['license']
    if Checks.check_nx_version(int(report_json['version_max']), int(report_json['version_min'])):
        if Checks.check_lic(lic, isDebug=False):
            instance = ReportCSETime()
            instance.report_time()
