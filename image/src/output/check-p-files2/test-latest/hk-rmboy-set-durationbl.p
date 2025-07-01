DEFINE INPUT PARAMETER userinit AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER zinr AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER duration AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str AS CHAR NO-UNDO.

DEFINE VARIABLE ci-date AS DATE.

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate.         /* Rulita 211024 | Fixing for serverless */

FIND FIRST queasy WHERE queasy.KEY EQ 196 AND queasy.date1 EQ ci-date AND ENTRY(1,queasy.char1,";") EQ zinr EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    IF queasy.char2 EQ userinit THEN
    DO:
        queasy.number2 = TIME.
    END.
    ELSE
    DO:
        FIND FIRST bediener WHERE bediener.userinit EQ queasy.char2 NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            IF INT(SUBSTRING(bediener.permissions,82,1)) GE 2 THEN
            DO:
                queasy.number2 = TIME.
            END.
            ELSE
            DO:
                msg-str = "Room " + zinr + " is being cleaned by " + bediener.username.
            END.
        END.
    END.
END.
FIND CURRENT queasy NO-LOCK NO-ERROR.
RELEASE queasy.
