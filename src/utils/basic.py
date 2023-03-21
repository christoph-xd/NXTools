import NXOpen


class BasicFunctions:
    def set_undo_mark(text: str, theSession: NXOpen.Session):
        theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, text)

    def get_language() -> str:
        lang = "EN"
        theSession = NXOpen.Session.GetSession()
        envVar = theSession.GetEnvironmentVariableValue("UGII_LANG")

        if envVar.lower() == "english":
            lang = "EN"
        elif envVar.lower() == "german":
            lang = "DE"
        else:
            lang = "EN"

        return lang

    def get_text(theDictionary, *args):
        # Gets text localized to language specified by UGII_LANG

        # If the passesd in object is not a dict then return "unknown"
        if not type(theDictionary) is dict:
            return "Unknown"

        if len(args) > 0 and args[0] == "core":
            return theDictionary["EN"]
        else:
            lang = BasicFunctions.get_language()
            if lang in theDictionary:
                return theDictionary[lang]
            elif "EN" in theDictionary:
                return theDictionary["EN"]

        # If we don't have a translation return "unknown"
        return "Unknown"
