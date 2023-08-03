import os
import re
import shutil
from datetime import datetime
from pathlib import Path

import NXOpen
import NXOpen.UF


def log(output: str) -> None:
    theSession = NXOpen.Session.GetSession()
    theSession.LogFile.WriteLine(output)


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


class UI:
    theUfSession = NXOpen.UF.UFSession.GetUFSession()
    theUI = NXOpen.UI.GetUI()

    @classmethod
    def show_information(cls, titel: str, msg: str):
        cls.theUI.NXMessageBox.Show(
            titel, NXOpen.NXMessageBox.DialogType.Information, msg
        )

    @classmethod
    def user_abort(cls):
        cls.theUI.NXMessageBox.Show(
            "User Abort",
            NXOpen.NXMessageBox.DialogType.Error,
            "User Abort",
        )

    @classmethod
    def error_msg(cls, title: str, msg: str):
        """Present an NX Error Message Box

        Args:
            title (str): Headline from the MsgBox
            msg (str): text in the MsgBox
        """
        cls.theUI.cls.theUI.NXMessageBox.Show(
            title,
            NXOpen.NXMessageBox.DialogType.Error,
            msg,
        )

    @classmethod
    def ask_yes_no(cls, title: str, message: list) -> int:
        """
        Display System Information
        Args:
            title   : The Title to Display
            message : The Message to Display
            Result  : The Response

        Returns:
            int: Give the response from User Answer.
        """
        response = 0

        try:
            buttons = cls.theUfSession.Ui.MessageButtons()
            buttons.Button1 = True
            buttons.Button2 = True
            buttons.Button3 = True
            buttons.Label1 = "Yes"
            buttons.Label2 = "Abort"
            buttons.Label3 = "Next"
            buttons.Response1 = 1
            buttons.Response2 = 2
            buttons.Response3 = 3

            response = cls.theUfSession.Ui.MessageDialog(
                title,
                NXOpen.UF.Ui.MessageDialogType.MESSAGE_QUESTION,
                message,
                len(message),
                True,
                buttons,
            )
        except NXOpen.NXException as nXException:
            response = 2
            cls.theUI.NXMessageBox.Show(
                "Dialog",
                NXOpen.NXMessageBox.DialogType.Error,
                "Unable to Display Dialog. Error : " + str(nXException.Message),
            )
        return response


class DeleteNxDB:
    def __init__(self):
        self.theSession = NXOpen.Session.GetSession()
        self.theUfSession = NXOpen.UF.UFSession.GetUFSession()
        self.theUI = NXOpen.UI.GetUI()
        self.envVar = self.theSession.GetEnvironmentVariableValue(
            "UGII_CAM_LIBRARY_TOOL_METRIC_DIR"
        )
        self.regex = r"^\s*DATA\s*\|([^|]+)\|\s*\d+\s*\|"

    def read_write_db(self, file: Path):
        with open(file, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            f.truncate()
            for line in lines:
                result = re.search(self.regex, line)
                if result:
                    continue
                f.write(line)
            f.close()
        return

    def check_db_exists(self, file_path: Path):
        return Path(file_path).exists()

    def check_file_access(self, file: Path):
        return os.access(file, os.W_OK)

    def backup(self, file: Path):
        backup_file = file.parent.joinpath(
            f"{file.name}_{datetime.today().strftime('%Y-%m-%d_%Hh-%Mm')}"
        )
        shutil.copyfile(file, backup_file)
        return

    def main(self):
        dbs = list(Path(self.envVar).glob("**/*.dat"))
        for db in dbs:
            db_name = "\u0332".join(db.name)
            reponse = UI.ask_yes_no(
                f"You want Delete {db.name}", [f"You are Sure to Delete {db_name}"]
            )
            if reponse == 2:
                UI.user_abort()
                return
            if reponse == 3:
                continue
            if not self.check_file_access(db):
                lw(f"File '{db.name}' have no write permission!!")
                log(f"File '{db.name}' have no write permission!!")
                continue
            self.backup(db)
            self.read_write_db(db)
        UI.show_information(
            "All DBs are Deleted", "All NX DBs are sucsessfully deleted!"
        )
        log("dbs now empty")


if __name__ == "__main__":
    tools = DeleteNxDB()
    tools.main()
