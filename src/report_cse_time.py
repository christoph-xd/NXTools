import json
import math
from pathlib import Path

import NXOpen
import NXOpen.CAM
import NXOpen.UF

from utils import Checks, Getters, UI, lw

# import NXOpen.Utilities


class ReportCSETime:
    def __init__(self, isDebug: bool) -> None:
        self.theSession = NXOpen.Session.GetSession()
        self.theUfSession = NXOpen.UF.UFSession.GetUFSession()
        self.theUI = NXOpen.UI.GetUI()
        self.workPart = self.theSession.Parts.Work
        self.operationTimes = []
        self.isDebug = isDebug
        if self.isDebug:
            self.theUI.NXMessageBox.Show("Debug Mode", NXOpen.NXMessageBox.DialogType.Information, str(
                "The Debug Mode is switched one!"))

    def report_time(self):

        if not Checks.check_workpart(self.workPart):
            return

        if not Checks.check_setup():
            return

        num = self.theUI.SelectionManager.GetNumSelectedObjects()
        objects1 = [NXOpen.CAM.CAMObject.Null] * num

        if num == 0:
            message = [str] * 1
            message[0] = "Ok to Calculate Machining Time?"
            if UI.ask_yes_no("Calculate Machining Time", message) == 1:
                self.workPart.CAMSetup.CalculateMachiningTimes()

            rootGroup = self.workPart.CAMSetup.GetRoot(
                NXOpen.CAM.CAMSetup.View.ProgramOrder)
            objects_at_start = NXOpen.CAM.NCGroup.GetMembers(rootGroup)
            self.parsing_opration(objects_at_start)
        else:
            for i in range(num):
                objects1[i] = self.theUI.SelectionManager.GetSelectedTaggedObject(
                    i)
                #self.operationTimes.append(self.get_cse_time(objects1[i]))
            self.parsing_opration(objects1)

        for i, operationTime in enumerate(self.operationTimes):
            lw("\n***************************************************")
            lw(f"{i+1}. Operation Name: {operationTime['operationName']}")
            lw(f"       Material Cutting Time   : { operationTime['cseMaterialCuttingTime']}")
            lw(f"       Air Cutting Time        : { operationTime['cseAirCuttingTime']}")
            lw(f"       Positioning Mixed Time  : { operationTime['csePositioningMixedTime']}")
            lw(f"       Dragging Time           : { operationTime['cseDraggingTime']}")
            lw(f"       Delay Time              : { operationTime['cseDelayTime']}")
            lw(f"       Wait Time               : { operationTime['cseWaitTime']}")
            lw(f"       ToolChange Time         : { operationTime['cseToolChangeTime']}")
            lw(f"       Positioning Linear Time : { operationTime['csePositioningLinearTime']}")
            lw(f"       Positioning Rotary Time : { operationTime['csePositioningRotaryTime']}")
            lw("***************************************************")
        return

    def parsing_opration(self, obj):

        for object in obj:
            if not object.Name == 'NONE':
                if self.workPart.CAMSetup.IsGroup(object):
                    self.parsing_opration(
                        NXOpen.CAM.NCGroup.GetMembers(object))
                elif self.workPart.CAMSetup.IsOperation(object):
                    self.operationTimes.append(self.get_cse_time(object))
        return

    def get_cse_time(self, operation):

        cseTime = {}

        cseTime["operationName"] = operation.Name
        cseTime["cseMaterialCuttingTime"] = self.convertTime(
            self.theUfSession.Param.AskDoubleValue(operation.Tag, 10250))
        cseTime["cseAirCuttingTime"] = self.convertTime(
            self.theUfSession.Param.AskDoubleValue(operation.Tag, 10251))
        cseTime["csePositioningMixedTime"] = self.cseAirCuttingTime = self.convertTime(
            self.theUfSession.Param.AskDoubleValue(operation.Tag, 10252))
        cseTime["cseDraggingTime"] = self.cseAirCuttingTime = self.convertTime(
            self.theUfSession.Param.AskDoubleValue(operation.Tag, 10253))
        cseTime["cseDelayTime"] = self.cseAirCuttingTime = self.convertTime(
            self.theUfSession.Param.AskDoubleValue(operation.Tag, 10254))
        cseTime["cseWaitTime"] = self.cseAirCuttingTime = self.convertTime(
            self.theUfSession.Param.AskDoubleValue(operation.Tag, 10255))
        cseTime["cseToolChangeTime"] = self.cseAirCuttingTime = self.convertTime(
            self.theUfSession.Param.AskDoubleValue(operation.Tag, 10256))
        cseTime["csePositioningLinearTime"] = self.cseAirCuttingTime = self.convertTime(
            self.theUfSession.Param.AskDoubleValue(operation.Tag, 10257))
        cseTime["csePositioningRotaryTime"] = self.cseAirCuttingTime = self.convertTime(
            self.theUfSession.Param.AskDoubleValue(operation.Tag, 10258))

        return cseTime

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
    isDebug = True
    config_file = Path(__file__).parent
    with open(f'{config_file}/config.json', 'r') as f:
        config = json.load(f)
        report_json = config['report_cse_time']
        lic = config['license']
    if Checks.check_nx_version(int(report_json['version_max']), int(report_json['version_min'])):
        if Checks.check_lic(lic, isDebug=False):
            instance = ReportCSETime(isDebug)
            instance.report_time()
