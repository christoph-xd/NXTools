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
from locale.ude_package import UdeName
from ui import DelUdeUi

class DelAllUde:
    def __init__(self) -> None:
        self.theSession = NXOpen.Session.GetSession()
        self.theUfSession = NXOpen.UF.UFSession.GetUFSession()
        self.workPart = self.theSession.Parts.Work
        self.theUI = NXOpen.UI.GetUI()
        
        
        self.thedel_ude = None
        try:
            self.thedel_ude =  DelUdeUi.del_ude()
            self.thedel_ude.Show()
            self.views = self.thedel_ude.views
            lw("hier")
            lw(len(self.views))
        except Exception as ex:
            NXOpen.UI.GetUI().NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))
        finally:
            if self.thedel_ude != None:
                self.thedel_ude.Dispose()
                self.thedel_ude = None
        
    def main(self):
        # AllViews = []
        # if not Checks.check_workpart(self.workPart):
        #     return
        # if not Checks.check_setup():
        #     return

        # response = UI.ask_yes_no(
        #     BF.get_text(Text.AskDelProgrammViewHeader),
        #     [BF.get_text(Text.AskDelProgrammView)],
        # )
        # if response == 1:
        #     AllViews.append(
        #         self.workPart.CAMSetup.GetRoot(NXOpen.CAM.CAMSetup.View.ProgramOrder)
        #     )

        # response = UI.ask_yes_no(
        #     BF.get_text(Text.AskDelToolViewHeader),
        #     [BF.get_text(Text.AskDelToolView)],
        # )
        # if response == 1:
        #     AllViews.append(
        #         self.workPart.CAMSetup.GetRoot(NXOpen.CAM.CAMSetup.View.MachineTool)
        #     )

        # response = UI.ask_yes_no(
        #     BF.get_text(Text.AskDelGeoViewHeader),
        #     [BF.get_text(Text.AskDelGeoView)],
        # )
        # if response == 1:
        #     AllViews.append(
        #         self.workPart.CAMSetup.GetRoot(NXOpen.CAM.CAMSetup.View.Geometry)
        #     )

        # response = UI.ask_yes_no(
        #     BF.get_text(Text.AskDelMethodViewHeader),
        #     [BF.get_text(Text.AskDelMethodView)],
        # )

        # if response == 1:
        #     AllViews.append(
        #         self.workPart.CAMSetup.GetRoot(NXOpen.CAM.CAMSetup.View.MachineMethod)
        #     )

        if len(self.views) == 0:
            UI.user_abort()
            return

        AllUdeTyps = [
            NXOpen.UF.Ude.SetType.ValueOf(0),
            NXOpen.UF.Ude.SetType.ValueOf(1),
            NXOpen.UF.Ude.SetType.ValueOf(3),
        ]
        BF.set_undo_mark("Delete all UDES's", self.theSession)
        for UdeType in AllUdeTyps:
            for View in self.views:
                objects_in_view = NXOpen.CAM.NCGroup.GetMembers(View)
                self.pars_view(objects_in_view, UdeType)

    def deleteude(self, tagged: NXOpen.CAM.Operation, UdeType):
        obj: list = [tagged]
        theObjectsUdeSet = self.workPart.CAMSetup.CreateObjectsUdeSet(
            obj, NXOpen.CAM.CAMSetup.Ude.Start
        )
        
        
        if not len(theObjectsUdeSet.UdeSet.UdeList.GetContents()) == 0:
            lw("*****************************************************")
            if self.workPart.CAMSetup.IsGroup(tagged):
                lw(f"Group Name: {tagged.Name}")
            if self.workPart.CAMSetup.IsOperation(tagged):
                lw(f"Operation Name: {tagged.Name}") 
            
            for ude in theObjectsUdeSet.UdeSet.UdeList.GetContents():
                    udeName = UdeName.get_ude_name(ude.UdeName)
                    lw(f"UDE Name: {udeName}")
        
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
        if Checks.check_nx_version(
            int(versions["version_max"]), int(versions["version_min"])
        ):
            instance = DelAllUde()
            instance.main()
