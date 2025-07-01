
DEF INPUT  PARAMETER case-type   AS INTEGER     NO-UNDO.
DEF INPUT  PARAMETER int1        AS INTEGER     NO-UNDO.
DEF INPUT  PARAMETER char1       AS CHAR        NO-UNDO.
DEF OUTPUT PARAMETER successFlag AS LOGICAL     INITIAL NO NO-UNDO.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST segment WHERE segment.segmentcode = int1
            EXCLUSIVE-LOCK.
        IF AVAILABLE segment THEN
        DO:
            DELETE segment.
            RELEASE segment.
            successFlag = YES.
        END.
    END.
END CASE.
