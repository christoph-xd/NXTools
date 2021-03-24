# NX 1911
# Journal created by brandauc on Wed Apr 22 13:07:48 2020 Mitteleuropäische Sommerzeit
#
#
import math
import NXOpen
import shutil
import os
import getpass
import time
import subprocess

def main() : 
    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display
    
    full_path = theSession.Parts.Work.FullPath
    partname = os.path.basename(full_path)
    pathname = os.path.dirname(full_path)

    os.startfile(pathname)

if __name__ == '__main__':
    main()