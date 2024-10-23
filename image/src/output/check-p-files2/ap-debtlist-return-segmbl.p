
DEF INPUT PARAMETER segm AS INT.
DEF OUTPUT PARAMETER avail-l-segment AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER segm-bezeich AS CHAR.

FIND FIRST l-segment WHERE l-segment.l-segmentcode = segm NO-LOCK NO-ERROR.
IF AVAILABLE l-segment THEN
DO:
    avail-l-segment = YES.
    segm-bezeich = l-segment.l-bezeich.
END.
