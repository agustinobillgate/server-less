
/*naufal 230920 - Perbaikan validasi saat assign guest ke keyaccount*/
DEFINE TEMP-TABLE guest-list
    FIELD guestnumber   AS INTEGER
    FIELD guestrefno    AS CHARACTER FORMAT "x(10)"
    FIELD guestname     AS CHARACTER FORMAT "x(30)"
    FIELD guesttype     AS CHARACTER FORMAT "x(30)"
    FIELD address       AS CHARACTER FORMAT "x(50)"
    FIELD SELECTED      AS LOGICAL INIT NO.

DEFINE TEMP-TABLE temp-list
    FIELD number1       AS INTEGER   FORMAT ">>>"
    FIELD number2       AS INTEGER   FORMAT ">>>"
    FIELD char1         AS CHARACTER FORMAT "x(50)"
    FIELD number3       AS INTEGER   FORMAT ">>>>>>>>>>"
    FIELD category      AS CHARACTER FORMAT "x(25)".

DEFINE INPUT PARAMETER selected-category    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER user-init            AS CHARACTER NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR guest-list.

DEFINE OUTPUT PARAMETER str-msg             AS CHARACTER INIT "".
DEFINE OUTPUT PARAMETER TABLE FOR temp-list.

DEFINE BUFFER b-queasy FOR queasy.
DEFINE VARIABLE nr          AS INTEGER INIT 1.
DEFINE VARIABLE category    AS CHARACTER.
DEFINE VARIABLE gname       AS CHARACTER.
DEFINE VARIABLE assigned    AS CHARACTER.

RUN add-guest.

PROCEDURE add-guest:
    FIND FIRST b-queasy WHERE b-queasy.KEY EQ 281 AND b-queasy.number1 EQ selected-category NO-LOCK NO-ERROR.
    IF AVAILABLE b-queasy THEN
    DO:
        category = b-queasy.char1.
    END.

    FOR EACH guest-list:
        FOR EACH queasy WHERE queasy.KEY EQ 282 AND queasy.number1 EQ selected-category BY queasy.number2 DESC:
            nr = queasy.number2 + 1.
            LEAVE.
        END.
        
        FIND FIRST queasy WHERE queasy.KEY EQ 282 AND queasy.number3 EQ guest-list.guestnumber NO-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
            CREATE queasy.
            ASSIGN
                queasy.KEY      = 282
                queasy.number1  = selected-category
                queasy.number2  = nr
                queasy.char1    = guest-list.guestname
                queasy.number3  = guest-list.guestnumber.
            gname = queasy.char1.
            
            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN
            DO:
                CREATE res-history.
                ASSIGN
                    res-history.nr          = bediener.nr
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME
                    res-history.aenderung   = "Assign Guest to KeyAccount, Name: " + gname + " KeyAccount: " + category
                    res-history.action      = "Key Account".
                FIND CURRENT res-history NO-LOCK.
                RELEASE res-history.
            END.
        END.
        ELSE IF AVAILABLE queasy THEN
        DO:
            FIND FIRST b-queasy WHERE b-queasy.KEY EQ 281 AND b-queasy.number1 EQ queasy.number1 NO-LOCK.
            IF AVAILABLE b-queasy THEN
            str-msg = str-msg + '"' + queasy.char1 + '" has already been assigned to "' + b-queasy.char1 + '"' + CHR(10).
        END.
    END.

    FOR EACH guest-list:
        DELETE guest-list.
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
END.

