import NXOpen
import NXOpen.CAM
from utils.utils import lw, Checks, UI
import sys


class CreateAxis:
    def __init__(self):
        self.theSession = NXOpen.Session.GetSession()
        self.theUfSession = NXOpen.UF.UFSession.GetUFSession()
        self.theUI = NXOpen.UI.GetUI()
        self.workPart = self.theSession.Parts.Work

    def create_axis(self):
        if not Checks.check_workpart(self.workPart):
            return

        if not Checks.check_setup():
            return

        num = self.theUI.SelectionManager.GetNumSelectedObjects()
        objects1 = [NXOpen.CAM.CAMObject.Null] * num

        if num == 0:
            self.theUI.NXMessageBox.Show(
                "Select Operation",
                NXOpen.NXMessageBox.DialogType.Error,
                "No Operation was selected!",
            )

        for i in range(num):
            objects1[i] = self.theUI.SelectionManager.GetSelectedTaggedObject(i)
            object: NXOpen.CAM.Operation = objects1[i]
            path: NXOpen.CAM.Path = object.GetPath()
            numberOfToolpathEvents: int = path.NumberOfToolpathEvents
            #camPathMotionType:NXOpen.CAM.CamPathMotionType = NXOpen.CAM.CamPathMotionType
            #camPathMotionShapeType : NXOpen.CAM.CamPathMotionShapeType = NXOpen.CAM.CamPathMotionShapeType

            for j in range(numberOfToolpathEvents):
                j += 1
                camPathToolpathEventType: NXOpen.CAM.CamPathToolpathEventType = (
                    path.GetToolpathEventType(j)
                )
                if camPathToolpathEventType == NXOpen.CAM.CamPathToolpathEventType.Motion:
                    lw("Its Motion")
                    
                    #ev = path.GetToolpathEvent(j)
                    #lw(type(path.IsToolpathEventAMotion(ev)))
                if camPathToolpathEventType == NXOpen.CAM.CamPathToolpathEventType.LevelMarker:
                    lw("Its Level Marker")
                    ...
                if camPathToolpathEventType == NXOpen.CAM.CamPathToolpathEventType.System:
                    lw("Its System")
                    ...
                if camPathToolpathEventType == NXOpen.CAM.CamPathToolpathEventType.Ude:
                    lw("Its UDE")
                    ...
                if camPathToolpathEventType == NXOpen.CAM.CamPathToolpathEventType.Marker:
                    lw("Its Marker")
                    ...


if __name__ == "__main__":
    lw(sys.version)
    inistance = CreateAxis()
    inistance.create_axis()
