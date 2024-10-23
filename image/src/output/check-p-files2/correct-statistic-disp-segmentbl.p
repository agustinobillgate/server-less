DEFINE TEMP-TABLE t-segment
    FIELD segmentcode LIKE segment.segmentcode
    FIELD bezeich LIKE segment.bezeich.

DEF OUTPUT PARAMETER TABLE FOR t-segment.

FOR EACH segment:
    CREATE t-segment.
    ASSIGN
    t-segment.segmentcode = segment.segmentcode
    t-segment.bezeich = segment.bezeich.
END.
