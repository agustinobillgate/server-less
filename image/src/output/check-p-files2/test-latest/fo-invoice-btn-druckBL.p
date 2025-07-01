
DEF INPUT  PARAMETER recid-hjournal     AS INT.
DEF INPUT  PARAMETER recid-hbill-line   AS INT.
DEF OUTPUT PARAMETER do-it              AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER recid-h-bill       AS INT INIT 0.

IF recid-hjournal NE 0 THEN
FIND FIRST h-journal WHERE RECID(h-journal) = recid-hjournal NO-LOCK NO-ERROR.
ELSE IF recid-hbill-line NE 0 THEN
FIND FIRST h-bill-line WHERE RECID(h-bill-line) = recid-hbill-line NO-LOCK NO-ERROR.

IF AVAILABLE h-journal THEN
FIND FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr
    AND h-bill.departement = h-journal.departement
    NO-LOCK NO-ERROR.
ELSE IF AVAILABLE h-bill-line THEN
FIND FIRST h-bill WHERE h-bill.rechnr = h-bill-line.rechnr
    AND h-bill.departement = h-bill-line.departement
    NO-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN
DO:
    do-it = YES.
    recid-h-bill = RECID(vhp.h-bill).
    /*MT
    IF double-currency THEN RUN print-hbill2.p(YES, 0, 
      RECID(vhp.h-bill)). 
    ELSE RUN print-hbill1.p(YES, 0, RECID(vhp.h-bill)). 
    */
END.
