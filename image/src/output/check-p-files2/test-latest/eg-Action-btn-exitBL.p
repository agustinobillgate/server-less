DEFINE TEMP-TABLE action LIKE eg-action.

DEF INPUT PARAMETER TABLE FOR action.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER a AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

DEFINE BUFFER queri FOR eg-action.

FIND FIRST action.
IF case-type = 1 THEN
DO :
    CREATE eg-action.
    BUFFER-COPY action TO eg-action.
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST eg-action WHERE RECID(eg-action) = rec-id.
    FIND FIRST queri WHERE queri.actionnr = action.actionnr AND ROWID(queri) NE ROWID(eg-action) NO-LOCK NO-ERROR.
    IF AVAILABLE queri THEN
    DO:
        fl-code = 1.
        RETURN NO-APPLY.
    END.
    ELSE
    DO:
        FIND FIRST queri WHERE queri.bezeich = action.bezeich AND queri.maintask = action.maintask AND
            ROWID(queri) NE ROWID(eg-action) NO-LOCK NO-ERROR.
        IF AVAILABLE queri THEN
        DO:
            fl-code = 2.
            RETURN NO-APPLY.
        END.
        ELSE
        DO:
            FIND CURRENT eg-action EXCLUSIVE-LOCK NO-ERROR.

            BUFFER-COPY action TO eg-action.
            ASSIGN eg-action.usefor = a. 

            FIND CURRENT eg-action NO-LOCK.
            fl-code = 3.
        END.
    END.
END.
