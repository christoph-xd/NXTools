import NXOpen
import NXOpen.UF
import sys
import math
import NXOpen
from typing import List, cast, Optional, Union

the_session: NXOpen.Session = NXOpen.Session.GetSession()
base_part = the_session.Parts.BaseWork
the_lw: NXOpen.ListingWindow = the_session.ListingWindow


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


def main():
    the_lw.Open()
    the_lw.WriteFullline("Starting Main() in " + the_session.ExecutingJournal)

    log_file_name: str = the_session.LogFile.FileName
    with open(log_file_name, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.find("Sold") != -1:
                sold_to_id: str = line.split(":")[1].strip()
                the_lw.WriteFullline(sold_to_id)


if __name__ == "__main__":
    main()
