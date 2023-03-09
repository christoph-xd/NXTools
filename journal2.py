# NX 2008
# Journal created by brandauc on Thu Mar  9 12:28:13 2023 W. Europe Standard Time
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
    #   Menu: Insert->Datum->Datum Axis...
    # ----------------------------------------------
    markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
    
    datumAxisBuilder1 = workPart.Features.CreateDatumAxisBuilder(NXOpen.Features.Feature.Null)
    
    datumAxisBuilder1.IsAssociative = True
    
    theSession.SetUndoMarkName(markId1, "Datum Axis Dialog")
    
    datumAxisBuilder1.Type = NXOpen.Features.DatumAxisBuilder.Types.TwoPoints
    
    datumAxisBuilder1.ResizedEndDistance = 0.0
    
    unit1 = datumAxisBuilder1.ArcLength.Expression.Units
    
    expression1 = workPart.Expressions.CreateSystemExpressionWithUnits("0", unit1)
    
    datumAxisBuilder1.Type = NXOpen.Features.DatumAxisBuilder.Types.PointAndDir
    
    datumAxisBuilder1.ResizedEndDistance = 0.0
    
    expression2 = workPart.Expressions.CreateSystemExpressionWithUnits("0", unit1)
    
    point1 = workPart.Points.FindObject("ENTITY 2 1 1")
    point2 = workPart.Points.CreatePoint(point1, NXOpen.Xform.Null, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    datumAxisBuilder1.Point = point2
    
    expression3 = workPart.Expressions.CreateSystemExpressionWithUnits("0", unit1)
    
    point3 = workPart.Points.CreatePoint(point1, NXOpen.Xform.Null, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    origin1 = NXOpen.Point3d(0.0, 0.0, 0.0)
    vector1 = NXOpen.Vector3d(0.0, 0.0, 1.0)
    direction1 = workPart.Directions.CreateDirection(origin1, vector1, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    datumAxisBuilder1.Vector = direction1
    
    markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Datum Axis")
    
    theSession.DeleteUndoMark(markId2, None)
    
    markId3 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Datum Axis")
    
    datumAxisBuilder1.ResizedEndDistance = 13.495076314175407
    
    datumAxisBuilder1.ArcLength.Update(NXOpen.GeometricUtilities.OnPathDimensionBuilder.UpdateReason.Path)
    
    nXObject1 = datumAxisBuilder1.Commit()
    
    theSession.DeleteUndoMark(markId3, None)
    
    theSession.SetUndoMarkName(markId1, "Datum Axis")
    
    datumAxisBuilder1.Destroy()
    
    workPart.MeasureManager.SetPartTransientModification()
    
    workPart.Expressions.Delete(expression2)
    
    workPart.MeasureManager.ClearPartTransientModification()
    
    workPart.MeasureManager.SetPartTransientModification()
    
    workPart.Expressions.Delete(expression1)
    
    workPart.MeasureManager.ClearPartTransientModification()
    
    workPart.MeasureManager.SetPartTransientModification()
    
    workPart.Expressions.Delete(expression3)
    
    workPart.MeasureManager.ClearPartTransientModification()
    
    workPart.Points.DeletePoint(point3)
    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()