
DEF BUFFER receiver FOR guest.

DEF INPUT  PARAMETER bil-recid AS INT.
DEF OUTPUT PARAMETER r-zahlungsart LIKE receiver.zahlungsart.

FIND FIRST bill WHERE RECID(bill) = bil-recid NO-LOCK NO-ERROR.
IF AVAILABLE bill THEN DO:
    FIND FIRST receiver WHERE receiver.gastnr = bill.gastnr NO-LOCK.
    r-zahlungsart = receiver.zahlungsart.
END.

