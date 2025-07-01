DEF TEMP-TABLE t-spbill-list
    FIELD selected AS LOGICAL INITIAL YES 
    FIELD bl-recid AS INTEGER. 

DEF TEMP-TABLE t-bill-line LIKE bill-line
    FIELD rec-id AS INT
    FIELD serv   AS DECIMAL FORMAT "->,>>>,>>>,>>9" 
    FIELD vat    AS DECIMAL FORMAT "->,>>>,>>>,>>9" 
    FIELD netto  AS DECIMAL FORMAT "->,>>>,>>>,>>9" 
    FIELD art-type AS INTEGER
    .

DEF INPUT  PARAMETER bil-recid AS INT.
DEF INPUT  PARAMETER double-currency AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-bill-line.
DEF OUTPUT PARAMETER TABLE FOR t-spbill-list.

DEFINE VARIABLE serv   AS DECIMAL FORMAT "->,>>>,>>>,>>9"   NO-UNDO.
DEFINE VARIABLE vat    AS DECIMAL FORMAT "->,>>>,>>>,>>9"   NO-UNDO.
DEFINE VARIABLE netto  AS DECIMAL FORMAT "->,>>>,>>>,>>9"   NO-UNDO.
DEFINE VARIABLE art-type AS INTEGER NO-UNDO.

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
        ASSIGN serv    = 0
               vat     = 0
               netto   = 0.

        FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN DO:
            ASSIGN art-type = artikel.artart.
            RUN calc-servvat.p(artikel.departement, artikel.artnr, bill-line.bill-datum, 
                   artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).
        END.
        CREATE t-bill-line.
        BUFFER-COPY bill-line TO t-bill-line.
        ASSIGN t-bill-line.rec-id   = RECID(bill-line)
               t-bill-line.serv     = t-bill-line.betrag * serv
               t-bill-line.vat      = t-bill-line.betrag * vat
               t-bill-line.netto    = t-bill-line.betrag - t-bill-line.serv  - t-bill-line.vat 
               t-bill-line.art-type = art-type.
    END.
    ELSE 
    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK:
        ASSIGN serv    = 0
               vat     = 0
               netto   = 0.

        FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN DO:
            ASSIGN art-type = artikel.artart.
            RUN calc-servvat.p(artikel.departement, artikel.artnr, bill-line.bill-datum, 
                   artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).
        END.
        CREATE t-bill-line.
        BUFFER-COPY bill-line TO t-bill-line.
        ASSIGN t-bill-line.rec-id = RECID(bill-line)
           t-bill-line.serv       = t-bill-line.betrag * serv
           t-bill-line.vat        = t-bill-line.betrag * vat
           t-bill-line.netto      = t-bill-line.betrag - t-bill-line.serv  - t-bill-line.vat 
           t-bill-line.art-type   = art-type.
    END.
END.

