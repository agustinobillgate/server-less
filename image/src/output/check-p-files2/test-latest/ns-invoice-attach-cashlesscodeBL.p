
DEFINE INPUT PARAMETER cashless-code AS CHARACTER.
DEFINE INPUT PARAMETER bill-recid AS INTEGER.
DEFINE OUTPUT PARAMETER ok-flag AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER msg-int AS INTEGER.

DEFINE VARIABLE found-sameqr AS LOGICAL.
DEFINE VARIABLE invalid-code AS LOGICAL.
DEFINE VARIABLE transaction-exist AS LOGICAL.

DEFINE BUFFER buf-bill FOR bill.


FOR EACH buf-bill WHERE buf-bill.flag EQ 0 
    AND buf-bill.resnr EQ 0 AND buf-bill.reslinnr EQ 1 
    AND buf-bill.rechnr GT 0 /*AND buf-bill.billtyp EQ dept*/ NO-LOCK:

    IF buf-bill.vesrdepot2 NE "" AND buf-bill.vesrdepot2 EQ cashless-code THEN
    DO:
        found-sameqr = YES.
        LEAVE.
    END.
END.
IF found-sameqr THEN
DO:
    msg-int = 1.
    RETURN.
END.    

IF cashless-code NE "" THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 248 AND queasy.char2 EQ cashless-code NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        invalid-code = YES.
    END.
    IF invalid-code THEN
    DO:
        msg-int = 2.
        RETURN.
    END.
END.

FIND FIRST buf-bill WHERE RECID(buf-bill) EQ bill-recid AND buf-bill.flag EQ 0 
    AND buf-bill.resnr EQ 0 AND buf-bill.reslinnr EQ 1 
    AND buf-bill.rechnr GT 0 AND buf-bill.vesrdepot2 NE "" NO-LOCK NO-ERROR.
IF AVAILABLE buf-bill THEN
DO:
    FIND FIRST bill-line WHERE bill-line.rechnr EQ buf-bill.rechnr NO-LOCK NO-ERROR.
    IF AVAILABLE bill-line THEN
    DO:
        msg-int = 3.
        RETURN.
    END.
END.

FIND FIRST bill WHERE RECID(bill) EQ bill-recid NO-LOCK NO-ERROR.
IF AVAILABLE bill THEN
DO:
    FIND CURRENT bill EXCLUSIVE-LOCK.
    bill.vesrdepot2 = cashless-code.
    FIND CURRENT bill NO-LOCK.
    RELEASE bill.

    ok-flag = YES.
END.
