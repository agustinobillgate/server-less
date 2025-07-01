DEFINE TEMP-TABLE trate-code LIKE queasy
    FIELD active-flag AS LOGICAL INIT NO.

DEFINE OUTPUT PARAMETER TABLE FOR trate-code.

DEFINE BUFFER bqueasy FOR queasy.

FOR EACH queasy WHERE queasy.KEY = 2
    AND queasy.logi2 = NO NO-LOCK:
    CREATE trate-code.
    BUFFER-COPY queasy TO trate-code.

    FIND FIRST bqueasy WHERE bqueasy.KEY = 264
        AND bqueasy.char1 = queasy.char1 NO-LOCK NO-ERROR.
    IF AVAILABLE bqueasy THEN ASSIGN trate-code.active-flag = bqueasy.logi1.
END.
