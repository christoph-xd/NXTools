import math
import json
import NXOpen
import NXOpen.CAM
from utils import lw, Checks, UI, Getters
from pathlib import Path


class CreateGeometry:
    def __init__(self):
        self.theSession = NXOpen.Session.GetSession()
        self.theUfSession = NXOpen.UF.UFSession.GetUFSession()
        self.theUI = NXOpen.UI.GetUI()
        self.workPart = self.theSession.Parts.Work
        self.unit = self.workPart.UnitCollection.FindObject("MilliMeter")
        self.flagFirstMotion = True
        self.flagLastMotion = True
        self.locale = Getters.get_lang(self.theSession)

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
        direction: NXOpen.CAM.CamPathDir,
    ) -> NXOpen.Point3d:
        v1 = [centerpoint.X - startpoint.X, centerpoint.Y - startpoint.Y]
        v2 = [centerpoint.X - endpoint.X, centerpoint.Y - endpoint.Y]
        dot_product = v1[0] * v2[0] + v1[1] * v2[1]
        length_product = math.sqrt(v1[0] ** 2 + v1[1] ** 2) * math.sqrt(
            v2[0] ** 2 + v2[1] ** 2
        )

        angle = math.acos(dot_product / length_product)
        if direction == NXOpen.CAM.CamPathDir.Clockwise:
            angle = -angle

        half_angle = angle / 2
        cos_half_angle = math.cos(half_angle)
        sin_half_angle = math.sin(half_angle)

        vector = [radius * cos_half_angle, radius * sin_half_angle]

        if direction == NXOpen.CAM.CamPathDir.Clockwise:
            vector = [-vector[0], -vector[1]]

        x = centerpoint.X + vector[0]
        y = centerpoint.Y + vector[1]

        return NXOpen.Point3d(x, y, endpoint.Z)

    def create_group(self, lineTags: list, groupName: str):
        groupBuilder = self.workPart.CreateGatewayGroupBuilder(NXOpen.Group.Null)
        groupBuilder.GroupName = groupName
        for lineTag in lineTags:
            obj = NXOpen.TaggedObjectManager.GetTaggedObject(lineTag)
            groupBuilder.ObjectsInGroup.Add(obj)
        groupBuilder.Commit()

    def create_point(self, points: NXOpen.Point3d):
        p = self.workPart.Points.CreatePoint(points)
        p.SetVisibility(NXOpen.SmartObject.VisibilityOption.Visible)

    def create_vector(self, vector: NXOpen.Vector3d, startPoint: NXOpen.Point3d):
        endPoint = self.calculate_endpoint(startPoint, vector)
        self.workPart.Datums.CreateFixedDatumAxis(startPoint, endPoint)

    def create_line(self, startpoint: NXOpen.Point3d, endpoint: NXOpen.Point3d):
        l = self.workPart.Curves.CreateLine(startpoint, endpoint)
        l.SetVisibility(NXOpen.SmartObject.VisibilityOption.Visible)

    def create_uf_line(self, startpoint: NXOpen.Point3d, endpoint: NXOpen.Point3d):
        startpoint = [startpoint.X, startpoint.Y, startpoint.Z]
        endpoint = [endpoint.X, endpoint.Y, endpoint.Z]
        line_coords = NXOpen.UF.Curve.Line(endpoint, startpoint)
        lineTag = self.theUfSession.Curve.CreateLine(line_coords)
        return lineTag

    def create_arc(
        self,
        startpoint: NXOpen.Point3d,
        centerpoint: NXOpen.Point3d,
        endpoint: NXOpen.Point3d,
        arcRadius: float,
        direction: int,
    ):
        pointon = self.calculate_pointon(
            startpoint, centerpoint, endpoint, arcRadius, direction
        )
        c = self.workPart.Curves.CreateArc(startpoint, pointon, endpoint, False)
        # c.SetVisibility(NXOpen.SmartObject.VisibilityOption.Visible)
    
    def create_uf_arc(self):
        self.theUfSession.Curve.CreateArc()

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
            if self.workPart.CAMSetup.IsOperation(objects1[i]):
                operationCollection.append(objects1[i])
            else:
                self.theUI.NXMessageBox.Show(
                    "Not an Operation",
                    NXOpen.NXMessageBox.DialogType.Error,
                    "The seleced Item isn't a Operation",
                )
                continue
            operationBuilder = (
                self.workPart.CAMSetup.CAMOperationCollection.CreateBuilder(objects1[i])
            )
            if (
                not operationBuilder.MotionOutputBuilder.OutputType
                == NXOpen.CAM.ArcOutputTypeCiBuilder.OutputTypes.LinearOnly
            ):
                self.theUI.NXMessageBox.Show(
                    "Output Not Line",
                    NXOpen.NXMessageBox.DialogType.Error,
                    "The Operation is not Calculated in Line",
                )
                return None

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
        direction = toolPathCircularMotion.Direction
        return endpoint, arcCenter, arcRadius, direction

    def main(self):
        # lw(Getters.get_lang(self.theSession))
        if not Checks.check_workpart(self.workPart):
            return

        if not Checks.check_setup():
            return

        operationCollection = self.selected_operation()

        if operationCollection == None:
            return

        for _, operation in enumerate(operationCollection):
            operation: NXOpen.CAM.Operation = operation
            operationName = operation.Name
            toolPath: NXOpen.CAM.Path = operation.GetPath()
            numberOfToolpathEvents: int = toolPath.NumberOfToolpathEvents
            lineTags: list = []

            if numberOfToolpathEvents > 10000:
                response = UI.ask_yes_no(
                    "Continue",
                    [
                        f"There are a big amount of Lines ({numberOfToolpathEvents})!\nYou are sure you want continue?"
                    ],
                )

                if response == 2:
                    lw("User Abort")
                    return

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

                    if (
                        camPathMotionShapeType
                        == NXOpen.CAM.CamPathMotionShapeType.Circular
                    ):
                        (
                            endpoint,
                            arcCenter,
                            arcRadius,
                            direction,
                        ) = self.circular_motion(toolPath, toolPathEvent)
                        if self.flagFirstMotion:
                            self.flagFirstMotion = False
                            startpoint = endpoint
                            continue
                        # self.create_line(startpoint, endpoint)
                        self.create_arc(
                            startpoint, arcCenter, endpoint, arcRadius, direction
                        )
                        startpoint = endpoint
                    if (
                        camPathMotionShapeType
                        == NXOpen.CAM.CamPathMotionShapeType.Helical
                    ):
                        if self.flagFirstMotion:
                            self.flagFirstMotion = False
                            startpoint = endpoint
                            continue
                        pass
                    if (
                        camPathMotionShapeType
                        == NXOpen.CAM.CamPathMotionShapeType.Linear
                    ):
                        endpoint = self.linear_motion(toolPath, toolPathEvent)
                        if self.flagFirstMotion:
                            self.flagFirstMotion = False
                            startpoint = endpoint
                            continue
                        lineTags.append(self.create_uf_line(startpoint, endpoint))
                        startpoint = endpoint
                    if (
                        camPathMotionShapeType
                        == NXOpen.CAM.CamPathMotionShapeType.Nurbs
                    ):
                        if self.flagFirstMotion:
                            self.flagFirstMotion = False
                            startpoint = endpoint
                            continue
                        pass
                    if (
                        camPathMotionShapeType
                        == NXOpen.CAM.CamPathMotionShapeType.Undefined
                    ):
                        if self.flagFirstMotion:
                            self.flagFirstMotion = False
                            startpoint = endpoint
                            continue
                        pass
        self.create_group(lineTags, operationName)


if __name__ == "__main__":
    config_file = Path(__file__).parent
    with open(f"{config_file}/config.json", "r") as f:
        config = json.load(f)
        report_json = config["report_cutting_length"]
    if Checks.check_nx_version(
        int(report_json["version_max"]), int(report_json["version_min"])
    ):
        inistance = CreateGeometry()
        inistance.main()
