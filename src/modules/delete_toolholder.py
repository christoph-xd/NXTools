import re
import os
from utils import lw
import NXOpen
import NXOpen.UF
from ui import DelToolHolderUI


class DeleteHolder:
    def __init__(self) -> None:
        self.theSession = NXOpen.Session.GetSession()
        self.theUfSession = NXOpen.UF.UFSession.GetUFSession()
        self.theUI = NXOpen.UI.GetUI()
        self.envVar = self.theSession.GetEnvironmentVariableValue(
            "UGII_CAM_LIBRARY_TOOL_METRIC_DIR"
        )

    def open_ui(self, holder: list):
        thedel_toolholder_ui = None
        try:
            thedel_toolholder_ui = DelToolHolderUI.del_toolholder_ui(holder)
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
        holder_dat = os.path.join(self.envVar, "holder_database.dat")
        with open(holder_dat, "r") as f:
            holder = []
            for line in f:
                result = re.search(r"^\s*DATA \| ([^|]+) \| \d+ \|", line)
                if result:
                    extracted_text = result.group(1).strip()
                    if not extracted_text in holder:
                        holder.append(extracted_text)
        self.open_ui(holder)

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
