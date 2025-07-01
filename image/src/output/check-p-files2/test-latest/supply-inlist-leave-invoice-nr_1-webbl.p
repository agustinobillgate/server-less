DEFINE INPUT PARAMETER h-recid       AS INTEGER.
DEFINE INPUT PARAMETER artnr         AS INTEGER.
DEFINE INPUT PARAMETER invoice-nr    AS CHARACTER.
DEFINE INPUT PARAMETER serial-number AS CHARACTER.
DEFINE INPUT PARAMETER invoice-date  AS DATE.

FIND FIRST l-ophdr WHERE RECID(l-ophdr) = h-recid EXCLUSIVE-LOCK. 
IF AVAILABLE l-ophdr THEN
DO:
    l-ophdr.fibukonto = TRIM(invoice-nr). 
    FIND CURRENT l-ophdr NO-LOCK. 

    /* Oscar (14/01/24) - 98F7A0 - save additional information in incoming report */
    FOR EACH l-op WHERE l-op.lscheinnr EQ l-ophdr.lscheinnr
        AND l-op.loeschflag LE 1
        AND l-op.op-art EQ 1 NO-LOCK:
            FIND FIRST queasy WHERE queasy.KEY EQ 335
                AND queasy.char1 EQ l-op.lscheinnr
                AND queasy.number1 EQ l-op.artnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE queasy THEN
            DO:
                CREATE queasy.
                ASSIGN
                    queasy.KEY     = 335
                    queasy.char1   = l-op.lscheinnr
                    queasy.number1 = l-op.artnr
                    queasy.date1   = l-op.datum
                    queasy.char2   = serial-number.

                IF queasy.number1 EQ artnr THEN
                DO:
                    queasy.date2 = invoice-date.
                END.
            END.
            ELSE
            DO:
                FIND CURRENT queasy EXCLUSIVE-LOCK.

                queasy.char2 = serial-number.
                IF queasy.number1 EQ artnr THEN
                DO:
                    queasy.date2 = invoice-date.
                END.

                FIND CURRENT queasy NO-LOCK.
                RELEASE queasy.
            END.
    END.
END.

