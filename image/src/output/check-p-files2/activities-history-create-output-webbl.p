DEFINE TEMP-TABLE b1-list
    FIELD datum     AS CHAR
    FIELD action    LIKE res-history.action
    FIELD aenderung LIKE res-history.aenderung
    FIELD username  LIKE bediener.username
    FIELD zeit      AS CHAR.
    /* INDEX idx       IS PRIMARY UNIQUE zeit. */

/* */
DEFINE INPUT PARAMETER idFlag       AS CHAR.
DEFINE OUTPUT PARAMETER doneFlag    AS LOGICAL NO-UNDO INITIAL NO.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR b1-list.

/* 
DEFINE VARIABLE idFlag AS CHAR.
DEFINE VARIABLE doneFlag AS LOGICAL.

idFlag = "".
doneFlag = ?.
*/

DEFINE VARIABLE counter   AS INTEGER NO-UNDO INITIAL 0.

DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER pqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.

FOR EACH queasy WHERE queasy.KEY = 280 AND queasy.char1 = "System Logfiles"
    AND queasy.char2 = idFlag NO-LOCK BY queasy.number1:

        ASSIGN counter = counter + 1.
        IF counter GT 1000 THEN LEAVE.

        CREATE b1-list.
        ASSIGN
            b1-list.datum       = ENTRY(1, queasy.char3, "$")
            b1-list.action      = ENTRY(2, queasy.char3, "$")
            b1-list.aenderung   = ENTRY(3, queasy.char3, "$")
            b1-list.username    = ENTRY(4, queasy.char3, "$")
            b1-list.zeit        = STRING(ENTRY(5, queasy.char3, "$"))
        .

        FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(queasy) EXCLUSIVE-LOCK.
        DELETE bqueasy.
        RELEASE bqueasy. 
END. 

FIND FIRST pqueasy WHERE pqueasy.KEY = 280
    AND pqueasy.char1 = "System Logfiles"
    AND pqueasy.char2 = idFlag NO-LOCK NO-ERROR.
IF AVAILABLE pqueasy THEN DO:
    ASSIGN doneFlag = NO.
END.
ELSE DO:
    FIND FIRST tqueasy WHERE tqueasy.KEY = 285
        AND tqueasy.char1 = "System Logfiles"
        AND tqueasy.number1 = 1
        AND tqueasy.char2 = idFlag NO-LOCK NO-ERROR.
    IF AVAILABLE tqueasy THEN DO:
        ASSIGN doneFlag = NO.
    END.
    ELSE DO:
        ASSIGN doneFlag = YES.
    END.
END.

FIND FIRST tqueasy WHERE tqueasy.KEY = 285
    AND tqueasy.char1 = "System Logfiles"
    AND tqueasy.number1 = 0
    AND tqueasy.char2 = idFlag NO-LOCK NO-ERROR.
IF AVAILABLE tqueasy THEN DO:
    FIND CURRENT tqueasy EXCLUSIVE-LOCK.
    DELETE tqueasy.
    RELEASE tqueasy.
END.

