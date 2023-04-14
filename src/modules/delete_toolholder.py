import re
import os
import shutil
from utils import lw, log
import NXOpen
import NXOpen.UF
from ui import DelToolHolderUI


class DeleteHolder:
    def __init__(self, isDebug) -> None:
        self.theSession = NXOpen.Session.GetSession()
        self.theUfSession = NXOpen.UF.UFSession.GetUFSession()
        self.theUI = NXOpen.UI.GetUI()
        self.isDebug = isDebug
        self.envVar = self.theSession.GetEnvironmentVariableValue(
            "UGII_CAM_LIBRARY_TOOL_METRIC_DIR"
        )
        self.holder_dat = os.path.join(self.envVar, "holder_database.dat")
        self.holder_dat_bck = os.path.join(self.envVar, "holder_database.bck")
        self.regex = r"^\s*DATA\s* \| ([^|]+) \| \d+ \|"

    def get_holder_names(self) -> list:
        if self.isDebug:
            log(" ")
            log(self.holder_dat)
            lw(self.holder_dat)
            log(" ")
        with open(self.holder_dat, "r") as f:
            holder = []
            for line in f:
                result = re.search(self.regex, line)
                if result:
                    extracted_text = result.group(1).strip()
                    if not extracted_text in holder:
                        holder.append(extracted_text)
        return holder

    def delete_holder(self, holder_name):

        if os.path.exists(self.holder_dat_bck):
            os.remove(self.holder_dat_bck)

        shutil.copyfile(self.holder_dat, self.holder_dat_bck)
        with open(self.holder_dat, "w") as f:
            for line in f:
                result = re.search(self.regex, line)
                if result:
                    extracted_text = result.group(1).strip()
                    if extracted_text == holder_name:
                        continue
                f.write(line)
        from pathlib import Path
        os.startfile(Path(self.holder_dat).parent)

    def open_ui(self):
        thedel_toolholder_ui = None
        try:
            thedel_toolholder_ui = DelToolHolderUI.del_toolholder_ui(
                self.get_holder_names(), self.delete_holder)
            #  The following method shows the dialog immediately
            thedel_toolholder_ui.Launch()
        except Exception as ex:
            # ---- Enter your exception handling code here -----
            NXOpen.UI.GetUI().NXMessageBox.Show(
                "Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex)
            )
        finally:
            if thedel_toolholder_ui != None:
                thedel_toolholder_ui.Dispose()
                thedel_toolholder_ui = None

    def main(self):
        self.open_ui()

        pass


if __name__ == "__main__":
    instance = DeleteHolder()
    instance.main()

# string = "DATA |  HLD001_00001  | 1 | 1 | 0 | 3 | 0.00000 | 0.00000 | 0.00000 |  Small collet"

# result = re.search(r"\| ([^|]+) \| \d+ \|", string)

# if result:
#     extracted_text = result.group(1).strip()
#     print(extracted_text)
# else:
#     print("Match not found.")
