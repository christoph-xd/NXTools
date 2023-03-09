# NX 2008
# Journal created by brandauc on Thu Mar  9 07:20:59 2023 W. Europe Standard Time
#
import math
import NXOpen
import NXOpen.Features
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display
    # ----------------------------------------------
    #   Menu: Insert->Datum->Point...
    # ----------------------------------------------
    markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
    
    unit1 = workPart.UnitCollection.FindObject("MilliMeter")
    expression1 = workPart.Expressions.CreateSystemExpressionWithUnits("0", unit1)
    
    expression2 = workPart.Expressions.CreateSystemExpressionWithUnits("p76_x=0.00000000000", unit1)
    
    expression3 = workPart.Expressions.CreateSystemExpressionWithUnits("p77_y=0.00000000000", unit1)
    
    expression4 = workPart.Expressions.CreateSystemExpressionWithUnits("p78_z=0.00000000000", unit1)
    
    expression5 = workPart.Expressions.CreateSystemExpressionWithUnits("p79_xdelta=0.00000000000", unit1)
    
    expression6 = workPart.Expressions.CreateSystemExpressionWithUnits("p80_ydelta=0.00000000000", unit1)
    
    expression7 = workPart.Expressions.CreateSystemExpressionWithUnits("p81_zdelta=0.00000000000", unit1)
    
    expression8 = workPart.Expressions.CreateSystemExpressionWithUnits("p82_radius=0.00000000000", unit1)
    
    unit2 = workPart.UnitCollection.FindObject("Degrees")
    expression9 = workPart.Expressions.CreateSystemExpressionWithUnits("p83_angle=0.00000000000", unit2)
    
    expression10 = workPart.Expressions.CreateSystemExpressionWithUnits("p84_zdelta=0.00000000000", unit1)
    
    expression11 = workPart.Expressions.CreateSystemExpressionWithUnits("p85_radius=0.00000000000", unit1)
    
    expression12 = workPart.Expressions.CreateSystemExpressionWithUnits("p86_angle1=0.00000000000", unit2)
    
    expression13 = workPart.Expressions.CreateSystemExpressionWithUnits("p87_angle2=0.00000000000", unit2)
    
    expression14 = workPart.Expressions.CreateSystemExpressionWithUnits("p88_distance=0", unit1)
    
    expression15 = workPart.Expressions.CreateSystemExpressionWithUnits("p89_arclen=0", unit1)
    
    expression16 = workPart.Expressions.CreateSystemExpressionWithUnits("p90_percent=0", NXOpen.Unit.Null)
    
    expression2.SetFormula("-261.6631227933")
    
    expression3.SetFormula("-92.1485312295")
    
    expression4.SetFormula("12.5")
    
    expression5.SetFormula("0")
    
    expression6.SetFormula("0")
    
    expression7.SetFormula("0")
    
    expression8.SetFormula("0")
    
    expression9.SetFormula("0")
    
    expression10.SetFormula("0")
    
    expression11.SetFormula("0")
    
    expression12.SetFormula("0")
    
    expression13.SetFormula("0")
    
    expression14.SetFormula("0")
    
    expression16.SetFormula("100")
    
    expression15.SetFormula("0")
    
    expression2.SetFormula("-261.6631227933")
    
    expression3.SetFormula("-92.1485312295")
    
    expression4.SetFormula("12.5")
    
    expression5.SetFormula("0")
    
    expression6.SetFormula("0")
    
    expression7.SetFormula("0")
    
    expression8.SetFormula("0")
    
    expression9.SetFormula("0")
    
    expression10.SetFormula("0")
    
    expression11.SetFormula("0")
    
    expression12.SetFormula("0")
    
    expression13.SetFormula("0")
    
    expression14.SetFormula("0")
    
    expression16.SetFormula("100")
    
    expression15.SetFormula("0")
    
    theSession.SetUndoMarkName(markId1, "Point Dialog")
    
    expression17 = workPart.Expressions.CreateSystemExpressionWithUnits("p91_x=0.00000000000", unit1)
    
    scalar1 = workPart.Scalars.CreateScalarExpression(expression17, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    expression18 = workPart.Expressions.CreateSystemExpressionWithUnits("p92_y=0.00000000000", unit1)
    
    scalar2 = workPart.Scalars.CreateScalarExpression(expression18, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    expression19 = workPart.Expressions.CreateSystemExpressionWithUnits("p93_z=0.00000000000", unit1)
    
    scalar3 = workPart.Scalars.CreateScalarExpression(expression19, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    point1 = workPart.Points.CreatePoint(scalar1, scalar2, scalar3, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    expression2.SetFormula("0")
    
    expression3.SetFormula("0")
    
    expression4.SetFormula("0")
    
    expression2.SetFormula("0.00000000000")
    
    expression3.SetFormula("0.00000000000")
    
    expression4.SetFormula("0.00000000000")
    
    expression2.SetFormula("0")
    
    expression3.SetFormula("0")
    
    expression4.SetFormula("0")
    
    expression2.SetFormula("0.00000000000")
    
    expression3.SetFormula("0.00000000000")
    
    expression4.SetFormula("0.00000000000")
    
    expression5.SetFormula("0.00000000000")
    
    expression6.SetFormula("0.00000000000")
    
    expression7.SetFormula("0.00000000000")
    
    expression8.SetFormula("0.00000000000")
    
    expression9.SetFormula("0.00000000000")
    
    expression10.SetFormula("0.00000000000")
    
    expression11.SetFormula("0.00000000000")
    
    expression12.SetFormula("0.00000000000")
    
    expression13.SetFormula("0.00000000000")
    
    expression16.SetFormula("100.00000000000")
    
    expression2.SetFormula("999")
    
    workPart.Points.DeletePoint(point1)
    
    expression2.RightHandSide = "999"
    
    expression3.RightHandSide = "0.00000000000"
    
    expression4.RightHandSide = "0.00000000000"
    
    expression20 = workPart.Expressions.CreateSystemExpressionWithUnits("p77_x=999", unit1)
    
    scalar4 = workPart.Scalars.CreateScalarExpression(expression20, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    expression21 = workPart.Expressions.CreateSystemExpressionWithUnits("p78_y=0.00000000000", unit1)
    
    scalar5 = workPart.Scalars.CreateScalarExpression(expression21, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    expression22 = workPart.Expressions.CreateSystemExpressionWithUnits("p79_z=0.00000000000", unit1)
    
    scalar6 = workPart.Scalars.CreateScalarExpression(expression22, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    point2 = workPart.Points.CreatePoint(scalar4, scalar5, scalar6, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    expression3.SetFormula("888")
    
    expression2.RightHandSide = "999"
    
    expression3.RightHandSide = "888"
    
    expression4.RightHandSide = "0.00000000000"
    
    workPart.Points.DeletePoint(point2)
    
    expression23 = workPart.Expressions.CreateSystemExpressionWithUnits("p77_x=999", unit1)
    
    scalar7 = workPart.Scalars.CreateScalarExpression(expression23, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    expression24 = workPart.Expressions.CreateSystemExpressionWithUnits("p78_y=888", unit1)
    
    scalar8 = workPart.Scalars.CreateScalarExpression(expression24, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    expression25 = workPart.Expressions.CreateSystemExpressionWithUnits("p79_z=0.00000000000", unit1)
    
    scalar9 = workPart.Scalars.CreateScalarExpression(expression25, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    point3 = workPart.Points.CreatePoint(scalar7, scalar8, scalar9, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    expression4.SetFormula("777")
    
    expression2.RightHandSide = "999"
    
    expression3.RightHandSide = "888"
    
    expression4.RightHandSide = "777"
    
    workPart.Points.DeletePoint(point3)
    
    expression26 = workPart.Expressions.CreateSystemExpressionWithUnits("p77_x=999", unit1)
    
    scalar10 = workPart.Scalars.CreateScalarExpression(expression26, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    expression27 = workPart.Expressions.CreateSystemExpressionWithUnits("p78_y=888", unit1)
    
    scalar11 = workPart.Scalars.CreateScalarExpression(expression27, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    expression28 = workPart.Expressions.CreateSystemExpressionWithUnits("p79_z=777", unit1)
    
    scalar12 = workPart.Scalars.CreateScalarExpression(expression28, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    point4 = workPart.Points.CreatePoint(scalar10, scalar11, scalar12, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Point")
    
    theSession.DeleteUndoMark(markId2, None)
    
    markId3 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Point")
    
    expression2.RightHandSide = "999"
    
    expression3.RightHandSide = "888"
    
    expression4.RightHandSide = "777"
    
    workPart.Points.DeletePoint(point4)
    
    expression29 = workPart.Expressions.CreateSystemExpressionWithUnits("p77_x=999", unit1)
    
    scalar13 = workPart.Scalars.CreateScalarExpression(expression29, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    expression30 = workPart.Expressions.CreateSystemExpressionWithUnits("p78_y=888", unit1)
    
    scalar14 = workPart.Scalars.CreateScalarExpression(expression30, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    expression31 = workPart.Expressions.CreateSystemExpressionWithUnits("p79_z=777", unit1)
    
    scalar15 = workPart.Scalars.CreateScalarExpression(expression31, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    point5 = workPart.Points.CreatePoint(scalar13, scalar14, scalar15, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    theSession.DeleteUndoMark(markId3, None)
    
    theSession.SetUndoMarkName(markId1, "Point")
    
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression2)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression3)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression4)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression5)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression6)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression7)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression8)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression9)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression10)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression11)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression12)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression13)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression14)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression15)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression16)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    workPart.MeasureManager.SetPartTransientModification()
    
    workPart.Expressions.Delete(expression1)
    
    workPart.MeasureManager.ClearPartTransientModification()
    
    point5.SetVisibility(NXOpen.SmartObject.VisibilityOption.Visible)
    
    pointFeatureBuilder1 = workPart.BaseFeatures.CreatePointFeatureBuilder(NXOpen.Features.Feature.Null)
    
    pointFeatureBuilder1.Point = point5
    
    nXObject1 = pointFeatureBuilder1.Commit()
    
    pointFeatureBuilder1.Destroy()
    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()
    
    
    
    #  expressionX = self.workPart.Expressions.CreateSystemExpressionWithUnits(
    #         str(endPoints.X), self.unit
    #     )
    #     expressionY = self.workPart.Expressions.CreateSystemExpressionWithUnits(
    #         str(endPoints.Y), self.unit
    #     )
    #     expressionZ = self.workPart.Expressions.CreateSystemExpressionWithUnits(
    #         str(endPoints.Z), self.unit
    #     )

    #     scalarX = self.workPart.Scalars.CreateScalarExpression(
    #         expressionX,
    #         NXOpen.Scalar.DimensionalityType.NotSet,
    #         NXOpen.SmartObject.UpdateOption.WithinModeling,
    #     )
    #     scalarY = self.workPart.Scalars.CreateScalarExpression(
    #         expressionY,
    #         NXOpen.Scalar.DimensionalityType.NotSet,
    #         NXOpen.SmartObject.UpdateOption.WithinModeling,
    #     )
    #     scalarZ = self.workPart.Scalars.CreateScalarExpression(
    #         expressionZ,
    #         NXOpen.Scalar.DimensionalityType.NotSet,
    #         NXOpen.SmartObject.UpdateOption.WithinModeling,
    #     )

    #     point = self.workPart.Points.CreatePoint(
    #         scalarX, scalarY, scalarZ, NXOpen.SmartObject.UpdateOption.WithinModeling
    #     )
    #     point.SetVisibility(NXOpen.SmartObject.VisibilityOption.Visible)
    #     pointFeatureBuilder1 = self.workPart.BaseFeatures.CreatePointFeatureBuilder(
    #         NXOpen.Features.Feature.Null
    #     )
    #     pointFeatureBuilder1.Point = point
    #     pointFeatureBuilder1.Commit()