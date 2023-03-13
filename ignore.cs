using System;
using NXOpen;
using NXOpen.UF;
using NXOpen.Utilities;
using NXOpen.CAM;
using NXOpen.Assemblies;

static class GetPathInformation
{
    static Session theSession;
    static UFSession theUfSession;
    private static UI theUI;

    public static void Main()
    {
        theSession = Session.GetSession();
        theUfSession = UFSession.GetUFSession();
        Part workPart = theSession.Parts.Work;
        theUI = UI.GetUI();

        if (workPart == null)
        {
            UI.GetUI().NXMessageBox.Show("Message", NXMessageBox.DialogType.Error, "A Part must be Opened.");
            return;
        }

        theSession.EnableRedo(false);

        if (!theSession.ListingWindow.IsOpen) theSession.ListingWindow.Open();

        SystemInfo(theUfSession.Part, workPart);

        try
        {
            Tag[] operTag;
            Tag setupTag = Tag.Null;

            int countObject = 0;

            theUfSession.Cam.InitSession();
            theUfSession.Setup.AskSetup(out setupTag);

            if (setupTag == Tag.Null)
            {
                UI.GetUI().NXMessageBox.Show("Message", NXMessageBox.DialogType.Error, "No Cam Setup in this Part.");
                return;
            }

            theUfSession.UiOnt.AskSelectedNodes(out countObject, out operTag);

            if (countObject == 0)
            {
                UI.GetUI().NXMessageBox.Show("Message", NXMessageBox.DialogType.Error, "An Operation must be Selected.");
                return;
            }

            for (int i = 0; i < countObject; i++)
            {
                int type, subType;

                theUfSession.Obj.AskTypeAndSubtype(operTag[i], out type, out subType);

                NXObject camObject = (NXObject)(NXObjectManager.Get(operTag[i]));

                if (type == UFConstants.UF_machining_operation_type)
                {
                    NXOpen.CAM.Operation operation = (NXOpen.CAM.Operation)(NXObjectManager.Get(operTag[i]));

                    Path path = operation.GetPath();
                    
                    int numberOfToolpathEvents = path.NumberOfToolpathEvents;

                    theSession.ListingWindow.WriteLine(i.ToString() + ". Operation : " + operation.Name + " Contains : " + numberOfToolpathEvents + " Path Events\n\n");

                    for (int j = 1; j < numberOfToolpathEvents + 1; j++)    /* The Path Index must be Start at 1 */
                    {
                        CamPathToolpathEventType camPathToolpathEventType = path.GetToolpathEventType(j);
                        CamPathMotionType camPathMotionType = default(CamPathMotionType);
                        CamPathMotionShapeType camPathMotionShapeType = default(CamPathMotionShapeType);

                        switch (camPathToolpathEventType)
                        {
                            case CamPathToolpathEventType.Motion:
                                path.IsToolpathEventAMotion(j, out camPathMotionType, out camPathMotionShapeType);
                                theSession.ListingWindow.WriteLine(j.ToString() + ". Path Motion Type : " + camPathMotionType + " --> Shape Type : " + camPathMotionShapeType);

                                switch (camPathMotionType)
                                {
                                    case CamPathMotionType.From:
                                    case CamPathMotionType.Rapid:
                                    case CamPathMotionType.Approach:
                                    case CamPathMotionType.Engage:
                                    case CamPathMotionType.FirstCut:
                                    case CamPathMotionType.Cut:
                                    case CamPathMotionType.SideCut:
                                    case CamPathMotionType.Stepover:
                                    case CamPathMotionType.InternalLift:
                                    case CamPathMotionType.Retract:
                                    case CamPathMotionType.Traversal:
                                    case CamPathMotionType.Gohome:
                                    case CamPathMotionType.Return:
                                    case CamPathMotionType.Departure:
                                    case CamPathMotionType.Cycle:
                                    case CamPathMotionType.Undefined:

                                        switch (camPathMotionShapeType)
                                        {
                                            case CamPathMotionShapeType.Linear:
                                                PathLinearMotion pathLinearMotion = path.GetLinearMotion(j);
                                                DisplayMotionInformation(pathLinearMotion);
                                                break;

                                            case CamPathMotionShapeType.Circular:
                                                PathCircularMotion pathCircularMotion = path.GetCircularMotion(j);
                                                DisplayCircularMotionInformation(pathCircularMotion);
                                                break;

                                            case CamPathMotionShapeType.Helical:
                                                PathHelixMotion pathHelixMotion = path.GetHelixMotion(j);
                                                DisplayHelicalMotionInformation(pathHelixMotion);
                                                break;

                                            case CamPathMotionShapeType.Nurbs:
                                                theSession.ListingWindow.WriteLine("Nurbs Motion Shape.");
                                                break;

                                            case CamPathMotionShapeType.Undefined:
                                                theSession.ListingWindow.WriteLine("Motion Shape Undefined.");
                                                break;

                                            default:
                                                theSession.ListingWindow.WriteLine("Unknown Motion Shape.");
                                                break;
                                        } /* switch camPathMotionShapeType */
                                        break;

                                    default:
                                        break;
                                } /* switch camPathMotionType */
                                break;

                            case CamPathToolpathEventType.LevelMarker:
                                PathLevelMarker pathLevelMarker = path.GetLevelMarker(j);
                                double levelDepth = pathLevelMarker.LevelDepth;
                                Vector3d vector3d = pathLevelMarker.LevelNormal;
                                theSession.ListingWindow.WriteLine(j.ToString() + ".Level Marker Depth : " + levelDepth + " Normal X" + vector3d.X + " Y" + vector3d.Y + " Z" + vector3d.Z + "\n\n");
                                break;

                            case CamPathToolpathEventType.System:
                                theSession.ListingWindow.WriteLine(j.ToString() + ". System Tool Path Event Type\n\n");
                                break;

                            case CamPathToolpathEventType.Ude:
                                Ude ude = path.GetUde(j);
                                DisplayUdeInformation(ude, j);
                                break;

                            default:
                                theSession.ListingWindow.WriteLine("Unknown ToolPath Event Type.");
                                break;
                        } /* switch camPathToolpathEventType */
                    } /* for int j = 1 */

            /* It is necessary to cleanup after a path has been asked for. The call below will cleanup and save the path if necessary */
            operation.SavePath(path);
                } /* if type */
            } /* for int i = 0 */
        }
        catch (NXOpen.NXException ex)
        {
            UI.GetUI().NXMessageBox.Show("Message", NXMessageBox.DialogType.Error, ex.Message);
        }
    }

    //------------------------------------------------------------------------------
    //             Method : DisplayUdeInformation
    //
    //  Display Ude Information (This Ude(s) are added in Edit Mode)
    //
    //  Input Ude     : The Ude to Query
    //  Input Integer : Count to Display
    //  Return        : None
    //------------------------------------------------------------------------------
    static void DisplayUdeInformation(Ude ude, int count)
    {
        string udeName = ude.UdeName;
        int numberOfparameters = ude.NumberOfParameters;

        theSession.ListingWindow.WriteLine(count.ToString() + ". Ude Name : " + udeName + " Number of Parameters : " + numberOfparameters);
    }

    //------------------------------------------------------------------------------
    //             Method : DisplayHelicalMotionInformation
    //
    //  Display Helical Motion Information
    //
    //  Input PathHelixMotion : The Helical Path Motion to Query
    //  Return                : None
    //------------------------------------------------------------------------------
    static void DisplayHelicalMotionInformation(PathHelixMotion pathHelixMotion)
    {
        Point3d arcCenter = pathHelixMotion.ArcCenter;
        Point3d endPoint = pathHelixMotion.EndPoint;

        double feedValue = 0.0;
        double arcRadius = pathHelixMotion.ArcRadius;
        double numberOfRevolutions = pathHelixMotion.NumberOfRevolutions;

        CamPathDir camPathDir = pathHelixMotion.Direction;
        CamPathFeedUnitType camPathFeedUnitType;

        Vector3d vector3d = pathHelixMotion.ToolAxis;

        pathHelixMotion.GetFeedrate(out feedValue, out camPathFeedUnitType);

        theSession.ListingWindow.WriteLine("\tCircular Motion End Point : X" + endPoint.X + " Y" + endPoint.Y + " Z" + endPoint.Z);
        theSession.ListingWindow.WriteLine("\tCenter      : X" + arcCenter.X + " Y" + arcCenter.Y + " Z" + arcCenter.Z );
        theSession.ListingWindow.WriteLine("\tRadius      : " + arcRadius + " --> Direction : " + camPathDir + " --> Number of Revolutions : " + numberOfRevolutions);
        theSession.ListingWindow.WriteLine("\tTool Axis   : X" + vector3d.X + " Y" + vector3d.Y + " Z" + vector3d.Z);
        theSession.ListingWindow.WriteLine("\tMotion Type : " + pathHelixMotion.MotionType);
        theSession.ListingWindow.WriteLine("\tFeedRate    : " + feedValue + " --> Unit : " + camPathFeedUnitType + "\n\n");
    }

    //------------------------------------------------------------------------------
    //             Method : DisplayCircularMotionInformation
    //
    //  Display Circular Motion Information
    //
    //  Input PathCircularMotion : The Circular Path Motion to Query
    //  Return                   : None
    //------------------------------------------------------------------------------
    static void DisplayCircularMotionInformation(PathCircularMotion pathCircularMotion)
    {
        double feedValue = 0.0;
        double arcRadius = pathCircularMotion.ArcRadius;

        Point3d arcCenter = pathCircularMotion.ArcCenter;
        Point3d endPoint = pathCircularMotion.EndPoint;

        CamPathDir camPathDir = pathCircularMotion.Direction;
        CamPathFeedUnitType camPathFeedUnitType;

        Vector3d vector3d = pathCircularMotion.ToolAxis;

        pathCircularMotion.GetFeedrate(out feedValue, out camPathFeedUnitType);

        theSession.ListingWindow.WriteLine("\tCircular Motion End Point : X" + endPoint.X + " Y" + endPoint.Y + " Z" + endPoint.Z);
        theSession.ListingWindow.WriteLine("\tCenter      : X" + arcCenter.X + " Y" + arcCenter.Y + " Z" + arcCenter.Z );
        theSession.ListingWindow.WriteLine("\tRadius      : " + arcRadius + " --> Direction : " + camPathDir);
        theSession.ListingWindow.WriteLine("\tTool Axis   : X" + vector3d.X + " Y" + vector3d.Y + " Z" + vector3d.Z);
        theSession.ListingWindow.WriteLine("\tMotion Type : " + pathCircularMotion.MotionType);
        theSession.ListingWindow.WriteLine("\tFeedRate    : " + feedValue + " --> Unit : " + camPathFeedUnitType + "\n\n");
    }

    //------------------------------------------------------------------------------
    //             Method : DisplayMotionInformation
    //
    //  Display Linear Motion Information
    //
    //  Input PathLinearMotion : The Linear Path Motion to Query
    //  Return                 : None
    //------------------------------------------------------------------------------
    static void DisplayMotionInformation(PathLinearMotion pathLinearMotion)
    {
        double feedValue = 0.0;
        CamPathFeedUnitType camPathFeedUnitType;

        Vector3d vector3d = pathLinearMotion.ToolAxis;
        Point3d endPoint = pathLinearMotion.EndPoint;
        
        pathLinearMotion.GetFeedrate(out feedValue, out camPathFeedUnitType);
        theSession.ListingWindow.WriteLine("\tLinear Motion End Point : X" + endPoint.X + " Y" + endPoint.Y + " Z" + endPoint.Z);
        theSession.ListingWindow.WriteLine("\tTool Axis   : X" + vector3d.X + " Y" + vector3d.Y + " Z" + vector3d.Z);
        theSession.ListingWindow.WriteLine("\tMotion Type : " + pathLinearMotion.MotionType);
        theSession.ListingWindow.WriteLine("\tFeedRate    : " + feedValue + " --> Unit : " + camPathFeedUnitType + "\n\n");
    }

    //------------------------------------------------------------------------------
    //             Method : SystemInfo
    //
    //  Display System Information
    //
    //  Input UFPart : The UF Part
    //  Input Part   : The Work Part
    //  Return       : None
    //------------------------------------------------------------------------------
    static void SystemInfo(UFPart uFPart, Part workPart)
    {
        SystemInfo sysInfo;
        theUfSession.UF.AskSystemInfo(out sysInfo);

        string partName = string.Empty;
        uFPart.AskPartName(workPart.Tag, out partName);

        theSession.ListingWindow.WriteLine("============================================================");
        theSession.ListingWindow.WriteLine("Information Listing Created by : " + sysInfo.user_name.ToString());
        theSession.ListingWindow.WriteLine("Date                           : " + sysInfo.date_buf.ToString());
        theSession.ListingWindow.WriteLine("Current Work Part              : " + partName);
        theSession.ListingWindow.WriteLine("Node Name                      : " + sysInfo.node_name.ToString());
        theSession.ListingWindow.WriteLine("============================================================\n\n");
    }

    //------------------------------------------------------------------------------
    //             Method : GetUnloadOption
    //
    //  Unload the Current Image
    //
    //  Input String : String Send by NX
    //  Return       : Integer
    //------------------------------------------------------------------------------
    public static int GetUnloadOption(string arg)
    {
        return System.Convert.ToInt32(Session.LibraryUnloadOption.Immediately);

        //Unloads the image explicitly, via an unload dialog
        //return System.Convert.ToInt32(Session.LibraryUnloadOption.Explicitly);

        //Unloads the image when the NX session terminates
        //return System.Convert.ToInt32(Session.LibraryUnloadOption.AtTermination);
    }
}