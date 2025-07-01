
DEF TEMP-TABLE t-bill-line LIKE bill-line
    FIELD rec-id AS INT
    FIELD run-disp-restbill AS LOGICAL INIT NO.
DEF TEMP-TABLE t-blinehis LIKE blinehis
    FIELD rec-id AS INT
    FIELD run-disp-restbill AS LOGICAL INIT NO.

DEF INPUT  PARAMETER a-rechnr AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-bill-line.
DEF OUTPUT PARAMETER TABLE FOR t-blinehis.

DEF BUFFER foart FOR artikel. 

FIND FIRST bill-line WHERE bill-line.rechnr = a-rechnr NO-LOCK NO-ERROR.
IF AVAILABLE bill-line THEN
FOR EACH bill-line WHERE bill-line.rechnr = a-rechnr NO-LOCK:
    FIND FIRST foart WHERE foart.artnr = bill-line.artnr 
        AND foart.departement = 0 NO-LOCK NO-ERROR. 

    CREATE t-bill-line.
    BUFFER-COPY bill-line TO t-bill-line.
    t-bill-line.rec-id = (RECID(bill-line)).

    IF AVAILABLE foart AND foart.artart = 1 THEN
        t-bill-line.run-disp-restbill = YES.
END.
ELSE
FOR EACH blinehis WHERE blinehis.rechnr = a-rechnr NO-LOCK :
    FIND FIRST foart WHERE foart.artnr = bill-line.artnr 
        AND foart.departement = 0 NO-LOCK NO-ERROR. 

    CREATE t-blinehis.
    BUFFER-COPY blinehis TO t-blinehis.
    t-blinehis.rec-id = (RECID(blinehis)).

    IF AVAILABLE foart AND foart.artart = 1 THEN
        t-blinehis.run-disp-restbill = YES.
END.
        
