import NXOpen


def lw(output: str):
    """
    Write a line in the NX Listing Window
    Args:
        output   : The Output which will shown
    """
    theSession = NXOpen.Session.GetSession()
    if not theSession.ListingWindow.IsOpen:
        theSession.ListingWindow.Open()
    else:
        pass

    theSession.ListingWindow.WriteFullline(str(output))


class Getters:
    @classmethod
    def get_base_unit(cls, workPart: NXOpen.Part) -> str:
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

    @classmethod
    def get_tool_information(cls, object) -> dict:
        """
        Get some Information for the tool
        Args:
            object  : The Cam object from the operation
        """
        tool = object.GetParent(NXOpen.CAM.CAMSetup.View.MachineTool)

        tool_info = {
            "name": tool.Name,
        }

        return tool_info

    @classmethod
    def get_operation_information(cls, object) -> dict:
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

        return operation_info


class Checks:
    theUI = NXOpen.UI.GetUI()
    theUfSession = NXOpen.UF.UFSession.GetUFSession()

    @classmethod
    def check_workpart(cls, workPart: NXOpen.Part) -> bool:
        """Check if a Parrt is loaded

        Args:
            workPart: _description_

        Returns:
            bool: True for Part is open 
        """
        if workPart is None:
            Checks.theUI.NXMessageBox.Show(
                "Part", NXOpen.NXMessageBox.DialogType.Error, "A Part must be Opened.")
            return False
        return True

    @staticmethod
    def check_setup() -> bool:
        """Check if the work part have an setup.

        Returns:
            bool: True for a Setup Exist in the WorkPart
        """
        Checks.theUfSession.Cam.InitSession()
        setupTag = Checks.theUfSession.Setup.AskSetup()
        if setupTag == 0:
            Checks.theUI.NXMessageBox.Show("CamSetup", NXOpen.NXMessageBox.DialogType.Information, str(
                "No CamSetup in this Part."))
            return False
        return True
