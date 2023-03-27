import json
from pathlib import Path
import NXOpen
import NXOpen.CAM
import NXOpen.Gateway
from utils import BasicFunctions as BF
from locale.language_package import ReportCuttingLengthLocale as Text
from utils import Checks, Getters, lw


class ReportCuttingLength:
    def __init__(self, isDebug: bool) -> None:
        self.theSession = NXOpen.Session.GetSession()
        self.theUfSession = NXOpen.UF.UFSession.GetUFSession()
        self.theUI = NXOpen.UI.GetUI()
        self.workPart = self.theSession.Parts.Work
        self.isDebug = isDebug

        if self.isDebug:
            self.theUI.NXMessageBox.Show(
                "Debug Mode",
                NXOpen.NXMessageBox.DialogType.Information,
                str("The Debug Mode is switched one!"),
            )
        self.checkWork = True
        self.checkSetup = True

        if not Checks.check_workpart(self.workPart):
            self.checkWork = False
        if not Checks.check_setup():
            self.checkSetup = False

    def main(self):
        count, toolTag = self.theUfSession.UiOnt.AskSelectedNodes()

        if self.isDebug:
            lw(type(self.workPart))

        objects1 = [NXOpen.CAM.CAMObject.Null] * count

        if count == 0:
            self.theUI.NXMessageBox.Show(
                "Object",
                NXOpen.NXMessageBox.DialogType.Information,
                BF.get_text(Text.selectONT),
            )
            return

        unit = Getters.get_base_unit(self.workPart)

        for i in range(count):
            if self.isDebug:
                lw(objects1)
            objects1[i] = NXOpen.TaggedObjectManager.GetTaggedObject(toolTag[i])
            object = objects1[i]

            if self.isDebug:
                lw(type(object))

            if self.workPart.CAMSetup.IsOperation(object):
                tool_info = Getters.get_tool_information(object)
                if self.isDebug:
                    lw(tool_info)
                operation_info = Getters.get_operation_information(object)
                if self.isDebug:
                    lw(operation_info)
                lw("\n***************************************************")
                lw(
                    f"{BF.get_text(Text.operationName)}\t\t\t:  {operation_info['name']}"
                )
                lw(f"{BF.get_text(Text.toolName)}\t\t\t:  {tool_info['name']}")
                lw(
                    f"{BF.get_text(Text.lengthCut)}\t\t:  {operation_info['g1']} / {operation_info['g1_time']}sec"
                )
                lw(
                    f"{BF.get_text(Text.lengthRapid)}\t\t:  {operation_info['g0']} / {operation_info['g0_time']}sec"
                )
                lw("***************************************************")


if __name__ == "__main__":
    isDebug = False
    config_file = Path(__file__).parent
    with open(f"{config_file}/config.json", "r") as f:
        config = json.load(f)
        versions = config["report_cutting_length"]
    if Checks.check_nx_version(
        int(versions["version_max"]), int(versions["version_min"])
    ):
        report = ReportCuttingLength(isDebug)
        report.main()
