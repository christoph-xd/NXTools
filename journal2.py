# NX 2008
# Journal created by brandauc on Mon Mar 13 16:00:58 2023 W. Europe Standard Time
#
import math
import NXOpen
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display
    # ----------------------------------------------
    #   Menu: Edit->Object Display...
    # ----------------------------------------------
    markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Start")
    
    theSession.SetUndoMarkName(markId1, "Object Color Dialog")
    
    # ----------------------------------------------
    #   Dialog Begin Object Color
    # ----------------------------------------------
    markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Object Color")
    
    theSession.DeleteUndoMark(markId2, None)
    
    markId3 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Object Color")
    
    theSession.DeleteUndoMark(markId3, None)
    
    theSession.SetUndoMarkName(markId1, "Object Color")
    
    theSession.DeleteUndoMark(markId1, None)
    
    markId4 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Edit Object Display")
    
    displayModification1 = theSession.DisplayManager.NewDisplayModification()
    
    displayModification1.ApplyToAllFaces = True
    
    displayModification1.ApplyToOwningParts = False
    
    displayModification1.NewColor = 186
    
    objects1 = [NXOpen.DisplayableObject.Null] * 1 
    line1 = workPart.Lines.FindObject("ENTITY 3 137 1")
    objects1[0] = line1
    displayModification1.Apply(objects1)
    
    nErrs1 = theSession.UpdateManager.DoUpdate(markId4)
    
    displayModification1.Dispose()
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()