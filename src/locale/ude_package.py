class UdeName:
    udes = {
        "ude_h2_angle_alpha_cycle800": "Alpha Angle CYCLE800 (DMG)",
        "h2_axis_limit_custom": "Axis Limit B-Axis (DMG)",
        "dmg_axis_output": "Axis Output (DMG)",
        "ude_dmg_spaenefoerderer": "Chip Conveyor (DMG)",
        "ude_dmg_spaenespuelung": "Chip Flushing (DMG)",
        "ude_dmg_Kuehlung": "Coolant (DMG)",
        "DMG_set_polar_head_table": "Coordinate Output Mode (DMG)",
        "DMG_CR_ausgabe": "CR-Output (DMG)",
        "DMG_Cycle800Options": "Cycle800 Options (DMG)",
        "ude_drilling_cycle_param": "Drilling Cycle Parameters (DMG)",
        "feed_rate_in_variable": "Feed in Variable (DMG)",
        "DMG_FirstMotionToStartPoint": "First Motion to Start Point (DMG)",
        "dmg_form_groups": "Form Groups (DMG)",
        "header": "Header (DMG)",
        "HighSpeedSettings_AdvancedTopSurface": "High Speed Settings (DMG)",
        "High_Speed_Settings_HSC": "High Speed Settings ATC (DMG)",
        "InsertPosition": "Insert Position (DMG)",
        "insert": "Insert",
        "ude_dmg_oelnebelabsagung": "Oil Mist Extraction (DMG)",
        "operator_message": "Operator Message",
        "opskip_off": "Optional Skip Off",
        "opskip_on": "Optional Skip On",
        "opstop": "Optional Stop",
        "DMG_OriginSettings": "Origin (DMG)",
        "DMG_tool_offset_check": "Tool- / Offsetcheck (DMG)",
        "dmg_kreisbogen_linear_ausgabe": "Output Circular / Linear (DMG)",
        "DmgCompensationProcessingTime": "Processing Time Compensation (DMG)",
        "DMG_RoofRinsing": "Roof Rinsing (DMG)",
        "rotate": "Rotate",
        "DMG_safe_motion_general": "Safe Motion General (DMG)",
        "DMG_safe_motion_on_operation": "Safe Motion on Operation (DMG)",
        "stop": "Stop",
        "dmg_tool_breakage_control": "Tool Breakage Control 9908 (BLUM)",
        "ude_tool_change": "Tool Change (DMG)",
        "dmg_tool_length_radius_messuring": "Tool Length/Radius Measuring 9903 (BLUM)",
        "dmg_tool_length_messuring": "Tool Length Measuring 9902 (BLUM)",
        "WorkpieceNew": "Workpiece (DMG)",
        "h2_first_pos_manuel_input": "Avoidance Position manual (DMG)",
    }

    @classmethod
    def get_ude_name(cls, event_name):

        if event_name in cls.udes:
            return cls.udes[event_name]
        return event_name
