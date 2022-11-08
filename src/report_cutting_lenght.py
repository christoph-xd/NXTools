import math
import NXOpen
import NXOpen.Gateway
import NXOpen.CAM
import NXOpen.UF


class ReportCuttingLength:
    def __init__(self, isDebug: bool) -> None:
        self.theSession = NXOpen.Session.GetSession()
        self.theUfSession = NXOpen.UF.UFSession.GetUFSession()
        self.theUI = NXOpen.UI.GetUI()
        self.isDebug = isDebug

        if isDebug:
            self.theUI.NXMessageBox.Show("Debug Mode", NXOpen.NXMessageBox.DialogType.Information, str(
                "The Debug Mode is switched one!"))

    def get_base_unit(self, workPart: NXOpen.Part) -> str:
        """
        Retrun the Unit of the active part
        Args:
            workPart : The workPart Object
        """
        unitCollection = workPart.UnitCollection
        baseUnit = unitCollection.GetBase("Length")
        unitsMM = ["MilliMeter", "Meter", "CentiMeter"]

        if baseUnit.Name in unitsMM:
            return "mm"
        else:
            return "inch"

    def get_tool_information(self, object) -> dict:
        """
        Get some Information for the tool
        Args:
            object  : The Cam object from the operation
        """
        tool = object.GetParent(NXOpen.CAM.CAMSetup.View.MachineTool)

        tool_info = {
            "name": tool.Name,
        }

        if self.isDebug:
            self.lw(tool_info)

        return tool_info

    def get_operation_information(self, object) -> dict:
        """Retruns the G1 Length, G0 Length and Operation Name

        Args:
            object (_type_): The Cam Operation Object

        Returns:
            dict: _description_
        """
        g1_len = round(object.GetToolpathCuttingLength())
        g0_len = round(object.GetToolpathLength() -
                       object.GetToolpathCuttingLength())
        g1_time = round(object.GetToolpathCuttingTime()*60)
        g0_time = round((object.GetToolpathTime() -
                        object.GetToolpathCuttingTime())*60)

        operation_info = {
            "name": object.Name,
            "g1": g1_len,
            "g1_time": g1_time,
            "g0": g0_len,
            "g0_time": g0_time,
        }

        if self.isDebug:
            self.lw(operation_info)

        return operation_info

    def lw(self, output: str):
        """
        Write a line in the NX Listing Window
        Args:
            output   : The Output which will shown
        """
        if not self.theSession.ListingWindow.IsOpen:
            self.theSession.ListingWindow.Open()
        else:
            pass

        self.theSession.ListingWindow.WriteFullline(str(output))

    def ask_workpart(self, workPart: NXOpen.Part) -> bool:
        """Check if a Parrt is loaded

        Args:
            workPart: _description_

        Returns:
            bool: True for Part is open 
        """
        if workPart is None:
            self.theUI.NXMessageBox.Show(
                "Part", NXOpen.NXMessageBox.DialogType.Error, "A Part must be Opened.")
            return False
        return True

    def ask_setup(self) -> bool:
        """Check if the work part have an setup.

        Returns:
            bool: True for a Setup Exist in the WorkPart
        """
        self.theUfSession.Cam.InitSession()
        setupTag = self.theUfSession.Setup.AskSetup()
        if setupTag == 0:
            self.theUI.NXMessageBox.Show("CamSetup", NXOpen.NXMessageBox.DialogType.Information, str(
                "No CamSetup in this Part."))
            return False
        return True

    def main(self):
        workPart = self.theSession.Parts.Work

        if self.isDebug:
            self.lw(type(workPart))

        if not self.ask_workpart(workPart):
            return

        if not self.ask_setup():
            return

        num = self.theUI.SelectionManager.GetNumSelectedObjects()
        objects1 = [NXOpen.CAM.CAMObject.Null] * num

        if num == 0:
            self.theUI.NXMessageBox.Show("Object", NXOpen.NXMessageBox.DialogType.Information, str(
                "One Object must be Selected in the ONT."))
            return

        unit = self. get_base_unit(workPart)

        for i in range(num):
            objects1[i] = self.theUI.SelectionManager.GetSelectedTaggedObject(
                i)
            object = objects1[i]
            if workPart.CAMSetup.IsOperation(object):
                tool_info = self.get_tool_information(object)
                operation_info = self.get_operation_information(object)
                self.lw("\n***************************************************")
                self.lw(f"Operation Name         :  {operation_info['name']}")
                self.lw(f"Tool Name              :  {tool_info['name']}")
                self.lw(
                    f"G1 Length / Time       :  {operation_info['g1']}{unit} / {operation_info['g1_time']}sec")
                self.lw(
                    f"G0 Length / Time       :  {operation_info['g0']}{unit} / {operation_info['g0_time']}sec")
                self.lw("***************************************************")


if __name__ == '__main__':
    isDebug = True
    report = ReportCuttingLength(isDebug)
    report.main()
