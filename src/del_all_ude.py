#############################################################################
#
#   Delete all Ude's in the CAM Session
#
#   Written by: Chrsitoph Brandau
##############################################################################
import NXOpen
import NXOpen.UF
import NXOpen.CAM

theSession  = NXOpen.Session.GetSession()
theUfSession  = NXOpen.UF.UFSession.GetUFSession()
workPart = theSession.Parts.Work
theUI = NXOpen.UI.GetUI()

def main():
    AllUdeTyps = [NXOpen.UF.Ude.SetType.ValueOf(0), 
                  NXOpen.UF.Ude.SetType.ValueOf(1), 
                  NXOpen.UF.Ude.SetType.ValueOf(3)]
    AllViews = [workPart.CAMSetup.GetRoot(NXOpen.CAM.CAMSetup.View.ProgramOrder), 
                workPart.CAMSetup.GetRoot(NXOpen.CAM.CAMSetup.View.MachineTool), 
                workPart.CAMSetup.GetRoot(NXOpen.CAM.CAMSetup.View.MachineMethod),
                workPart.CAMSetup.GetRoot(NXOpen.CAM.CAMSetup.View.Geometry)]
    
    for UdeType in AllUdeTyps:
        for View in AllViews:
            objects_in_view = NXOpen.CAM.NCGroup.GetMembers(View)
            pars_view(objects_in_view, UdeType)
                        
def deleteude(tagged:NXOpen.CAM.Operation, UdeType):
    theUfSession.Param.DeleteAllUdes(tagged.Tag,UdeType )

def pars_view(view, UdeType):  
    for tagged in view:
        if not tagged == 'NONE':
            if workPart.CAMSetup.IsGroup(tagged):
                group = NXOpen.CAM.NCGroup.GetMembers(tagged)
                deleteude(tagged, UdeType)
                pars_view(group, UdeType)
            else:
                deleteude(tagged, UdeType)

if __name__ == '__main__':
    main()


