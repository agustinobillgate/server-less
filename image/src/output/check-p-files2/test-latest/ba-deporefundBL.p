
DEFINE TEMP-TABLE depobuff   LIKE artikel.
DEFINE TEMP-TABLE veran-list LIKE bk-veran.

DEFINE INPUT PARAMETER veran-nr         AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER currency        AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER exchg-rate      AS DECIMAL NO-UNDO.
DEFINE OUTPUT PARAMETER bqt-dept        AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER art-depo        AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER err-msg         AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER depoart         AS INTEGER NO-UNDO. 
DEFINE OUTPUT PARAMETER depobezeich     AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER price-decimal   AS INTEGER NO-UNDO. 
DEFINE OUTPUT PARAMETER double-currency AS LOGICAL NO-UNDO. 
DEFINE OUTPUT PARAMETER TABLE FOR depobuff.
DEFINE OUTPUT PARAMETER TABLE FOR veran-list.

DEFINE BUFFER bartikel FOR artikel. 

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN currency = htparam.fchar.
 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
 
FIND FIRST htparam WHERE htparam.paramnr = 900 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN bqt-dept = htparam.finteger.
 
FIND FIRST htparam WHERE htparam.paramnr = 117 USE-INDEX paramnr_ix NO-LOCK. 
IF AVAILABLE htparam THEN ASSIGN art-depo = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN ASSIGN price-decimal = htparam.finteger. 

FIND FIRST htparam WHERE paramnr = 240 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN ASSIGN double-currency = htparam.flogical. 

FIND FIRST artikel WHERE artikel.artnr = art-depo 
  AND artikel.departement = bqt-dept AND artikel.artart = 5 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE artikel THEN DO:
    FIND FIRST bartikel WHERE bartikel.artnr = art-depo
        AND bartikel.departement = 0 AND bartikel.artart = 5 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE bartikel THEN
        ASSIGN err-msg = 1.
    ELSE DO:
        ASSIGN 
            depoart     = bartikel.artnr
            depobezeich = bartikel.bezeich. 
    END.
END.
ELSE 
    ASSIGN 
        depoart     = artikel.artnr
        depobezeich = artikel.bezeich. 

FIND FIRST bk-veran WHERE bk-veran.veran-nr = veran-nr USE-INDEX vernr-ix NO-LOCK NO-ERROR.
IF AVAILABLE bk-veran THEN DO:
    CREATE veran-list.
    BUFFER-COPY bk-veran TO veran-list.
END.

FOR EACH artikel NO-LOCK:
    CREATE depobuff.
    BUFFER-COPY artikel TO depobuff.
END.


