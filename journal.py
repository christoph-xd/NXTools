# NX 2008
# Journal created by brandauc on Thu Mar 16 09:16:18 2023 W. Europe Standard Time
#
import math
import NXOpen
import NXOpen.Assemblies
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display
    # ----------------------------------------------
    #   Menu: Information->Object...
    # ----------------------------------------------
    selectedObjects1 = [NXOpen.NXObject.Null] * 1 
    component1 = workPart.ComponentAssembly.RootComponent.FindObject("COMPONENT Form 1")
    face1 = component1.FindObject("PROTO#.Features|UNPARAMETERIZED_FEATURE(1)|FACE 5 1 {(62.5,62.5,0) UNPARAMETERIZED_FEATURE(1)}")
    selectedObjects1[0] = face1
    theSession.Information.DisplayObjectsDetails(selectedObjects1)
    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()