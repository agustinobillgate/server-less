DEFINE TEMP-TABLE payload-list
    FIELD ns-rechnr             AS INTEGER
    FIELD payment-type          AS INTEGER
    FIELD rechnr-remark         AS INTEGER
    FIELD input-remark          AS CHAR
    FIELD rechnr-due-date       AS INTEGER
    FIELD due-date              AS DATE
    FIELD mode                  AS INTEGER
    FIELD user-init             AS CHAR
    FIELD bill-type             AS CHAR
    .

DEFINE TEMP-TABLE guarantee-payment
    FIELD payment-type      AS CHAR
    FIELD payment-number    AS INTEGER
    .

DEFINE INPUT PARAMETER TABLE FOR payload-list.
DEFINE OUTPUT PARAMETER TABLE FOR guarantee-payment.

DEFINE BUFFER buff-queasy FOR queasy.

FIND FIRST payload-list NO-ERROR.
IF payload-list.mode EQ 1 THEN
DO:
    /* prepare Guarantee Payment */
    FOR EACH queasy WHERE queasy.KEY = 9 NO-LOCK:
        CREATE guarantee-payment.
        ASSIGN
            guarantee-payment.payment-type      = queasy.char1
            guarantee-payment.payment-number    = queasy.number1.
    END.
END.
ELSE
DO:
    /* Save Guarantee Payment 
    FIND FIRST bill WHERE bill.rechnr = payload-list.ns-rechnr 
        AND bill.flag = 0 AND bill.saldo NE 0 NO-LOCK NO-ERROR.
    IF AVAILABLE bill THEN
    DO:
        FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
            AND res-line.reslinnr = bill.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE res-line THEN
        DO:
            FIND CURRENT res-line EXCLUSIVE-LOCK.
            ASSIGN
                res-line.code = STRING(payload-list.payment-type).
            FIND CURRENT res-line NO-LOCK.
            RELEASE res-line.
        END.
    END. */

    /* Save Guarantee Payment (2) */
    IF payload-list.ns-rechnr NE ? THEN
    DO:
        FIND FIRST bill WHERE bill.rechnr = payload-list.ns-rechnr 
            AND bill.flag = 0 AND bill.saldo NE 0 NO-LOCK NO-ERROR.
        IF AVAILABLE bill THEN
        DO:
            IF payload-list.bill-type EQ "NS" THEN
            DO: 
                FIND FIRST buff-queasy WHERE buff-queasy.KEY = 9 
                    AND buff-queasy.number1 = payload-list.payment-type NO-LOCK NO-ERROR.
                IF AVAILABLE buff-queasy THEN
                DO:     
                    FIND FIRST queasy WHERE queasy.key EQ 350 
                        AND queasy.number1 = bill.rechnr NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        FIND CURRENT queasy EXCLUSIVE-LOCK.
                        ASSIGN
                            queasy.char1  = buff-queasy.char1
                            .
                        FIND CURRENT queasy NO-LOCK.
                        RELEASE queasy.
                    END.
                    ELSE
                    DO:
                        CREATE queasy.
                        ASSIGN
                            queasy.key      = 350
                            queasy.number1  = bill.rechnr
                            queasy.char1    = buff-queasy.char1
                            queasy.char2    = "NS"
                        .
                    END.
                END.
            END.
            ELSE IF payload-list.bill-type EQ "M" THEN
            DO:
                FIND FIRST buff-queasy WHERE buff-queasy.KEY = 9 
                    AND buff-queasy.number1 = payload-list.payment-type NO-LOCK NO-ERROR.
                IF AVAILABLE buff-queasy THEN
                DO:     
                    FIND FIRST queasy WHERE queasy.key EQ 350 
                        AND queasy.number1 = bill.rechnr NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        FIND CURRENT queasy EXCLUSIVE-LOCK.
                        ASSIGN
                            queasy.char1  = buff-queasy.char1
                            .
                        FIND CURRENT queasy NO-LOCK.
                        RELEASE queasy.
                    END.
                    ELSE
                    DO:
                        CREATE queasy.
                        ASSIGN
                            queasy.key      = 350
                            queasy.number1  = bill.rechnr
                            queasy.char1    = buff-queasy.char1
                            queasy.char2    = "M"
                        .
                    END.
                END.
            END.
            ELSE
            DO:
                FIND FIRST buff-queasy WHERE buff-queasy.KEY = 9 
                    AND buff-queasy.number1 = payload-list.payment-type NO-LOCK NO-ERROR.
                IF AVAILABLE buff-queasy THEN
                DO:     
                    FIND FIRST queasy WHERE queasy.key EQ 350 
                        AND queasy.number1 = bill.rechnr NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        FIND CURRENT queasy EXCLUSIVE-LOCK.
                        ASSIGN
                            queasy.char1  = buff-queasy.char1
                            .
                        FIND CURRENT queasy NO-LOCK.
                        RELEASE queasy.
                    END.
                    ELSE
                    DO:
                        CREATE queasy.
                        ASSIGN
                            queasy.key      = 350
                            queasy.number1  = bill.rechnr
                            queasy.char1    = buff-queasy.char1
                        .
                    END.
                END.
            END.
        END.
    END.

    /* Save remark  */
    IF payload-list.rechnr-remark NE ? THEN
    DO:
        IF payload-list.bill-type EQ "NS" THEN
        DO:
            FIND FIRST bill WHERE bill.rechnr = payload-list.rechnr-remark 
                AND bill.flag = 0 AND bill.saldo NE 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bill THEN
            DO:
                IF bill.vesrdepot NE payload-list.input-remark THEN
                DO:
                    /* log file for remark */
                    FIND FIRST bediener WHERE bediener.userinit = payload-list.user-init NO-LOCK.
                    CREATE res-history. 
                    ASSIGN 
                        res-history.nr = bediener.nr 
                        res-history.datum = TODAY 
                        res-history.zeit = TIME 
                        res-history.action = "Outstanding Folio"
                    .
                    res-history.aenderung = "Outstanding Folio: billNo " + STRING(bill.rechnr)
                        + " and BillType:" + payload-list.bill-type + " " + bill.vesrdepot + " changed to " + payload-list.input-remark.

                    FIND CURRENT res-history NO-LOCK.   
                    RELEASE res-history. 

                    FIND CURRENT bill EXCLUSIVE-LOCK.
                    ASSIGN
                        bill.vesrdepot = payload-list.input-remark.
                    FIND CURRENT bill NO-LOCK.
                    RELEASE bill.
                END.
            END.
        END.
        ELSE IF payload-list.bill-type EQ "M" THEN
        DO:
            FIND FIRST bill WHERE bill.rechnr = payload-list.rechnr-remark 
                AND bill.flag = 0 AND bill.saldo NE 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bill THEN
            DO:
                IF bill.vesrdepot NE payload-list.input-remark THEN
                DO:
                    /* log file for remark */
                    FIND FIRST bediener WHERE bediener.userinit = payload-list.user-init NO-LOCK.
                    CREATE res-history. 
                    ASSIGN 
                        res-history.nr = bediener.nr 
                        res-history.datum = TODAY 
                        res-history.zeit = TIME 
                        res-history.action = "Outstanding Folio"
                    .
                    res-history.aenderung = "Outstanding Folio: billNo " + STRING(bill.rechnr)
                        + " and BillType:" + payload-list.bill-type + " " + bill.vesrdepot + " changed to " + payload-list.input-remark.

                    FIND CURRENT res-history NO-LOCK.   
                    RELEASE res-history. 

                    FIND CURRENT bill EXCLUSIVE-LOCK.
                    ASSIGN
                        bill.vesrdepot = payload-list.input-remark.
                    FIND CURRENT bill NO-LOCK.
                    RELEASE bill.
                END.
            END.
        END.
        ELSE
        DO:
            FIND FIRST bill WHERE bill.rechnr = payload-list.rechnr-remark 
                AND bill.flag = 0 AND bill.saldo NE 0 NO-LOCK NO-ERROR.
            IF AVAILABLE bill THEN
            DO:
                IF bill.vesrdepot NE payload-list.input-remark THEN
                DO:
                    /* log file for remark */
                    FIND FIRST bediener WHERE bediener.userinit = payload-list.user-init NO-LOCK.
                    CREATE res-history. 
                    ASSIGN 
                        res-history.nr = bediener.nr 
                        res-history.datum = TODAY 
                        res-history.zeit = TIME 
                        res-history.action = "Outstanding Folio"
                    .
                    res-history.aenderung = "Outstanding Folio: billNo " + STRING(bill.rechnr)
                        + " and BillType:GB" + " " + bill.vesrdepot + " changed to " + payload-list.input-remark.

                    FIND CURRENT res-history NO-LOCK.   
                    RELEASE res-history. 

                    FIND CURRENT bill EXCLUSIVE-LOCK.
                    ASSIGN
                        bill.vesrdepot = payload-list.input-remark.
                    FIND CURRENT bill NO-LOCK.
                    RELEASE bill.
                END.
            END.
        END.
    END.

    /* Save Due Date  */
    IF payload-list.rechnr-due-date NE ? THEN
    DO:
        IF payload-list.bill-type EQ "NS" THEN
        DO:
            FIND FIRST queasy WHERE queasy.key EQ 350 
                AND queasy.number1 = payload-list.rechnr-due-date NO-LOCK NO-ERROR.
            IF NOT AVAILABLE queasy THEN
            DO:
                CREATE queasy.
                ASSIGN
                    queasy.key      = 350
                    queasy.number1  = payload-list.rechnr-due-date
                    queasy.date1    = payload-list.due-date
                    queasy.char2    = "NS"
                .
            END.
            ELSE
            DO:
                FIND CURRENT queasy EXCLUSIVE-LOCK.
                ASSIGN
                    queasy.date1 = payload-list.due-date
                .
                FIND CURRENT queasy NO-LOCK.
                RELEASE queasy.
            END.
        END.
        ELSE IF payload-list.bill-type EQ "M" THEN
        DO:
            FIND FIRST queasy WHERE queasy.key EQ 350 
                AND queasy.number1 = payload-list.rechnr-due-date NO-LOCK NO-ERROR.
            IF NOT AVAILABLE queasy THEN
            DO:
                CREATE queasy.
                ASSIGN
                    queasy.key      = 350
                    queasy.number1  = payload-list.rechnr-due-date
                    queasy.date1    = payload-list.due-date
                    queasy.char2    = "M"
                .
            END.
            ELSE
            DO:
                FIND CURRENT queasy EXCLUSIVE-LOCK.
                ASSIGN
                    queasy.date1 = payload-list.due-date
                .
                FIND CURRENT queasy NO-LOCK.
                RELEASE queasy.
            END.
        END.
        ELSE
        DO:
            FIND FIRST queasy WHERE queasy.key EQ 350 
                AND queasy.number1 = payload-list.rechnr-due-date NO-LOCK NO-ERROR.
            IF NOT AVAILABLE queasy THEN
            DO:
                CREATE queasy.
                ASSIGN
                    queasy.key      = 350
                    queasy.number1  = payload-list.rechnr-due-date
                    queasy.date1    = payload-list.due-date
                .
            END.
            ELSE
            DO:
                FIND CURRENT queasy EXCLUSIVE-LOCK.
                ASSIGN
                    queasy.date1 = payload-list.due-date
                .
                FIND CURRENT queasy NO-LOCK.
                RELEASE queasy.
            END.
        END.
    END.
END.
