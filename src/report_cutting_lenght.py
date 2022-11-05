import math
import NXOpen
import NXOpen.Gateway
import NXOpen.CAM
import NXOpen.UF


theSession = NXOpen.Session.GetSession()
theUfSession = NXOpen.UF.UFSession.GetUFSession()
theUI = NXOpen.UI.GetUI()
isDebug = False


def get_base_unit(workPart) -> str:
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


def get_tool_information(object) -> dict:
    """
    Get some Information for the tool
    Args:
        object  : The Cam object from the operation
    """
    tool = object.GetParent(NXOpen.CAM.CAMSetup.View.MachineTool)

    tool_info = {
        "name": tool.Name,
    }

    if isDebug:
        lw(tool_info)

    return tool_info


def get_operation_information(object) -> dict:
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

    if isDebug:
        lw(operation_info)

    return operation_info


def lw(output: str):
    """
    Write a line in the NX Listing Window
    Args:
        output   : The Output which will shown
    """
    if not theSession.ListingWindow.IsOpen:
        theSession.ListingWindow.Open()
    else:
        pass

    theSession.ListingWindow.WriteFullline(str(output))


def ask_workpart(workPart) -> bool:
    """Check if a Parrt is loaded

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


def ask_setup() -> bool:
    """Check if the work part have an setup.

    Returns:
        bool: True for a Setup Exist in the WorkPart
    """
    theUfSession.Cam.InitSession()
    setupTag = theUfSession.Setup.AskSetup()
    if setupTag == 0:
        theUI.NXMessageBox.Show("CamSetup", NXOpen.NXMessageBox.DialogType.Information, str(
            "No CamSetup in this Part."))
        return False
    return True


def main():
    workPart = theSession.Parts.Work

    if not ask_workpart(workPart):
        return

    if not ask_setup():
        return

    num = theUI.SelectionManager.GetNumSelectedObjects()
    objects1 = [NXOpen.CAM.CAMObject.Null] * num

    if num == 0:
        theUI.NXMessageBox.Show("Object", NXOpen.NXMessageBox.DialogType.Information, str(
            "One Object must be Selected in the ONT."))
        return

    unit = get_base_unit(workPart)

    for i in range(num):
        objects1[i] = theUI.SelectionManager.GetSelectedTaggedObject(i)
        object = objects1[i]
        if workPart.CAMSetup.IsOperation(object):
            tool_info = get_tool_information(object)
            operation_info = get_operation_information(object)
            lw("\n***************************************************")
            lw(f"Operation Name         :  {operation_info['name']}")
            lw(f"Tool Name              :  {tool_info['name']}")
            lw(f"G1 Length / Time       :  {operation_info['g1']}{unit} / {operation_info['g1_time']}sec")
            lw(f"G0 Length / Time       :  {operation_info['g0']}{unit} / {operation_info['g0_time']}sec")
            lw("***************************************************")


if __name__ == '__main__':
    if isDebug:
        theUI.NXMessageBox.Show("Debug Mode", NXOpen.NXMessageBox.DialogType.Information, str(
            "The Debug Mode is switched one!"))
    main()
