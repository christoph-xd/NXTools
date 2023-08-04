import NXOpen
import NXOpen.UF


def lw(output: str):
    """
    Write a line in the NX Listing Window
    Args:
        output   : The Output which will shown in the NX Listing Window
    """
    theSession = NXOpen.Session.GetSession()
    if not theSession.ListingWindow.IsOpen:
        theSession.ListingWindow.Open()
    else:
        pass
    theSession.ListingWindow.WriteFullline(str(output))
    theSession.ListingWindow.Close()


theSession = NXOpen.Session.GetSession()
theUfSession = NXOpen.UF.UFSession.GetUFSession()

lw(dir(theUfSession.Mom.AskMom(456)))
