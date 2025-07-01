DEF TEMP-TABLE t-spbill-list
    FIELD selected AS LOGICAL INITIAL YES 
    FIELD bl-recid AS INTEGER. 

DEF TEMP-TABLE t-bill-line LIKE bill-line
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER bil-recid AS INT.
DEF INPUT  PARAMETER double-currency AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-bill-line.
DEF OUTPUT PARAMETER TABLE FOR t-spbill-list.

FIND FIRST bill WHERE RECID(bill) = bil-recid NO-LOCK.
IF AVAILABLE bill THEN DO:
    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK: 
        FIND FIRST t-spbill-list WHERE t-spbill-list.bl-recid = INTEGER(RECID(bill-line)) 
          NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE t-spbill-list THEN 
        DO: 
          create t-spbill-list. 
          ASSIGN 
            t-spbill-list.selected = NO 
            t-spbill-list.bl-recid = RECID(bill-line). 
        END. 
    END.

    IF double-currency THEN 
    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK: 
        CREATE t-bill-line.
        BUFFER-COPY bill-line TO t-bill-line.
        ASSIGN t-bill-line.rec-id = RECID(bill-line).
    END.
    ELSE 
    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK:
        CREATE t-bill-line.
        BUFFER-COPY bill-line TO t-bill-line.
        ASSIGN t-bill-line.rec-id = RECID(bill-line).
    END.
END.

