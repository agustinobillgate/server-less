/*
    Note:
    The date-to-date program only updates the queasy, 
    the actual delivery remains in centralized interface.
*/

/*=========================DEFINE VARIABLES========================*/
DEFINE INPUT PARAMETER inp-fdate AS DATE NO-UNDO.
DEFINE INPUT PARAMETER inp-tdate AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER counter AS INTEGER NO-UNDO.
DEFINE VARIABLE date-char   AS CHARACTER NO-UNDO. /*YYYY-MM-DD*/
DEFINE VARIABLE mapping     AS CHARACTER NO-UNDO.
DEFINE VARIABLE jour-desc   AS CHARACTER NO-UNDO.

DEFINE BUFFER bqueasy FOR queasy.

/*===========================MAIN LOGIC============================*/
ASSIGN counter = 0.

FOR EACH gl-jouhdr WHERE gl-jouhdr.activeflag EQ 0 /*0 = Active ; 1 = Closed*/
    AND gl-jouhdr.datum GE inp-fdate
    AND gl-jouhdr.datum LE inp-tdate
    NO-LOCK
    BY gl-jouhdr.datum
    BY gl-jouhdr.refno
    BY gl-jouhdr.bezeich:

    FOR EACH gl-journal WHERE gl-journal.jnr EQ gl-jouhdr.jnr NO-LOCK:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ gl-journal.fibukonto
            AND gl-acct.userinit NE ?
            AND gl-acct.userinit NE ""
            NO-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN
        DO:
            IF NUM-ENTRIES(gl-acct.userinit, ";") GE 2 THEN
            DO:
                ASSIGN mapping = TRIM(ENTRY(2, gl-acct.userinit, ";")).
            END.
            ELSE
            DO:
                ASSIGN mapping = TRIM(ENTRY(1, gl-acct.userinit, ";")).
            END.
            IF mapping NE "" THEN
            DO:
                FIND FIRST bqueasy WHERE bqueasy.KEY EQ 345
                    AND bqueasy.number1 EQ gl-jouhdr.jnr 
                    AND bqueasy.date1 EQ gl-jouhdr.datum
                    NO-LOCK NO-ERROR.
                IF AVAILABLE bqueasy THEN
                DO:
                    /*Update Queasy*/
                    FIND CURRENT bqueasy EXCLUSIVE-LOCK.
                    ASSIGN
                        bqueasy.logi1 = YES
                        bqueasy.logi2 = NO
                        bqueasy.logi3 = NO.
                    FIND CURRENT bqueasy NO-LOCK.
                    RELEASE bqueasy.

                    ASSIGN counter = counter + 1.
                END.
                ELSE
                DO:
                    /*Create Queasy*/
                    CREATE bqueasy.
                    ASSIGN
                        bqueasy.KEY = 345
                        bqueasy.number1 = gl-jouhdr.jnr
                        bqueasy.number2 = TIME
                        bqueasy.char1 = gl-jouhdr.bezeich
                        bqueasy.date1 = gl-jouhdr.datum
                        bqueasy.logi1 = YES
                        bqueasy.logi2 = NO
                        bqueasy.logi3 = NO.
                    RELEASE bqueasy.

                    ASSIGN counter = counter + 1.
                END.
            END.
        END.
    END.
END.
