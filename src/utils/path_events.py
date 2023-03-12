import NXOpen


class PathMotion:
    def path_event_type(
        camPathToolpathEventType: NXOpen.CAM.CamPathToolpathEventType,
    ):
        match camPathToolpathEventType:
            case NXOpen.CAM.CamPathToolpathEventType.Motion:
                pass
            case NXOpen.CAM.CamPathToolpathEventType.LevelMarker:
                pass
            case NXOpen.CAM.CamPathToolpathEventType.Ude:
                pass
            case NXOpen.CAM.CamPathToolpathEventType.System:
                pass
            case NXOpen.CAM.CamPathToolpathEventType.Marker:
                pass

    def path_motion_type(camPathMotionType: NXOpen.CAM.CamPathMotionType):
        match camPathMotionType:
            case NXOpen.CAM.CamPathMotionType.Approach:
                pass
            case NXOpen.CAM.CamPathMotionType.Cycle:
                pass
            case NXOpen.CAM.CamPathMotionType.Cut:
                pass
            case NXOpen.CAM.CamPathMotionType.Departure:
                pass
            case NXOpen.CAM.CamPathMotionType.FirstCut:
                pass
            case NXOpen.CAM.CamPathMotionType.From:
                pass
            case NXOpen.CAM.CamPathMotionType.Gohome:
                pass
            case NXOpen.CAM.CamPathMotionType.InternalLift:
                pass
            case NXOpen.CAM.CamPathMotionType.Rapid:
                pass
            case NXOpen.CAM.CamPathMotionType.Retract:
                pass
            case NXOpen.CAM.CamPathMotionType.Return:
                pass
            case NXOpen.CAM.CamPathMotionType.SideCut:
                pass
            case NXOpen.CAM.CamPathMotionType.Stepover:
                pass
            case NXOpen.CAM.CamPathMotionType.Traversal:
                pass
            case NXOpen.CAM.CamPathMotionType.Undefined:
                pass

    def path_motion_shape(camPathMotionShapeType: NXOpen.CAM.CamPathMotionShapeType):
        match camPathMotionShapeType:
            case NXOpen.CAM.CamPathMotionShapeType.Circular:
                pass
            case NXOpen.CAM.CamPathMotionShapeType.Helical:
                pass
            case NXOpen.CAM.CamPathMotionShapeType.Linear:
                pass
            case NXOpen.CAM.CamPathMotionShapeType.Nurbs:
                pass
            case NXOpen.CAM.CamPathMotionShapeType.Undefined:
                pass
