DEFINE TEMP-TABLE location LIKE eg-location.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER TABLE FOR location.

FIND FIRST location.
IF case-type = 1 THEN
DO:
    CREATE eg-location.
    BUFFER-COPY location TO eg-location.
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST eg-location WHERE RECID(eg-location) = rec-id.
    FIND CURRENT eg-location EXCLUSIVE-LOCK NO-ERROR.
    BUFFER-COPY location TO eg-location.
    FIND CURRENT eg-location NO-LOCK.
END.
