DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEF TEMP-TABLE t-h-artikel1 LIKE h-artikel
    FIELD rec-id            AS INTEGER
    FIELD amount-taxserv    AS DECIMAL
    FIELD max-soldout-qty   AS INTEGER
    FIELD soldout-flag      AS LOGICAL
    FIELD posted-qty        AS INTEGER
.

DEF INPUT-OUTPUT PARAMETER kpr-time AS INT.
DEF INPUT-OUTPUT PARAMETER kpr-recid AS INT.
DEF INPUT PARAMETER bill-date AS DATE.
DEF INPUT PARAMETER tischnr AS INT.
DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER amount LIKE bill-line.betrag.

DEF OUTPUT PARAMETER fl-code AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-h-artikel1.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.

DEFINE VARIABLE ct                  AS CHARACTER NO-UNDO.
DEFINE VARIABLE l-deci              AS INTEGER NO-UNDO INIT 2.
DEFINE VARIABLE serv-vat            AS LOGICAL NO-UNDO. 
DEFINE VARIABLE tax-vat             AS LOGICAL NO-UNDO.                                   
DEFINE VARIABLE tax                 AS DECIMAL NO-UNDO. 
DEFINE VARIABLE serv                AS DECIMAL NO-UNDO.
DEFINE VARIABLE service             AS DECIMAL NO-UNDO.
DEFINE VARIABLE vat                 AS DECIMAL NO-UNDO INIT 0.
DEFINE VARIABLE vat2                AS DECIMAL NO-UNDO INIT 0.
DEFINE VARIABLE fact-scvat          AS DECIMAL NO-UNDO INIT 1.
DEFINE VARIABLE servtax-use-foart   AS LOGICAL.         
DEFINE VARIABLE service-foreign     AS DECIMAL NO-UNDO INIT 0.  
DEFINE VARIABLE serv-code           AS INTEGER. 
DEFINE VARIABLE vat-code            AS INTEGER.
DEFINE VARIABLE f-disc              AS INTEGER.
DEFINE VARIABLE b-disc              AS INTEGER.
DEFINE VARIABLE o-disc              AS INTEGER. 
DEFINE VARIABLE price-decimal       AS INTEGER.
DEFINE VARIABLE curr-qty-posted     AS INTEGER.

FIND FIRST hoteldpt WHERE hoteldpt.num EQ curr-dept NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN
DO:
    servtax-use-foart = hoteldpt.defult.
END. 
FIND FIRST htparam WHERE htparam.paramnr EQ 557 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.finteger NE 0 THEN f-disc = htparam.finteger.
FIND FIRST htparam WHERE htparam.paramnr EQ 556 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.finteger NE 0 THEN o-disc = htparam.finteger.
FIND FIRST htparam WHERE htparam.paramnr EQ 596 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.finteger NE 0 THEN b-disc = htparam.finteger.
FIND FIRST htparam WHERE htparam.paramnr EQ 491 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN price-decimal = htparam.finteger.

IF (kpr-time - TIME) GE 300 THEN kpr-time = TIME.
IF kpr-recid = 0 THEN
DO:
    FIND FIRST vhp.queasy WHERE vhp.queasy.key = 3 
      AND vhp.queasy.number1 NE 0 
      AND (vhp.queasy.char1 NE "" OR vhp.queasy.char3 NE "") 
      AND (queasy.date1 EQ bill-date) NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.queasy THEN 
    ASSIGN kpr-recid = INTEGER(RECID(vhp.queasy)).
    kpr-time = TIME.
END.
ELSE IF kpr-recid NE 0 AND (TIME GT (kpr-time + 30)) THEN
DO:
    FIND FIRST vhp.queasy WHERE RECID(vhp.queasy) = kpr-recid
        NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.queasy AND vhp.queasy.number1 NE 0 THEN
    DO:
        fl-code = 1.
    END.
    ASSIGN
      kpr-recid = 0
      kpr-time  = TIME
    .
END.

FIND FIRST vhp.h-bill WHERE vhp.h-bill.tischnr = tischnr
    AND vhp.h-bill.departement = curr-dept
    AND vhp.h-bill.flag = 0 NO-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN
DO:
    CREATE t-h-bill.
    BUFFER-COPY h-bill TO t-h-bill.
    ASSIGN t-h-bill.rec-id = RECID(h-bill).
END.

FOR EACH h-artikel WHERE h-artikel.departement = curr-dept
    AND h-artikel.activeflag NO-LOCK:
    
    CREATE t-h-artikel1.
    BUFFER-COPY h-artikel TO t-h-artikel1.
    ASSIGN t-h-artikel1.rec-id = RECID(h-artikel).

    fact-scvat = 1.
    service = 0.
    vat = 0.
    vat2 = 0.

    IF servtax-use-foart THEN
    DO:
        FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
            AND artikel.departement EQ h-artikel.departement NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN
        DO:
            ASSIGN
                serv-code = artikel.service-code
                vat-code = artikel.mwst-code
            .
        END.
    END.  
    ELSE
    DO:
        ASSIGN
            serv-code = h-artikel.service-code
            vat-code = h-artikel.mwst-code
        .
    END.

    FIND FIRST htparam WHERE htparam.paramnr = 135 NO-LOCK. 
    IF NOT htparam.flogical AND h-artikel.artart = 0 
        AND /*h-artikel.service-code*/ serv-code NE 0 THEN 
    DO: 
        FIND FIRST htparam WHERE htparam.paramnr = /*h-artikel.service-code*/ serv-code NO-LOCK NO-ERROR. 
        IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
        DO:
            IF NUM-ENTRIES(htparam.fchar, CHR(2)) GE 2 THEN
            ASSIGN service = DECIMAL(ENTRY(2, htparam.fchar, CHR(2))) / 10000.
            ELSE service = htparam.fdecimal.
        END.
    END.
    
    RUN htplogic.p(479, OUTPUT serv-vat).
    RUN htplogic.p(483, OUTPUT tax-vat).
                     
    FIND FIRST htparam WHERE paramnr = 134 NO-LOCK. 
    IF NOT vhp.htparam.flogical AND h-artikel.artart = 0 
        AND /*h-artikel.mwst-code*/ vat-code NE 0 THEN 
    DO: 
        FIND FIRST htparam WHERE htparam.paramnr = /*h-artikel.mwst-code*/ vat-code NO-LOCK NO-ERROR. 
        IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
        DO: 
            IF NUM-ENTRIES(htparam.fchar, CHR(2)) GE 2 THEN 
            ASSIGN vat = DECIMAL(ENTRY(2, htparam.fchar, CHR(2))) / 10000.
            ELSE vat = htparam.fdecimal.
            
            IF serv-vat AND NOT tax-vat THEN vat = vat + vat * service / 100.
            ELSE IF serv-vat AND tax-vat THEN vat = vat + vat * (service + vat2) / 100.
            ELSE IF NOT serv-vat AND tax-vat THEN vat = vat + vat * vat2 / 100.
            ASSIGN 
              ct     = REPLACE(STRING(vat), ".", ",")
              l-deci = LENGTH(ENTRY(2, ct, ",")) NO-ERROR
            .
            
            IF l-deci LE 2 THEN vat = ROUND(vat, 2).
            ELSE IF l-deci = 3 THEN vat = ROUND(vat, 3).
            ELSE vat = ROUND(vat, 4).
        END. 
    END.

    IF h-artikel.artart = 0 
        AND (h-artikel.artnr NE f-disc OR h-artikel.artnr NE b-disc OR h-artikel.artnr NE o-disc) THEN 
    DO:                
        IF serv-code NE 0 THEN service = service / 100.
        IF vat-code NE 0 THEN
        DO:
            ASSIGN
                vat     = vat / 100
                vat2    = vat2 / 100
            .   
        END.                        
        
        ASSIGN fact-scvat = 1 + service + vat + vat2.
        
        IF vat = 1 THEN 
        ASSIGN
        fact-scvat  = 1
        service     = 0
        vat2        = 0
        .   
        ELSE IF vat2 = 1 THEN 
        ASSIGN
        fact-scvat = 1
        service    = 0
        vat        = 0
        .   
        ELSE IF service = 1 THEN 
        ASSIGN
        fact-scvat = 1
        vat        = 0
        vat2       = 0
        .   
    END. 

    t-h-artikel1.amount-taxserv = h-artikel.epreis1 * fact-scvat.
    IF price-decimal EQ 0 THEN t-h-artikel1.amount-taxserv = ROUND(t-h-artikel1.amount-taxserv,0).    
    ELSE t-h-artikel1.amount-taxserv = ROUND(t-h-artikel1.amount-taxserv,2).

    /*FDL Oct 31, 2024: Ticket 7AD362*/
    FIND FIRST queasy WHERE queasy.KEY EQ 222 
         AND queasy.number1 EQ 2 
         AND queasy.number2 EQ h-artikel.artnr
         AND queasy.number3 EQ h-artikel.departement NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN
            t-h-artikel1.max-soldout-qty = INT(queasy.deci1)
            t-h-artikel1.soldout-flag = queasy.logi2
            .
    END. 

    IF t-h-artikel1.max-soldout-qty GT 0 THEN
    DO:
        curr-qty-posted = 0.
        FOR EACH h-journal WHERE h-journal.artnr EQ h-artikel.artnr
            AND h-journal.departement EQ h-artikel.departement
            AND h-journal.bill-datum EQ bill-date NO-LOCK:
            curr-qty-posted = curr-qty-posted + h-journal.anzahl.
        END.
        t-h-artikel1.posted-qty = curr-qty-posted.
    END.
END.

