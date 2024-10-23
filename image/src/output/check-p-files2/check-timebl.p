DEF INPUT  PARAMETER case-type  AS INT.
DEF INPUT  PARAMETER id-table   AS INT.
DEF INPUT  PARAMETER id-table1  AS INT.
DEF INPUT  PARAMETER name-table AS CHAR.
DEF INPUT  PARAMETER init-time2 AS INT.
DEF INPUT  PARAMETER init-date2 AS DATE.

DEF OUTPUT PARAMETER flag-ok    AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER init-time1 AS INT.
DEF OUTPUT PARAMETER init-date1 AS DATE.

DEFINE VARIABLE delta-time  AS INTEGER NO-UNDO.

DEF VAR init-time AS INT.
DEF VAR init-date AS DATE.
DEF VAR setting-time AS INT.
setting-time = (3 * 60).

ASSIGN
    init-time  = TIME
    init-date  = TODAY
    init-time1 = init-time
    init-date1 = init-date.

IF case-type = 1 THEN   /* wktu prepare */
DO:
    IF id-table1 NE ? THEN
    FIND FIRST queasy WHERE queasy.KEY = 9999 
        AND queasy.char1 = name-table 
        AND queasy.number2 = id-table 
        AND queasy.number3 = id-table1 
        NO-LOCK NO-ERROR.
    ELSE
    FIND FIRST queasy WHERE queasy.KEY = 9999 
        AND queasy.char1 = name-table 
        AND queasy.number2 = id-table NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        delta-time = (TIME - INTEGER(queasy.number1))
                + (TODAY - queasy.date1) * 24 * 3600 .
        IF delta-time LT setting-time THEN RETURN.
        ELSE
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            ASSIGN
                queasy.number1 = init-time
                queasy.date1 = init-date.
            FIND CURRENT queasy NO-LOCK.
            flag-ok = YES.
        END.

        /*MT
        IF init-date > queasy.date1 THEN /* ganti hari */
        DO:
            IF (queasy.number1 - init-time) > setting-time THEN
            DO:
                FIND CURRENT queasy EXCLUSIVE-LOCK.
                ASSIGN
                    queasy.number1 = init-time
                    queasy.date1 = init-date.
                FIND CURRENT queasy NO-LOCK.
                flag-ok = YES.
            END.
            ELSE
            DO:
                RETURN. /* modified */
            END.
        END.
        ELSE
        DO:
            IF (init-time - queasy.number1) > setting-time THEN
            DO:
                FIND CURRENT queasy EXCLUSIVE-LOCK.
                ASSIGN
                    queasy.number1 = init-time
                    queasy.date1 = init-date.
                FIND CURRENT queasy NO-LOCK.
                flag-ok = YES.
            END.
            ELSE
            DO:
                RETURN. /* modified */
            END.
        END.
        */
    END.
    ELSE
    DO:
        CREATE queasy.
        ASSIGN
            queasy.KEY = 9999
            queasy.char1 = name-table
            queasy.number1 = init-time
            queasy.number2 = id-table
            queasy.date1 = init-date.
        IF id-table1 NE ? THEN
            ASSIGN queasy.number3 = id-table1.
        flag-ok = YES.
    END.
END.
ELSE IF case-type = 2 THEN   /* wktu stop */
DO:
    IF id-table1 NE ? THEN
    FIND FIRST queasy WHERE queasy.KEY = 9999 
        AND queasy.char1 = name-table 
        AND queasy.number2 = id-table 
        AND queasy.number3 = id-table1 
        NO-LOCK NO-ERROR.
    ELSE
    FIND FIRST queasy WHERE queasy.KEY = 9999 
        AND queasy.char1 = name-table 
        AND queasy.number2 = id-table NO-LOCK NO-ERROR.

    IF AVAILABLE queasy THEN
    DO:
        IF init-date2 = queasy.date1 AND init-time2 = queasy.number1 THEN
        DO:
            FIND CURRENT queasy.
            DELETE queasy.
            RELEASE queasy.
            flag-ok = YES.
        END.
    END.
END.
ELSE IF case-type = 3 THEN   /* wktu btn-go */
DO:
    IF id-table1 NE ? THEN
    FIND FIRST queasy WHERE queasy.KEY = 9999 
        AND queasy.char1 = name-table 
        AND queasy.number2 = id-table 
        AND queasy.number3 = id-table1 
        NO-LOCK NO-ERROR.
    ELSE
    FIND FIRST queasy WHERE queasy.KEY = 9999 
        AND queasy.char1 = name-table 
        AND queasy.number2 = id-table NO-LOCK NO-ERROR.

    IF AVAILABLE queasy THEN
    DO:
        IF init-date2 = queasy.date1 AND init-time2 = queasy.number1 THEN
            flag-ok = YES.
    END.
END.
