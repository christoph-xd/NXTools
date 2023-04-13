import json
import math
import sys
from pathlib import Path

import NXOpen
import NXOpen.CAM

from utils import UI, Checks, lw


class CreateAxis:
    def __init__(self):
        self.theSession = NXOpen.Session.GetSession()
        self.theUfSession = NXOpen.UF.UFSession.GetUFSession()
        self.theUI = NXOpen.UI.GetUI()
        self.workPart = self.theSession.Parts.Work
        self.unit = self.workPart.UnitCollection.FindObject("MilliMeter")
        self.flagFirstMotion = False
        self.flagLastMotion = False

        self.checkWork = True
        self.checkSetup = True
        if not Checks.check_workpart(self.workPart):
            self.checkWork = False

        if not Checks.check_setup():
            self.checkSetup = False

    def calculate_endpoint(
        self, point: NXOpen.Point3d, vector: NXOpen.Vector3d
    ) -> NXOpen.Point3d:
        """Calc the Endpoint by Vector and Startpoint

        Args:
            point (NXOpen.Point3d): Startpoint
            vector (NXOpen.Vector3d): Tool Vector

        Returns:
            NXOpen.Point3d: Endpoint by a length of 5
        """
        length = 5
        x = point.X + length * vector.X
        y = point.Y + length * vector.Y
        z = point.Z + length * vector.Z
        endpoint = NXOpen.Point3d(x, y, z)

        return endpoint

    def create_point(self, points: NXOpen.Point3d):
        p = self.workPart.Points.CreatePoint(points)
        p.SetVisibility(NXOpen.SmartObject.VisibilityOption.Visible)

    def create_vector(self, vector: NXOpen.Vector3d, startPoint: NXOpen.Point3d):
        endPoint = self.calculate_endpoint(startPoint, vector)
        self.workPart.Datums.CreateFixedDatumAxis(startPoint, endPoint)

    def linear_motion(self, path: NXOpen.CAM.Path, toolPathEvent: NXOpen.CAM.PathEvent):
        pathLinearMotion: NXOpen.CAM.PathLinearMotion = path.GetLinearMotion(
            toolPathEvent
        )

        endPoints: NXOpen.Point3d = pathLinearMotion.EndPoint
        toolAxis: NXOpen.Vector3d = pathLinearMotion.ToolAxis

        self.create_point(endPoints)
        self.create_vector(toolAxis, endPoints)

    def circular_motion(
        self, path: NXOpen.CAM.Path, toolPathEvent: NXOpen.CAM.PathEvent
    ):
        pathCircularMotion: NXOpen.CAM.PathCircularMotion = path.GetCircularMotion(
            toolPathEvent
        )
        pass

    def check_motion_shape(
        self,
        camPathMotionShapeType: NXOpen.CAM.CamPathMotionShapeType,
        path: NXOpen.CAM.Path,
        toolPathEvent: NXOpen.CAM.PathEvent,
    ):
        if camPathMotionShapeType == NXOpen.CAM.CamPathMotionShapeType.Linear:
            self.linear_motion(path, toolPathEvent)

        if camPathMotionShapeType == NXOpen.CAM.CamPathMotionShapeType.Circular:
            self.circular_motion(path, toolPathEvent)

    def create_axis(self):
        count, toolTag = self.theUfSession.UiOnt.AskSelectedNodes()
        objects1 = [NXOpen.CAM.CAMObject.Null] * count

        if count == 0:
            self.theUI.NXMessageBox.Show(
                "Select Operation",
                NXOpen.NXMessageBox.DialogType.Error,
                "No Operation was selected!",
            )

        for i in range(count):
            objects1[i] = NXOpen.TaggedObjectManager.GetTaggedObject(toolTag[i])
            object: NXOpen.CAM.Operation = objects1[i]
            path: NXOpen.CAM.Path = object.GetPath()
            numberOfToolpathEvents: int = path.NumberOfToolpathEvents

            while not self.flagFirstMotion and not self.flagLastMotion:
                for j in range(numberOfToolpathEvents):
                    j += 1
                    camPathToolpathEventType: NXOpen.CAM.CamPathToolpathEventType = (
                        path.GetToolpathEventType(j)
                    )

                    if (
                        camPathToolpathEventType
                        == NXOpen.CAM.CamPathToolpathEventType.Motion
                    ):
                        # lw("Its Motion")
                        self.flagFirstMotion = True
                        toolPathEvent = path.GetToolpathEvent(j)
                        (
                            _,
                            camPathMotionType,
                            camPathMotionShapeType,
                        ) = path.IsToolpathEventAMotion(toolPathEvent)

                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.FirstCut:
                            # lw("Its FirstCut")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Rapid:
                            # lw("Its Rapid")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.From:
                            # lw("Its From")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Approach:
                            # lw("Its Approach")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Engage:
                            # lw("Its Engage")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Cut:
                            # lw("Its Cut")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.SideCut:
                            # lw("Its SideCut")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Stepover:
                            # lw("Its Stepover")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if (
                            camPathMotionType
                            == NXOpen.CAM.CamPathMotionType.InternalLift
                        ):
                            # lw("Its InternalLift")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Retract:
                            # lw("Its Retract")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Traversal:
                            # lw("Its Traversal")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Gohome:
                            # lw("Its Gohome")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Return:
                            # lw("Its Return")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Departure:
                            # lw("Its Departure")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Cycle:
                            # lw("Its Cycle")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Undefined:
                            # lw("Undefined")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )

                    if self.flagFirstMotion:
                        break
                for j in reversed(range(numberOfToolpathEvents)):
                    j += 1
                    camPathToolpathEventType: NXOpen.CAM.CamPathToolpathEventType = (
                        path.GetToolpathEventType(j)
                    )

                    if (
                        camPathToolpathEventType
                        == NXOpen.CAM.CamPathToolpathEventType.Motion
                    ):
                        # lw("Its Motion")
                        self.flagLastMotion = True
                        toolPathEvent = path.GetToolpathEvent(j)
                        (
                            _,
                            camPathMotionType,
                            camPathMotionShapeType,
                        ) = path.IsToolpathEventAMotion(toolPathEvent)

                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.FirstCut:
                            # lw("Its FirstCut")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Rapid:
                            # lw("Its Rapid")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.From:
                            # lw("Its From")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Approach:
                            # lw("Its Approach")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Engage:
                            # lw("Its Engage")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Cut:
                            # lw("Its Cut")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.SideCut:
                            # lw("Its SideCut")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Stepover:
                            # lw("Its Stepover")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if (
                            camPathMotionType
                            == NXOpen.CAM.CamPathMotionType.InternalLift
                        ):
                            # lw("Its InternalLift")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Retract:
                            # lw("Its Retract")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Traversal:
                            # lw("Its Traversal")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Gohome:
                            # lw("Its Gohome")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Return:
                            # lw("Its Return")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Departure:
                            # lw("Its Departure")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Cycle:
                            # lw("Its Cycle")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )
                        if camPathMotionType == NXOpen.CAM.CamPathMotionType.Undefined:
                            # lw("Undefined")
                            self.check_motion_shape(
                                camPathMotionShapeType, path, toolPathEvent
                            )

                    if self.flagLastMotion:
                        break


if __name__ == "__main__":
    config_file = Path(__file__).parent
    with open(f"{config_file}/config.json", "r") as f:
        config = json.load(f)
        versions = config["report_cutting_length"]
    if Checks.check_nx_version(
        int(versions["version_max"]), int(versions["version_min"])
    ):
        inistance = CreateAxis()
        inistance.create_axis()
