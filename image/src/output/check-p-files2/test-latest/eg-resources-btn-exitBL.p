DEFINE TEMP-TABLE resources LIKE eg-resources.

DEF INPUT PARAMETER TABLE FOR resources.
DEF INPUT PARAMETER case-type   AS INT.
DEF INPUT PARAMETER rec-id      AS INT.
DEF INPUT PARAMETER fibukonto   AS CHAR.

FIND FIRST resources.
IF case-type = 1 THEN
DO :
    CREATE eg-resources.
    BUFFER-COPY resources TO eg-resources.
    ASSIGN eg-resources.char1 = fibukonto.
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST eg-resources WHERE RECID(eg-resources) = rec-id.
    FIND CURRENT eg-resources EXCLUSIVE-LOCK NO-ERROR.
    BUFFER-COPY resources TO eg-resources.
    ASSIGN eg-resources.char1 = fibukonto.
    FIND CURRENT eg-resources NO-LOCK.
END.
