import json
import NXOpen
from ui import MainUi
from utils import BasicFunctions as BF
from modules.renumber_tools import RenumberTool
from modules.create_toolpath_geo import CreateGeometry
from modules.del_all_ude import DelAllUde
from modules.axis_toolpath import CreateAxis
from pathlib import Path
from utils import Checks

theSession = NXOpen.Session.GetSession()


def main():
    themain_ui = None
    try:
        themain_ui = MainUi.main_ui(renumber_tool, tp_geo, del_ude, tool_vector_point)
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


def renumber_tool():
    config_file = Path(__file__).parent
    with open(f"{config_file}/config.json", "r") as f:
        config = json.load(f)
        versions = config["renumber_tools"]
    if Checks.check_nx_version(
        int(versions["version_max"]), int(versions["version_min"])
    ):
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
        instance = CreateGeometry()
        if instance.checkSetup and instance.checkWork:
            instance.main()


def del_ude():
    config_file = Path(__file__).parent
    with open(f"{config_file}/config.json", "r") as f:
        config = json.load(f)
        versions = config["del_all_ude"]
        if Checks.check_nx_version(
            int(versions["version_max"]), int(versions["version_min"])
        ):
            instance = DelAllUde()
            if instance.checkSetup and instance.checkWork:
                instance.main()


def tool_vector_point():
    config_file = Path(__file__).parent
    with open(f"{config_file}/config.json", "r") as f:
        config = json.load(f)
        versions = config["report_cutting_length"]
    if Checks.check_nx_version(
        int(versions["version_max"]), int(versions["version_min"])
    ):
        instance = CreateAxis()
        if instance.checkSetup and instance.checkWork:
            instance.create_axis()


if __name__ == "__main__":
    main()
