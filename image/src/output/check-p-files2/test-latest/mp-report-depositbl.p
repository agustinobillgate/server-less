DEFINE TEMP-TABLE t-deposit
    FIELD blockID       AS CHARACTER
    FIELD startDate     AS DATE
    FIELD gName         AS CHARACTER
    FIELD depositAmount AS DECIMAL
    FIELD limitDate     AS DATE
    FIELD paidAmount    AS DECIMAL
    FIELD refundAmount  AS DECIMAL
    FIELD remainBalance AS DECIMAL.

/*DEFINE INPUT PARAMETER searchBy     AS CHARACTER.
DEFINE INPUT PARAMETER searchValue  AS CHARACTER.
DEFINE INPUT PARAMETER searchDate1  AS DATE.
DEFINE INPUT PARAMETER searchDate2  AS DATE.
DEFINE INPUT PARAMETER dispType     AS INTEGER.*/
DEFINE OUTPUT PARAMETER TABLE FOR t-deposit.

FOR EACH bk-deposit NO-LOCK:
    FIND FIRST bk-master WHERE bk-master.block-id EQ bk-deposit.blockId NO-LOCK NO-ERROR.
    IF AVAILABLE bk-master THEN
    DO:
        CREATE t-deposit.
        ASSIGN
            t-deposit.blockId       = bk-master.block-id
            t-deposit.startDate     = bk-master.startdate
            t-deposit.gName         = bk-master.name
            t-deposit.depositAmount = bk-deposit.deposit
            t-deposit.limitDate     = bk-deposit.limitDate
            t-deposit.paidAmount    = bk-deposit.totalPaid
            t-deposit.refundAmount  = bk-deposit.totalRefund
            t-deposit.remainBalance = bk-deposit.deposit - bk-deposit.totalPaid + bk-deposit.totalRefund.
    END.
END.

/*
IF dispType EQ 0 THEN
DO:
    FOR EACH bk-deposit WHERE bk-deposit.totalPaid GT 0:
        FIND FIRST bk-master WHERE bk-master.block-id EQ bk-deposit.blockId
            AND bk-master.startdate GE searchDate1
            AND bk-master.startdate LE searchDate2 NO-LOCK NO-ERROR.
        IF AVAILABLE bk-master THEN
        DO:
            CREATE t-deposit.
            ASSIGN
                t-deposit.blockId       = bk-master.block-id
                t-deposit.startDate     = bk-master.startdate
                t-deposit.gName         = bk-master.name
                t-deposit.depositAmount = bk-deposit.deposit
                t-deposit.limitDate     = bk-deposit.limitDate
                t-deposit.paidAmount    = bk-deposit.totalPaid
                t-deposit.refundAmount  = bk-deposit.totalRefund
                t-deposit.remainBalance = bk-deposit.deposit - bk-deposit.totalPaid + bk-deposit.totalRefund.
        END.
    END.
END.
ELSE IF dispType EQ 1 THEN
DO:
    FOR EACH bk-deposit:
        FIND FIRST bk-master WHERE bk-master.block-id EQ bk-deposit.blockId
            AND bk-master.startdate GE searchDate1
            AND bk-master.startdate LE searchDate2 NO-LOCK NO-ERROR.
        IF AVAILABLE bk-master THEN
        DO:
            CREATE t-deposit.
            ASSIGN
                t-deposit.blockId       = bk-master.block-id
                t-deposit.startDate     = bk-master.startdate                
                t-deposit.gName         = bk-master.name
                t-deposit.depositAmount = bk-deposit.deposit
                t-deposit.limitDate     = bk-deposit.limitDate
                t-deposit.paidAmount    = bk-deposit.totalPaid
                t-deposit.refundAmount  = bk-deposit.totalRefund
                t-deposit.remainBalance = bk-deposit.deposit - bk-deposit.totalPaid + bk-deposit.totalRefund.
        END.
    END.
END.
ELSE IF dispType EQ 2 THEN
DO:
    FOR EACH bk-deposit WHERE bk-deposit.totalPaid LE 0: 
        FIND FIRST bk-master WHERE bk-master.block-id EQ bk-deposit.blockId
            AND bk-master.startdate GE searchDate1
            AND bk-master.startdate LE searchDate2 NO-LOCK NO-ERROR.
        IF AVAILABLE bk-master THEN
        DO:
            CREATE t-deposit.
            ASSIGN
                t-deposit.blockId       = bk-master.block-id
                t-deposit.startDate     = bk-master.startdate                
                t-deposit.gName         = bk-master.name
                t-deposit.depositAmount = bk-deposit.deposit
                t-deposit.limitDate     = bk-deposit.limitDate
                t-deposit.paidAmount    = bk-deposit.totalPaid
                t-deposit.refundAmount  = bk-deposit.totalRefund
                t-deposit.remainBalance = bk-deposit.deposit - bk-deposit.totalPaid + bk-deposit.totalRefund.
        END.
    END.
END.

IF searchBy EQ "Block ID" THEN
DO:
    searchValue = "*" + searchValue + "*".
    
    FOR EACH t-deposit WHERE NOT t-deposit.blockId MATCHES searchValue:
        DELETE t-deposit.
    END.
END.
ELSE IF searchBy EQ "Guest Name" THEN
DO:
    searchValue = "*" + searchValue + "*".
    
    FOR EACH t-deposit WHERE NOT t-deposit.gName MATCHES searchValue:
        DELETE t-deposit.
    END.
END.
ELSE IF searchBy EQ "Deposit" THEN
DO:   
    FOR EACH t-deposit WHERE t-deposit.deposit NE DECIMAL(searchValue):
        DELETE t-deposit.
    END.
END.
ELSE IF searchBy EQ "Paid Amount" THEN
DO:
    FOR EACH t-deposit WHERE t-deposit.paidAmount NE DECIMAL(searchValue):
        DELETE t-deposit.
    END.
END.
ELSE IF searchBy EQ "Remain Balance" THEN
DO:
    FOR EACH t-deposit WHERE t-deposit.remainBalance NE DECIMAL(searchValue):
        DELETE t-deposit.
    END.
END.
*/
