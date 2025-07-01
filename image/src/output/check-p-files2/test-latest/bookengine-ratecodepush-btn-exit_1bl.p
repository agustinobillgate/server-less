DEF TEMP-TABLE t-push-list
    FIELD rcodeVHP      AS CHAR
    FIELD rcodeBE       AS CHAR
    FIELD rmtypeVHP     AS CHAR
    FIELD rmtypeBE      AS CHAR
    FIELD argtVHP       AS CHAR
    FIELD flag          AS INT INIT 0.

DEF TEMP-TABLE outlist
    FIELD KEY       AS INT
    FIELD number1   AS INT
    FIELD char1     AS CHAR.


DEF INPUT PARAMETER TABLE FOR t-push-list.
DEF INPUT PARAMETER bookengID AS INT.
/*naufal - add for logfile*/
DEF INPUT PARAMETER user-init AS CHAR.

DEF VAR str AS CHAR.
DEF VAR i   AS INT.

DEF BUFFER bufQ FOR queasy.
DEF BUFFER qsy FOR queasy.

FIND FIRST queasy WHERE queasy.KEY = 161 AND queasy.number1 = bookengID NO-LOCK NO-ERROR.
DO WHILE AVAILABLE queasy :
    CREATE outlist.
    ASSIGN
        outlist.KEY     = 161
        outlist.number1 = queasy.number1
        outlist.char1   = queasy.char1.
	FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
    IF AVAILABLE qsy THEN
	DO:
		DELETE qsy.
		RELEASE qsy.
	END.
	FIND NEXT queasy WHERE queasy.KEY = 161 AND queasy.number1 = bookengID NO-LOCK NO-ERROR.
END.
/*
FOR EACH queasy WHERE queasy.KEY = 161 AND queasy.number1 = bookengID:
    DELETE queasy.
END.
*/
FOR EACH t-push-list NO-LOCK:
    str = t-push-list.rcodeVHP   + ";"
        + t-push-list.rcodeBE    + ";"
        + t-push-list.rmtypeVHP  + ";"
        + t-push-list.rmtypeBE   + ";"
        + t-push-list.argtVHP.

    CREATE bufQ.
    ASSIGN
        bufQ.KEY = 161
        bufQ.number1 = bookengID
        bufQ.char1 = str.
    RELEASE bufQ.

    FOR EACH outlist WHERE outlist.KEY EQ 161 AND outlist.number1 EQ bookengID:
        IF outlist.char1 NE str THEN
        DO:
            /*naufal - add for logfile*/
            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN
            DO:
                CREATE res-history.
                ASSIGN
                    res-history.nr          = bediener.nr       
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME
                    res-history.aenderung   = "Push RateCode, Booking Engine ID: " + STRING(bookengID) + ", RateCode: " + str
                    res-history.action      = "Booking Engine".
                FIND CURRENT res-history NO-LOCK.
                RELEASE res-history.
            END.
        END.
    END.
END.
