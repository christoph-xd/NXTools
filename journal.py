# NX 2008
# Journal created by brandauc on Mon Mar 13 12:39:55 2023 W. Europe Standard Time
#
import math
import NXOpen
import NXOpen.Features
import NXOpen.GeometricUtilities
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display
    # ----------------------------------------------
    #   Menu: Insert->Curve->Studio Spline...
    # ----------------------------------------------
    markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
    
    studioSplineBuilderEx1 = workPart.Features.CreateStudioSplineBuilderEx(NXOpen.NXObject.Null)
    
    origin1 = NXOpen.Point3d(0.0, 0.0, 0.0)
    normal1 = NXOpen.Vector3d(0.0, 0.0, 1.0)
    plane1 = workPart.Planes.CreatePlane(origin1, normal1, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    studioSplineBuilderEx1.DrawingPlane = plane1
    
    unit1 = studioSplineBuilderEx1.Extender.StartValue.Units
    
    expression1 = workPart.Expressions.CreateSystemExpressionWithUnits("0", unit1)
    
    expression2 = workPart.Expressions.CreateSystemExpressionWithUnits("0", unit1)
    
    origin2 = NXOpen.Point3d(0.0, 0.0, 0.0)
    normal2 = NXOpen.Vector3d(0.0, 0.0, 1.0)
    plane2 = workPart.Planes.CreatePlane(origin2, normal2, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    studioSplineBuilderEx1.MovementPlane = plane2
    
    expression3 = workPart.Expressions.CreateSystemExpressionWithUnits("0", unit1)
    
    expression4 = workPart.Expressions.CreateSystemExpressionWithUnits("0", unit1)
    
    studioSplineBuilderEx1.OrientExpress.ReferenceOption = NXOpen.GeometricUtilities.OrientXpressBuilder.Reference.WcsDisplayPart
    
    theSession.SetUndoMarkName(markId1, "Studio Spline Dialog")
    
    studioSplineBuilderEx1.MatchKnotsType = NXOpen.Features.StudioSplineBuilderEx.MatchKnotsTypes.NotSet
    
    studioSplineBuilderEx1.OrientExpress.AxisOption = NXOpen.GeometricUtilities.OrientXpressBuilder.Axis.Passive
    
    studioSplineBuilderEx1.OrientExpress.PlaneOption = NXOpen.GeometricUtilities.OrientXpressBuilder.Plane.Passive
    
    markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Studio Spline")
    
    theSession.DeleteUndoMark(markId2, None)
    
    markId3 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Studio Spline")
    
    studioSplineBuilderEx1.Destroy()
    
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression2)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression4)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression1)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression3)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    theSession.UndoToMark(markId1, None)
    
    theSession.DeleteUndoMark(markId1, None)
    
    # ----------------------------------------------
    #   Menu: Insert->Curve->Line...
    # ----------------------------------------------
    markId4 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
    
    associativeLineBuilder1 = workPart.BaseFeatures.CreateAssociativeLineBuilder(NXOpen.Features.AssociativeLine.Null)
    
    origin3 = NXOpen.Point3d(0.0, 0.0, 0.0)
    normal3 = NXOpen.Vector3d(0.0, 0.0, 1.0)
    plane3 = workPart.Planes.CreatePlane(origin3, normal3, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    expression5 = workPart.Expressions.CreateSystemExpressionWithUnits("0", unit1)
    
    expression6 = workPart.Expressions.CreateSystemExpressionWithUnits("0", unit1)
    
    associativeLineBuilder1.Limits.StartLimit.Distance.SetFormula("0")
    
    associativeLineBuilder1.StartPointOptions = NXOpen.Features.AssociativeLineBuilder.StartOption.Point
    
    associativeLineBuilder1.StartAngle.SetFormula("0")
    
    associativeLineBuilder1.EndPointOptions = NXOpen.Features.AssociativeLineBuilder.EndOption.Point
    
    associativeLineBuilder1.EndAngle.SetFormula("0")
    
    associativeLineBuilder1.Limits.StartLimit.LimitOption = NXOpen.GeometricUtilities.CurveExtendData.LimitOptions.AtPoint
    
    associativeLineBuilder1.Limits.StartLimit.Distance.SetFormula("0")
    
    associativeLineBuilder1.Limits.EndLimit.LimitOption = NXOpen.GeometricUtilities.CurveExtendData.LimitOptions.AtPoint
    
    associativeLineBuilder1.Limits.EndLimit.Distance.SetFormula("21.5358302034802")
    
    associativeLineBuilder1.StartPointOptions = NXOpen.Features.AssociativeLineBuilder.StartOption.Inferred
    
    associativeLineBuilder1.EndPointOptions = NXOpen.Features.AssociativeLineBuilder.EndOption.Inferred
    
    theSession.SetUndoMarkName(markId4, "Line Dialog")
    
    expression7 = workPart.Expressions.CreateSystemExpression("0")
    
    scalar1 = workPart.Scalars.CreateScalarExpression(expression7, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    extractFace1 = workPart.Features.FindObject("LINKED_BODY(1)")
    edge1 = extractFace1.FindObject("EDGE * 364 * 383 {(-47.5774312966003,-76.0426066834721,182.2000000000001)(-48.8541218299192,-75.2287496920385,182.2000000000001)(-50.116894000743,-74.3934603020874,182.2000000000001) LINKED_BODY(1)}")
    point1 = workPart.Points.CreatePoint(edge1, scalar1, NXOpen.PointCollection.PointOnCurveLocationOption.PercentParameter, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    associativeLineBuilder1.StartPoint.Value = point1
    
    associativeLineBuilder1.StartPointOptions = NXOpen.Features.AssociativeLineBuilder.StartOption.Point
    
    expression8 = workPart.Expressions.CreateSystemExpression("0")
    
    scalar2 = workPart.Scalars.CreateScalarExpression(expression8, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    edge2 = extractFace1.FindObject("EDGE * 363 * 383 {(-39.3681803303588,-80.5992331072468,182.2000000000001)(-40.722948239988,-79.9232850090837,182.2000000000001)(-42.0661143290494,-79.2245670562819,182.2000000000001) LINKED_BODY(1)}")
    point2 = workPart.Points.CreatePoint(edge2, scalar2, NXOpen.PointCollection.PointOnCurveLocationOption.PercentParameter, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    associativeLineBuilder1.Limits.StartLimit.Distance.SetFormula("0")
    
    associativeLineBuilder1.Limits.EndLimit.Distance.SetFormula("9.38907054998417")
    
    associativeLineBuilder1.Limits.EndLimit.Distance.SetFormula("9.38907054998417")
    
    associativeLineBuilder1.EndPoint.Value = point2
    
    associativeLineBuilder1.EndPointOptions = NXOpen.Features.AssociativeLineBuilder.EndOption.Point
    
    markId5 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Line")
    
    theSession.DeleteUndoMark(markId5, None)
    
    markId6 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Line")
    
    nXObject1 = associativeLineBuilder1.Commit()
    
    theSession.DeleteUndoMark(markId6, None)
    
    theSession.SetUndoMarkName(markId4, "Line")
    
    associativeLineBuilder1.Destroy()
    
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression6)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression5)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    plane3.DestroyPlane()
    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()