import math
import NXOpen
import NXOpen.Gateway
import NXOpen.CAM
import NXOpen.UF
from utils import Checks, Getters
from utils import lw


class ReportCuttingLength:
    def __init__(self, isDebug: bool) -> None:
        self.theSession = NXOpen.Session.GetSession()
        self.theUfSession = NXOpen.UF.UFSession.GetUFSession()
        self.theUI = NXOpen.UI.GetUI()
        self.isDebug = isDebug

        if isDebug:
            self.theUI.NXMessageBox.Show("Debug Mode", NXOpen.NXMessageBox.DialogType.Information, str(
                "The Debug Mode is switched one!"))

    # def lw(self, output: str):
    #     """
    #     Write a line in the NX Listing Window
    #     Args:
    #         output   : The Output which will shown
    #     """
    #     if not self.theSession.ListingWindow.IsOpen:
    #         self.theSession.ListingWindow.Open()
    #     else:
    #         pass

    #     self.theSession.ListingWindow.WriteFullline(str(output))

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
            objects1[i] = self.theUI.SelectionManager.GetSelectedTaggedObject(
                i)
            object = objects1[i]
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
                    f"G1 Length / Time       :  {operation_info['g1']}{unit} / {operation_info['g1_time']}sec")
                lw(
                    f"G0 Length / Time       :  {operation_info['g0']}{unit} / {operation_info['g0_time']}sec")
                lw("***************************************************")


if __name__ == '__main__':
    isDebug = True
    report = ReportCuttingLength(isDebug)
    report.main()
