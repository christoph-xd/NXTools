#############################################################################
#
#   Delete all Ude's in the CAM Session
#
#   Written by: Chrsitoph Brandau
##############################################################################
import NXOpen
import NXOpen.UF
import NXOpen.CAM
from utils import UI, lw, Checks
from utils.basic import BasicFunctions as BF
from locale.language_package import DeleteAllUDE as Text
import json
from pathlib import Path


class DelAllUde:
    def __init__(self) -> None:
        self.theSession = NXOpen.Session.GetSession()
        self.theUfSession = NXOpen.UF.UFSession.GetUFSession()
        self.workPart = self.theSession.Parts.Work
        self.theUI = NXOpen.UI.GetUI()

    def main(self):
        response = UI.ask_yes_no(BF.get_text(Text.AskYesNoHeader), [
                                 BF.get_text(Text.AskYesNo)])
        if response == 2:
            UI.user_abort()
            return
        AllUdeTyps = [
            NXOpen.UF.Ude.SetType.ValueOf(0),
            NXOpen.UF.Ude.SetType.ValueOf(1),
            NXOpen.UF.Ude.SetType.ValueOf(3),
        ]
        AllViews = [
            self.workPart.CAMSetup.GetRoot(
                NXOpen.CAM.CAMSetup.View.ProgramOrder),
            self.workPart.CAMSetup.GetRoot(
                NXOpen.CAM.CAMSetup.View.MachineTool),
            self.workPart.CAMSetup.GetRoot(
                NXOpen.CAM.CAMSetup.View.MachineMethod),
            self.workPart.CAMSetup.GetRoot(NXOpen.CAM.CAMSetup.View.Geometry),
        ]

        for UdeType in AllUdeTyps:
            for View in AllViews:
                objects_in_view = NXOpen.CAM.NCGroup.GetMembers(View)
                self.pars_view(objects_in_view, UdeType)

    def deleteude(self, tagged: NXOpen.CAM.Operation, UdeType):
        self.theUfSession.Param.DeleteAllUdes(tagged.Tag, UdeType)

    def pars_view(self, view, UdeType):
        for tagged in view:
            if not tagged == "NONE":
                if self.workPart.CAMSetup.IsGroup(tagged):
                    group = NXOpen.CAM.NCGroup.GetMembers(tagged)
                    self.deleteude(tagged, UdeType)
                    self.pars_view(group, UdeType)
                else:
                    self.deleteude(tagged, UdeType)


if __name__ == "__main__":
    config_file = Path(__file__).parent

    with open(f"{config_file}/config.json", "r") as f:
        config = json.load(f)
        versions = config["del_all_ude"]
        if Checks.check_nx_version(int(versions["version_max"]), int(versions["version_min"])):
            instance = DelAllUde()
            instance.main()
