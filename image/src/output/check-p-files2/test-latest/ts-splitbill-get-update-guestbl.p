DEFINE INPUT PARAMETER v-key        AS INTEGER.
DEFINE INPUT PARAMETER hbill-recid  AS INTEGER.
DEFINE INPUT PARAMETER curr-select  AS INTEGER.
DEFINE INPUT PARAMETER guest-name   AS CHARACTER.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER gname       AS CHARACTER.

DEFINE VARIABLE bill-no AS INTEGER NO-UNDO.
DEFINE VARIABLE dept-no AS INTEGER NO-UNDO.
DEFINE VARIABLE main-guest AS CHARACTER NO-UNDO.

FIND FIRST h-bill WHERE RECID(h-bill) EQ hbill-recid NO-LOCK NO-ERROR.
IF NOT AVAILABLE h-bill THEN RETURN.

ASSIGN
    bill-no     = h-bill.rechnr
    dept-no     = h-bill.departement
    main-guest  = h-bill.bilname
    .

IF v-key EQ 1 THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 286
        AND queasy.number1 EQ bill-no
        AND queasy.number2 EQ dept-no
        AND queasy.number3 EQ curr-select NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        IF guest-name NE "" OR guest-name NE ? THEN
        DO:
            CREATE queasy.
            ASSIGN
                queasy.KEY      = 286
                queasy.number1  = bill-no     
                queasy.number2  = dept-no    
                queasy.number3  = curr-select
                queasy.char1    = guest-name
                /*queasy.char2    = main-guest*/
                .        
        END.    
    END.
    ELSE
    DO:
        IF guest-name NE "" AND guest-name NE ? THEN
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK NO-ERROR.
            queasy.char1    = guest-name.
            /*queasy.char2    = main-guest.*/
            FIND CURRENT queasy NO-LOCK.
            RELEASE queasy.       
        END.
        ELSE
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            DELETE queasy.
            RELEASE queasy.        
        END.
    END.
    success-flag = YES.
END.
ELSE IF v-key EQ 2 THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 286
        AND queasy.number1 EQ bill-no
        AND queasy.number2 EQ dept-no
        AND queasy.number3 EQ curr-select NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN gname = queasy.char1.

    success-flag = YES.
END.
ELSE IF v-key EQ 3 THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 286
        AND queasy.number1 EQ bill-no
        AND queasy.number2 EQ dept-no
        AND queasy.number3 EQ curr-select NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        DELETE queasy.
        RELEASE queasy.
    END.
    success-flag = YES.
END.

