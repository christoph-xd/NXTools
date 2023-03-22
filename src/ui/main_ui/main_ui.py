﻿# ==============================================================================
#   WARNING!!  This file is overwritten by the Block UI Styler while generating
#   the automation code. Any modifications to this file will be lost after
#   generating the code again.
#
#        Filename:  D:\GitHub\NXTools\src\ui\main_ui\main_ui.py
#
#         This file was generated by the NX Block UI Styler
#         Created by: brandauc
#               Version: NX 2008
#               Date: 03-22-2023  (Format: mm-dd-yyyy)
#               Time: 14:28 (Format: hh-mm)
#
# ==============================================================================

# ==============================================================================
#   Purpose:  This TEMPLATE file contains Python source to guide you in the
#   construction of your Block application dialog. The generation of your
#   dialog file (.dlx extension) is the first step towards dialog construction
#   within NX.  You must now create a NX Open application that
#   utilizes this file (.dlx).
#
#   The information in this file provides you with the following:
#
#   1.  Help on how to load and display your Block UI Styler dialog in NX
#       using APIs provided in NXOpen.BlockStyler namespace
#   2.  The empty callback methods (stubs) associated with your dialog items
#       have also been placed in this file. These empty methods have been
#       created simply to start you along with your coding requirements.
#       The method name, argument list and possible return values have already
#       been provided for you.
# ==============================================================================

# ------------------------------------------------------------------------------
# These imports are needed for the following template code
# ------------------------------------------------------------------------------
import NXOpen
import NXOpen.BlockStyler
import os
from pathlib import Path


# ------------------------------------------------------------------------------
# Represents Block Styler application cls
# ------------------------------------------------------------------------------
class main_ui:
    # static class members
    theSession = None
    theUI = None

    # ------------------------------------------------------------------------------
    # Constructor for NX Styler class
    # ------------------------------------------------------------------------------
    def __init__(self, callbackRenumber, callbackTpGeo):
        try:
            self.theSession = NXOpen.Session.GetSession()
            self.theUI = NXOpen.UI.GetUI()
            self.theDlxFileName = os.path.join(Path(__file__).parent,"main_ui.dlx")
            self.theDialog = self.theUI.CreateDialog(self.theDlxFileName)
            self.theDialog.AddUpdateHandler(self.update_cb)
            self.theDialog.AddInitializeHandler(self.initialize_cb)
            self.theDialog.AddDialogShownHandler(self.dialogShown_cb)

            self.renumber = callbackRenumber
            self.tp_geo = callbackTpGeo
        except Exception as ex:
            # ---- Enter your exception handling code here -----
            raise ex

    # ------------------------------- DIALOG LAUNCHING ---------------------------------
    #
    #     Before invoking this application one needs to open any part/empty part in NX
    #     because of the behavior of the blocks.
    #
    #     Make sure the dlx file is in one of the following locations:
    #         1.) From where NX session is launched
    #         2.) $UGII_USER_DIR/application
    #         3.) For released applications, using UGII_CUSTOM_DIRECTORY_FILE is highly
    #             recommended. This variable is set to a full directory path to a file
    #             containing a list of root directories for all custom applications.
    #             e.g., UGII_CUSTOM_DIRECTORY_FILE=$UGII_BASE_DIR\ugii\menus\custom_dirs.dat
    #
    #     You can create the dialog using one of the following way:
    #
    #     1. Journal Replay
    #
    #         1) Replay this file through Tool->Journal->Play Menu.
    #
    #     2. USER EXIT
    #
    #         1) Create the Shared Library -- Refer "Block UI Styler programmer's guide"
    #         2) Invoke the Shared Library through File->Execute->NX Open menu.
    #
    # ------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------
    # This method shows the dialog on the screen
    # ------------------------------------------------------------------------------
    def Show(self):
        try:
            self.theDialog.Show()
        except Exception as ex:
            # ---- Enter your exception handling code here -----
            self.theUI.NXMessageBox.Show(
                "Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex)
            )

    # ------------------------------------------------------------------------------
    # Method Name: Dispose
    # ------------------------------------------------------------------------------
    def Dispose(self):
        if self.theDialog != None:
            self.theDialog.Dispose()
            self.theDialog = None

    # ------------------------------------------------------------------------------
    # ---------------------Block UI Styler Callback Functions--------------------------
    # ------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------
    # Callback Name: initialize_cb
    # ------------------------------------------------------------------------------
    def initialize_cb(self):
        try:
            self.numberTools_btn = self.theDialog.TopBlock.FindBlock("numberTools_btn")
            self.tpGeo_btn = self.theDialog.TopBlock.FindBlock("tpGeo_btn")
            self.button0 = self.theDialog.TopBlock.FindBlock("button0")
        except Exception as ex:
            # ---- Enter your exception handling code here -----
            self.theUI.NXMessageBox.Show(
                "Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex)
            )

    # ------------------------------------------------------------------------------
    # Callback Name: dialogShown_cb
    # This callback is executed just before the dialog launch. Thus any value set
    # here will take precedence and dialog will be launched showing that value.
    # ------------------------------------------------------------------------------
    def dialogShown_cb(self):
        try:
            # ---- Enter your callback code here -----
            pass
        except Exception as ex:
            # ---- Enter your exception handling code here -----
            self.theUI.NXMessageBox.Show(
                "Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex)
            )

    # ------------------------------------------------------------------------------
    # Callback Name: update_cb
    # ------------------------------------------------------------------------------
    def update_cb(self, block):
        try:
            if block == self.numberTools_btn:
                self.renumber()
                pass
            elif block == self.tpGeo_btn:
                self.tp_geo()
                pass
            elif block == self.button0:
                # ---- Enter your code here -----
                pass
        except Exception as ex:
            # ---- Enter your exception handling code here -----
            self.theUI.NXMessageBox.Show(
                "Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex)
            )

        return 0

    # ------------------------------------------------------------------------------
    # Function Name: GetBlockProperties
    # Returns the propertylist of the specified BlockID
    # ------------------------------------------------------------------------------
    def GetBlockProperties(self, blockID):
        try:
            return self.theDialog.GetBlockProperties(blockID)
        except Exception as ex:
            # ---- Enter your exception handling code here -----
            self.theUI.NXMessageBox.Show(
                "Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex)
            )

        return None


def main():
    themain_ui = None
    try:
        themain_ui = main_ui()
        #  The following method shows the dialog immediately
        themain_ui.Show()
    except Exception as ex:
        # ---- Enter your exception handling code here -----
        NXOpen.UI.GetUI().NXMessageBox.Show(
            "Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex)
        )
    finally:
        if themain_ui != None:
            themain_ui.Dispose()
            themain_ui = None


if __name__ == "__main__":
    main()
