
DEF INPUT PARAMETER case-type   AS INT.
DEF INPUT PARAMETER int1        AS INT.
DEF OUTPUT PARAMETER fl-avail   AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER char1      AS CHAR.
DEF OUTPUT PARAMETER int2       AS INT.

IF case-type = 1 THEN
DO:
    FIND FIRST l-segment WHERE l-segment.l-segmentcode = int1 NO-LOCK NO-ERROR.
    IF AVAILABLE l-segment THEN
    DO:
        char1 = l-segment.l-bezeich.
        fl-avail = YES.
    END.
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST l-kredit WHERE RECID(l-kredit) = int1 NO-LOCK.
    IF l-kredit.opart = 2 THEN fl-avail = YES.
    int2 = l-kredit.lief-nr.
END.
