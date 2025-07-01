
/*naufal 230920 - perbaikan validasi saat delete guest*/
DEFINE TEMP-TABLE temp-list
    FIELD number1       AS INTEGER   FORMAT ">>>>>"
    FIELD number2       AS INTEGER   FORMAT ">>>"
    FIELD char1         AS CHARACTER FORMAT "x(50)"
    FIELD number3       AS INTEGER   FORMAT ">>>>>>>>>>"
    FIELD category      AS CHARACTER FORMAT "x(40)".

DEFINE INPUT PARAMETER selected-guest AS INTEGER.
DEFINE INPUT PARAMETER user-init      AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR temp-list.

DEFINE VARIABLE num1        AS INTEGER.
DEFINE VARIABLE nr          AS INTEGER INIT 0.
DEFINE VARIABLE category    AS CHARACTER.
DEFINE BUFFER b-queasy FOR queasy.

FIND FIRST queasy WHERE queasy.KEY = 282
    AND queasy.number3 = selected-guest NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    num1 = queasy.number1.
    FIND CURRENT queasy EXCLUSIVE-LOCK.
    DELETE queasy.
    RELEASE queasy.

    FIND FIRST b-queasy WHERE b-queasy.KEY EQ 281 AND b-queasy.number1 EQ num1 NO-LOCK NO-ERROR.
    IF AVAILABLE b-queasy THEN
    DO:
        category = b-queasy.char1.
    END.

    FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        CREATE res-history.
        ASSIGN
            res-history.nr          = bediener.nr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.aenderung   = "Delete Guest from KeyAccount, GuestNo: " + STRING(selected-guest) + " KeyAccount: " + category
            res-history.action      = "Key Account".
        FIND CURRENT res-history NO-LOCK.
        RELEASE res-history.
    END.
END.

FOR EACH queasy WHERE queasy.KEY = 282 AND queasy.number1 = num1:
    ASSIGN
        nr = nr + 1
        queasy.number2 = nr.
END.

FOR EACH temp-list:
    DELETE temp-list.
END.

FOR EACH queasy WHERE queasy.KEY EQ 282 NO-LOCK:
    FIND FIRST b-queasy WHERE b-queasy.KEY EQ 281 AND b-queasy.number1 EQ queasy.number1 NO-LOCK NO-ERROR.
    IF AVAILABLE b-queasy THEN
    DO:
        CREATE temp-list.
        ASSIGN
            temp-list.number1 = queasy.number1
            temp-list.number2 = queasy.number2
            temp-list.char1   = queasy.char1
            temp-list.number3 = queasy.number3.
        IF queasy.number1 EQ b-queasy.number1 THEN
        DO:
            temp-list.category = b-queasy.char1.
        END.
    END.
END.

