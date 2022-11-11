import base64
from datetime import datetime

import NXOpen
import NXOpen.UF


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
    theSession = NXOpen.Session.GetSession()

    @classmethod
    def check_lic(cls, lic: str, isDebug: bool = False) -> bool:
        """Check if a valid License Key is given.

        Args:
            lic (str): License Key
            isDebug (bool, optional): Switch on the Debug Mode. Defaults to False.

        Returns:
            bool: True for a valid License is given.
        """
        license = lic.encode('ascii')
        license = base64.b64decode(license)
        license = license.decode('ascii')

        lic_date = license.split('-')
        # date_now = str(datetime.date(datetime.now())).split('-')
        lic_date = datetime.date(datetime(int(lic_date[0]), int(
            lic_date[1]), int(lic_date[2])))
        # date_now = datetime.date(datetime(int(date_now[0]), int(
        #     date_now[1]), int(date_now[2])))
        if isDebug:
            lw(lic)
            lw(license)
            lw(lic_date)

        if datetime.date(datetime.now()) > lic_date:
            cls.theUI.NXMessageBox.Show(
                "License Check", NXOpen.NXMessageBox.DialogType.Error, "The Licens is not valid anymore. \nPlease request a new one!")
            return False
        return True

    @classmethod
    def check_nx_version(cls, highV: int, lowV: int) -> bool:
        """Check if the given Version of fit to the current Version. 


        Args:
            highV (int): the latest Version of NX
            lowV (int): th oldest Verson of NX

        Returns:
            bool: retruns of NX is in the range of the Versions
        """
        UGRelease = cls.theSession.GetEnvironmentVariableValue(
            "NX_COMPATIBLE_BASE_RELEASE_VERSION")
        UGRelease = int(str(UGRelease).replace('v', ''))
        if UGRelease > highV or UGRelease < lowV:
            cls.theUI.NXMessageBox.Show(
                "Version Check", NXOpen.NXMessageBox.DialogType.Error, "The current NX Version don't match to required Version.")
            return False
        return True

    @classmethod
    def check_workpart(cls, workPart: NXOpen.Part) -> bool:
        """Check if a Parrt is loaded

        Args:
            workPart: _description_

        Returns:
            bool: True for Part is open 
        """
        if workPart is None:
            cls.theUI.NXMessageBox.Show(
                "Part", NXOpen.NXMessageBox.DialogType.Error, "A Part must be Opened.")
            return False
        return True

    @classmethod
    def check_setup(cls) -> bool:
        """Check if the work part have an setup.

        Returns:
            bool: True for a Setup Exist in the WorkPart
        """
        cls.theUfSession.Cam.InitSession()
        setupTag = cls.theUfSession.Setup.AskSetup()
        if setupTag == 0:
            cls.theUI.NXMessageBox.Show("CamSetup", NXOpen.NXMessageBox.DialogType.Information, str(
                "No CamSetup in this Part."))
            return False
        return True
