import json
import NXOpen
from ui import MainUi
from renumber_tools import RenumberTool
from create_toolpath_geo import CreateGeometry
from pathlib import Path
from utils import Checks

def main():

    themain_ui = None
    try:
        themain_ui =  MainUi.main_ui(renumber_tool, tp_geo)
        #  The following method shows the dialog immediately
        themain_ui.Show()
    except Exception as ex:
        # ---- Enter your exception handling code here -----
        NXOpen.UI.GetUI().NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))
    finally:
        if themain_ui != None:
            themain_ui.Dispose()
            themain_ui = None


def renumber_tool():
    config_file = Path(__file__).parent
    with open(f"{config_file}/config.json", "r") as f:
        config = json.load(f)
        versions = config["renumber_tools"]
    if Checks.check_nx_version(int(versions["version_max"]), int(versions["version_min"])):
        instance = RenumberTool()
        instance.main()
        
def tp_geo():
    config_file = Path(__file__).parent
    with open(f"{config_file}/config.json", "r") as f:
        config = json.load(f)
        report_json = config["report_cutting_length"]
    if Checks.check_nx_version(
        int(report_json["version_max"]), int(report_json["version_min"])
    ):
        inistance = CreateGeometry()
        inistance.main()
        
def del_ude():
    pass

if __name__ == "__main__":
    main()
