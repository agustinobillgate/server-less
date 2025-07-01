
DEF INPUT PARAMETER c-list-rechnr AS INT.
DEF INPUT PARAMETER c-list-dept AS INT.
DEF INPUT PARAMETER guestname AS CHAR.
DEF INPUT PARAMETER c-list-datum AS DATE.
DEF INPUT PARAMETER c-list-p-artnr AS INT.

FIND FIRST h-bill WHERE h-bill.rechnr = c-list-rechnr 
    AND h-bill.departement = c-list-dept NO-LOCK NO-ERROR. 
IF AVAILABLE h-bill THEN 
DO: 
    FIND CURRENT h-bill EXCLUSIVE-LOCK. 
    h-bill.bilname = guestname. 
    FIND CURRENT h-bill NO-LOCK. 
END. 
FIND FIRST h-journal WHERE h-journal.bill-datum = c-list-datum 
    AND h-journal.departement = c-list-dept 
    AND h-journal.segmentcode = c-list-p-artnr 
    AND h-journal.rechnr = c-list-rechnr 
    AND h-journal.zeit GE 0 USE-INDEX segment_ix NO-LOCK NO-ERROR. 
DO WHILE AVAILABLE h-journal: 
    FIND CURRENT h-journal EXCLUSIVE-LOCK. 
    h-journal.aendertext = guestname. 
    FIND CURRENT h-journal NO-LOCK. 
    FIND NEXT h-journal WHERE h-journal.bill-datum = c-list-datum 
      AND h-journal.departement = c-list-dept 
      AND h-journal.segmentcode = c-list-p-artnr 
      AND h-journal.rechnr = c-list-rechnr 
      AND h-journal.zeit GE 0 USE-INDEX segment_ix NO-LOCK NO-ERROR. 
END.
