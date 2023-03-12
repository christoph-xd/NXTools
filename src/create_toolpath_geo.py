import math
import NXOpen
import NXOpen.CAM
from utils import lw, Checks, UI
import sys


class CreateGeometry:
    def __init__(self):
        self.theSession = NXOpen.Session.GetSession()
        self.theUfSession = NXOpen.UF.UFSession.GetUFSession()
        self.theUI = NXOpen.UI.GetUI()
        self.workPart = self.theSession.Parts.Work
        self.unit = self.workPart.UnitCollection.FindObject("MilliMeter")
        self.flagFirstMotion = True
        self.flagLastMotion = True

    def calculate_endpoint(
        self, point: NXOpen.Point3d, vector: NXOpen.Vector3d
    ) -> NXOpen.Point3d:
        length = 5
        x = point.X + length * vector.X
        y = point.Y + length * vector.Y
        z = point.Z + length * vector.Z
        endpoint = NXOpen.Point3d(x, y, z)

        return endpoint

    def calculate_pointon(
        self,
        startpoint: NXOpen.Point3d,
        centerpoint: NXOpen.Point3d,
        endpoint: NXOpen.Point3d,
        radius: float,
    ) -> NXOpen.Point3d:
        v1 = [centerpoint.X - startpoint.X, centerpoint.Y - startpoint.Y]
        v2 = [centerpoint.X - endpoint.X, centerpoint.Y - endpoint.Y]
        dot_product = v1[0] * v2[0] + v1[1] * v2[1]
        length_product = math.sqrt(v1[0] ** 2 + v1[1] ** 2) * math.sqrt(
            v2[0] ** 2 + v2[1] ** 2
        )
        angle = math.acos(dot_product / length_product)

        half_angle = angle / 2
        cos_half_angle = math.cos(half_angle)
        sin_half_angle = math.sin(half_angle)

        vector = [radius * cos_half_angle, radius * sin_half_angle]

        x = centerpoint.X + vector[0]
        y = centerpoint.Y + vector[1]

        return NXOpen.Point3d(x, y, endpoint.Z)

    def create_point(self, points: NXOpen.Point3d):
        p = self.workPart.Points.CreatePoint(points)
        p.SetVisibility(NXOpen.SmartObject.VisibilityOption.Visible)

    def create_vector(self, vector: NXOpen.Vector3d, startPoint: NXOpen.Point3d):
        endPoint = self.calculate_endpoint(startPoint, vector)
        self.workPart.Datums.CreateFixedDatumAxis(startPoint, endPoint)

    def create_line(self, startpoint: NXOpen.Point3d, endpoint: NXOpen.Point3d):
        l = self.workPart.Curves.CreateLine(startpoint, endpoint)
        l.SetVisibility(NXOpen.SmartObject.VisibilityOption.Visible)

    def create_arc(
        self,
        startpoint: NXOpen.Point3d,
        centerpoint: NXOpen.Point3d,
        endpoint: NXOpen.Point3d,
        arcRadius: float,
    ):
        pointon = self.calculate_pointon(startpoint, centerpoint, endpoint, arcRadius)
        c = self.workPart.Curves.CreateArc(startpoint, pointon, endpoint, False)
        # c.SetVisibility(NXOpen.SmartObject.VisibilityOption.Visible)

    def selected_operation(self) -> list:
        operationCollection = []
        num = self.theUI.SelectionManager.GetNumSelectedObjects()
        objects1 = [NXOpen.CAM.CAMObject.Null] * num

        if num != 1:
            self.theUI.NXMessageBox.Show(
                "Select Operation",
                NXOpen.NXMessageBox.DialogType.Error,
                "Select only 1 Operation!",
            )
            return None
        selected = self.theUI.SelectionManager.GetSelectedTaggedObject

        for i in range(num):
            objects1[i] = selected(i)
            operationCollection.append(objects1[i])

        return operationCollection

    def linear_motion(
        self, toolPath: NXOpen.CAM.Path, toolPathEvent: NXOpen.CAM.PathEvent
    ) -> NXOpen.Point3d:
        toolPathLinearMotion: NXOpen.CAM.PathLinearMotion = toolPath.GetLinearMotion(
            toolPathEvent
        )
        endpoint: NXOpen.Point3d = toolPathLinearMotion.EndPoint

        return endpoint

    def circular_motion(
        self, toolPath: NXOpen.CAM.Path, toolPathEvent: NXOpen.CAM.PathEvent
    ) -> tuple:
        toolPathCircularMotion: NXOpen.CAM.PathCircularMotion = (
            toolPath.GetCircularMotion(toolPathEvent)
        )

        endpoint = toolPathCircularMotion.EndPoint
        arcCenter = toolPathCircularMotion.ArcCenter
        arcRadius = toolPathCircularMotion.ArcRadius
        lw(toolPathCircularMotion.Direction)
        return endpoint, arcCenter, arcRadius

    def main(self):
        if not Checks.check_workpart(self.workPart):
            return

        if not Checks.check_setup():
            return

        operationCollection = self.selected_operation()

        if operationCollection == None:
            return

        for _, operation in enumerate(operationCollection):
            operation: NXOpen.CAM.Operation = operation

            toolPath: NXOpen.CAM.Path = operation.GetPath()
            numberOfToolpathEvents: int = toolPath.NumberOfToolpathEvents

            startpoint = 0
            endpoint = 0
            for i in range(numberOfToolpathEvents):
                i += 1
                camPathToolpathEventType: NXOpen.CAM.CamPathToolpathEventType = (
                    toolPath.GetToolpathEventType(i)
                )

                if (
                    camPathToolpathEventType
                    == NXOpen.CAM.CamPathToolpathEventType.Motion
                ):
                    toolPathEvent = toolPath.GetToolpathEvent(i)
                    (
                        _,
                        _,
                        camPathMotionShapeType,
                    ) = toolPath.IsToolpathEventAMotion(toolPathEvent)

                    match camPathMotionShapeType:
                        case NXOpen.CAM.CamPathMotionShapeType.Circular:
                            endpoint, arcCenter, arcRadius = self.circular_motion(
                                toolPath, toolPathEvent
                            )
                            if self.flagFirstMotion:
                                self.flagFirstMotion = False
                                startpoint = endpoint
                                continue
                            # self.create_line(startpoint, endpoint)
                            self.create_arc(startpoint, arcCenter, endpoint, arcRadius)
                            startpoint = endpoint
                        case NXOpen.CAM.CamPathMotionShapeType.Helical:
                            if self.flagFirstMotion:
                                self.flagFirstMotion = False
                                startpoint = endpoint
                                continue
                            pass
                        case NXOpen.CAM.CamPathMotionShapeType.Linear:
                            endpoint = self.linear_motion(toolPath, toolPathEvent)
                            if self.flagFirstMotion:
                                self.flagFirstMotion = False
                                startpoint = endpoint
                                continue
                            self.create_line(startpoint, endpoint)
                            startpoint = endpoint
                        case NXOpen.CAM.CamPathMotionShapeType.Nurbs:
                            if self.flagFirstMotion:
                                self.flagFirstMotion = False
                                startpoint = endpoint
                                continue
                            pass
                        case NXOpen.CAM.CamPathMotionShapeType.Undefined:
                            if self.flagFirstMotion:
                                self.flagFirstMotion = False
                                startpoint = endpoint
                                continue
                            pass


if __name__ == "__main__":
    inistance = CreateGeometry()
    inistance.main()
    # C:\Users\chris\Documents\Development\NXTools\src
