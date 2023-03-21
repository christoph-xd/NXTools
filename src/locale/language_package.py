################################################################################################
#
#   Purpose:
#   Language Pack for all NXTools
#
################################################################################################
#
#   Notes:
#   As standard language always english will be used
#
################################################################################################


class Core:
    Yes = {"EN": "Yes", "DE": "Ja"}
    No = {"EN": "No", "DE": "Nein"}
    UserAbort = {"EN": "User Abort", "DE": "Benutzerabbruch"}
    VersionCheckHeader = {"EN": "Version Check", "DE": "Versions Prüfung"}
    VersionCheck = {
        "EN": "The current NX Version don't match to required Version!",
        "DE": "Die aktuelle NX Version passt nicht zur Vorausgesetzten!",
    }
    WorkPartCheckHeader = {"EN": "No Work Part", "DE": "Kein Work Part"}
    WorkPartCheck = {
        "EN": "A Part must be Opened!",
        "DE": "Ein WorkPart muss geöffnet sein!",
    }
    SetupCheckHeader = {"EN": "No CAM Setup", "DE": "Kein CAM Setup"}
    SetupCheck = {"EN": "No CAM Setup is open!", "DE": "Kein CAM Setup geöffnet!"}


class DeleteAllUDE:
    AskYesNoHeader = {"EN": "Sure?", "DE": "Sicher?"}
    AskYesNo = {
        "EN": "You are Sure to delete all UDE's?",
        "DE": "Bist du sicher das alle UDE's gelöscht werden sollen?",
    }
    AskDelProgrammViewHeader = {
        "EN": "Delete UDE Program View",
        "DE": "UDE in Programm View löschen",
    }
    AskDelProgrammView = {
        "EN": "You want delete all UDE's in the Programm View?",
        "DE": "Willst du alle UDE's in der Programm View löschen?",
    }
    AskDelToolViewHeader = {
        "EN": "Delete UDE Tool View",
        "DE": "UDE in Tool View löschen",
    }
    AskDelToolView = {
        "EN": "You want delete all UDE's in the Tool View?",
        "DE": "Willst du alle UDE's in der Tool View löschen?",
    }
    AskDelGeoViewHeader = {
        "EN": "Delete UDE Geometry View",
        "DE": "UDE in Geometry View löschen",
    }
    AskDelGeoView = {
        "EN": "You want delete all UDE's in the Geometry View?",
        "DE": "Willst du alle UDE's in der Geometry View löschen?",
    }
    AskDelMethodViewHeader = {
        "EN": "Delete UDE Method View",
        "DE": "UDE in Method View löschen",
    }
    AskDelMethodView = {
        "EN": "You want delete all UDE's in the Method View?",
        "DE": "Willst du alle UDE's in der Method View löschen?",
    }


class CreateToolpathGeo:
    AskYesNoToolpathAmountHeader = {"EN": "Continue?", "DE": "Fortsetzen?"}
    AskYesNoToolpathAmount = {
        "EN": "There are a big amount of Lines!\nYou are sure you want continue?",
        "DE": "Große Anzahl an Punkten!\nWillst du fortfahren?",
    }
    ErrorNotLineHeader = {"EN": "Output Not Line!", "DE": "Ausgabe ist nicht Line!"}
    ErrorNotLine = {
        "EN": "The Operation is not Calculated in Line!",
        "DE": "Die Operation ist nicht auf Linen Berechnet!",
    }
    ErrorNotOperationHeader = {"EN": "Not an Operation", "DE": "Keine Operation"}
    ErrorNotOperation = {
        "EN": "The seleced Item isn't a Operation!",
        "DE": "Das ausgewählte Objekt ist keine Operstion!",
    }
    ErrorSelectHeader = {"EN": "Select Operation", "DE": "1 Operation wählen"}
    ErrorSelect = {
        "EN": "Please select 1 Operation!",
        "DE": "Bitte wähle 1 Operation aus!",
    }


class CreateAxisFromToolpath:
    ...


class ReportCuttingLengthLocale:
    operationName = {"EN": "Operation Name", "DE": "Operations Name"}
    toolName = {"EN": "Tool Name", "DE": "Werkzeug Name"}
    lengthCut = {"EN": "G1 Length / Time", "DE": "G1 Länge / Zeit"}
    lengthRapid = {"EN": "G0 Length / Time", "DE": "G0 Länge / Zeit"}
    selectONT = {
        "EN": "One Object must be Selected in the ONT.",
        "DE": "Es muss eine Operation im ONT ausgewählt werden.",
    }


class ReportCSETimeLocale:
    ...


class RenumberToolLocale:
    undoMark = {
        "EN": "Renumbering the Tool's",
        "DE": "Neu nummerierung der Werkzeuge"
    }