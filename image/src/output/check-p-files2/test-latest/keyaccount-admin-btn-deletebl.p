DEF INPUT PARAMETER number1 AS INT.
DEF INPUT PARAMETER user-init AS CHAR.

DEF OUTPUT PARAMETER str-msg AS CHAR.

DEFINE BUFFER   q212        FOR queasy.
DEFINE VARIABLE category    AS CHARACTER.
DEFINE VARIABLE num1        AS INTEGER.
DEFINE VARIABLE nr          AS INTEGER INIT 0.

FIND FIRST queasy WHERE queasy.KEY = 211
    AND queasy.number1 = number1 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    FIND CURRENT queasy EXCLUSIVE-LOCK.
    FIND FIRST q212 WHERE q212.KEY EQ 212 AND q212.number1 EQ queasy.number1 NO-LOCK NO-ERROR.
    IF AVAILABLE q212 THEN
    DO:
        str-msg = "Member entries exist, deleting KeyAccount not possible".
    END.
    ELSE
    DO:
        str-msg = "".
        category = queasy.char1.
        DELETE queasy.
        RELEASE queasy.

        FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            CREATE res-history.
            ASSIGN
                res-history.nr          = bediener.nr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.aenderung   = "Delete KeyAccount, Name: " + category
                res-history.action      = "Key Account".
            FIND CURRENT res-history NO-LOCK.
            RELEASE res-history.
        END.

        /*FOR EACH queasy WHERE queasy.KEY = 211 NO-LOCK BY queasy.number1:
            ASSIGN
                nr   = nr + 1
                num1 = queasy.number1.
            queasy.number1 = nr.
            FOR EACH q212 WHERE q212.KEY EQ
            END.
        END.*/
    END.
END.
