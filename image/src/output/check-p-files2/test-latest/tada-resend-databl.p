DEFINE TEMP-TABLE log-list
    FIELD nr        AS INT
    FIELD send-date AS DATE
    FIELD data-date AS DATE
    FIELD deptnr    AS INT
    FIELD filenames AS CHAR
    FIELD send-status AS LOGICAL
    FIELD rec-id      AS INT.

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT PARAMETER send-date AS DATE.
DEFINE INPUT PARAMETER rec-id    AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR log-list.

DEF VAR nr AS INT.
IF case-type EQ 1 THEN
DO:
    /*
    FIND FIRST queasy WHERE queasy.KEY EQ 270 
        AND queasy.number1 EQ 99 
        AND queasy.date1 EQ send-date
        /*AND queasy.betriebsnr EQ dept*/ NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        queasy.logi1 = NO.
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.
    */
    FIND FIRST queasy WHERE RECID(queasy) EQ rec-id NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        queasy.logi1 = NO.
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.
END.

FOR EACH queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 99 
    /*AND queasy.betriebsnr EQ dept*/ NO-LOCK:
    nr = nr + 1.
    CREATE log-list.
    ASSIGN 
       log-list.nr          = nr 
       log-list.send-date   = queasy.date1
       log-list.data-date   = queasy.date2
       log-list.deptnr      = queasy.betriebsnr
       log-list.filenames   = queasy.char1
       log-list.send-status = queasy.logi1
       log-list.rec-id      = RECID(queasy)
        .
END.
