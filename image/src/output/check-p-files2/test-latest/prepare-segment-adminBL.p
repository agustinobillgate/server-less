DEF TEMP-TABLE t-l-segment
    FIELD l-segmentcode LIKE l-segment.l-segmentcode
    FIELD l-bezeich     LIKE l-segment.l-bezeich.

DEF OUTPUT PARAMETER TABLE FOR t-l-segment.

FOR EACH l-segment:
    CREATE t-l-segment.
    ASSIGN
    t-l-segment.l-segmentcode = l-segment.l-segmentcode
    t-l-segment.l-bezeich     = l-segment.l-bezeich.
END.
