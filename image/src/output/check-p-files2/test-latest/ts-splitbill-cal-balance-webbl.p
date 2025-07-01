
DEF TEMP-TABLE t-h-bill-line LIKE h-bill-line
    FIELD rec-id AS INTEGER.

DEFINE TEMP-TABLE ordered-item
    FIELD dept      AS INT
    FIELD artnr     AS INT
    FIELD rec-id    AS INT
    FIELD qty       AS INT
    FIELD epreis    AS DECIMAL
    FIELD net-bet   AS DECIMAL
    FIELD tax       AS DECIMAL
    FIELD service   AS DECIMAL
    FIELD bill-date AS DATE
    FIELD betrag    AS DECIMAL
    .

DEFINE TEMP-TABLE summary-bill
    FIELD subtotal      AS DECIMAL
    FIELD total-service AS DECIMAL
    FIELD total-tax     AS DECIMAL
    FIELD grand-total   AS DECIMAL
    .

DEFINE TEMP-TABLE t-h-artikel  LIKE h-artikel
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER curr-dept      AS INT.
DEF INPUT  PARAMETER curr-select    AS INT.
DEF INPUT  PARAMETER t-rechnr       AS INT.
DEF OUTPUT PARAMETER balance        AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill-line.
DEF OUTPUT PARAMETER TABLE FOR summary-bill. 
DEF OUTPUT PARAMETER TABLE FOR t-h-artikel.

DEFINE VARIABLE t-serv%         AS DECIMAL INITIAL 0.  
DEFINE VARIABLE t-mwst%         AS DECIMAL INITIAL 0.  
DEFINE VARIABLE t-fact          AS DECIMAL INITIAL 1.
DEFINE VARIABLE t-service       AS DECIMAL.
DEFINE VARIABLE t-mwst1         AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-mwst          AS DECIMAL INITIAL 0. 
DEFINE VARIABLE h-service       AS DECIMAL.  
DEFINE VARIABLE h-mwst          AS DECIMAL.  
DEFINE VARIABLE h-mwst2         AS DECIMAL.
DEFINE VARIABLE t-h-service     AS DECIMAL.  
DEFINE VARIABLE t-h-mwst        AS DECIMAL.  
DEFINE VARIABLE t-h-mwst2       AS DECIMAL.
DEFINE VARIABLE incl-service    AS LOGICAL.  
DEFINE VARIABLE incl-mwst       AS LOGICAL.
DEFINE VARIABLE gst-logic       AS LOGICAL INITIAL NO.
DEFINE VARIABLE serv-disc       AS LOGICAL INITIAL YES.
DEFINE VARIABLE vat-disc        AS LOGICAL INITIAL YES.
DEFINE VARIABLE f-discArt       AS INTEGER INITIAL -1 NO-UNDO. 
DEFINE VARIABLE amount          AS DECIMAL. 
DEFINE VARIABLE f-dec           AS DECIMAL.

/*FD Dec 09, 2021*/
DEFINE VARIABLE serv-code       AS INTEGER. 
DEFINE VARIABLE vat-code        AS INTEGER. 
DEFINE VARIABLE servtax-use-foart AS LOGICAL. 
DEFINE VARIABLE serv-vat        AS LOGICAL NO-UNDO. 
DEFINE VARIABLE tax-vat         AS LOGICAL NO-UNDO. 
DEFINE VARIABLE ct              AS CHAR    NO-UNDO.
DEFINE VARIABLE l-deci          AS INTEGER NO-UNDO INIT 2.
DEFINE VARIABLE fact-scvat      AS DECIMAL NO-UNDO INIT 1.
DEFINE VARIABLE service         AS DECIMAL.
DEFINE VARIABLE vat             AS DECIMAL.
DEFINE VARIABLE vat2            AS DECIMAL.
DEFINE VARIABLE mwst            AS DECIMAL.
DEFINE VARIABLE mwst1           AS DECIMAL.

DEFINE VARIABLE sub-tot   AS DECIMAL.
DEFINE VARIABLE tot-serv  AS DECIMAL.
DEFINE VARIABLE tot-tax   AS DECIMAL.
DEFINE VARIABLE grand-tot AS DECIMAL.

DEFINE VARIABLE netto-bet    AS DECIMAL. /*FD*/

DEFINE VARIABLE cashless-flag  AS LOGICAL NO-UNDO.
DEFINE VARIABLE cashless-artnr AS INTEGER NO-UNDO INIT ?.

FIND FIRST htparam WHERE htparam.paramnr = 468 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN serv-disc = htparam.flogic.

FIND FIRST htparam WHERE htparam.paramnr = 469 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN vat-disc = htparam.flogic.

FIND FIRST vhp.htparam WHERE paramnr = 557 NO-LOCK. /*rest food disc artNo */   
IF vhp.htparam.finteger NE 0 THEN f-discArt = vhp.htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 376 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
DO:
    IF NOT htparam.flogic AND ENTRY(1,htparam.fchar,";") = "GST(MA)" THEN
    gst-logic = YES.
END.
FIND FIRST vhp.htparam WHERE paramnr = 135 NO-LOCK. 
incl-service = vhp.htparam.flogical. 
 
FIND FIRST vhp.htparam WHERE paramnr = 134 NO-LOCK. 
incl-mwst = vhp.htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 834 NO-LOCK.
ASSIGN cashless-flag = htparam.flogical.
IF cashless-flag THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 569 NO-LOCK.
  IF htparam.paramnr NE 0 THEN 
    ASSIGN cashless-artnr = htparam.finteger.
END.

/*FD Dec 09, 2021*/
FIND FIRST hoteldpt WHERE hoteldpt.num EQ curr-dept NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN servtax-use-foart = hoteldpt.defult.

RUN htplogic.p(479, OUTPUT serv-vat).
RUN htplogic.p(483, OUTPUT tax-vat).

FOR EACH h-artikel WHERE h-artikel.departement = curr-dept
    AND (h-artikel.artart = 2 OR h-artikel.artart = 6
    OR h-artikel.artart = 7 OR h-artikel.artart = 11
    OR h-artikel.artart = 12) NO-LOCK:
    CREATE t-h-artikel.
    BUFFER-COPY h-artikel TO t-h-artikel.
    ASSIGN t-h-artikel.rec-id = INTEGER(RECID(h-artikel)).
    IF t-h-artikel.artnr = cashless-artnr THEN
    ASSIGN t-h-artikel.bezeich = REPLACE(t-h-artikel.bezeich, " ", "").
END.

IF curr-select GT 0 THEN 
DO: 
    FOR EACH h-bill-line WHERE h-bill-line.rechnr = t-rechnr 
        AND h-bill-line.waehrungsnr = curr-select NO-LOCK:
        CREATE t-h-bill-line.
        BUFFER-COPY h-bill-line TO t-h-bill-line.
        ASSIGN t-h-bill-line.rec-id = RECID(h-bill-line).

        CREATE ordered-item.
        ASSIGN 
            ordered-item.dept    = t-h-bill-line.departement
            ordered-item.artnr   = t-h-bill-line.artnr    
            ordered-item.rec-id  = t-h-bill-line.rec-id   
            ordered-item.qty     = t-h-bill-line.anzahl   
            ordered-item.epreis  = t-h-bill-line.epreis   
            ordered-item.net-bet = t-h-bill-line.nettobetrag
            ordered-item.bill-date = t-h-bill-line.bill-datum
            ordered-item.betrag  = t-h-bill-line.betrag. 
    END.
END. 
ELSE 
DO: 
    FOR EACH h-bill-line WHERE h-bill-line.rechnr = t-rechnr NO-LOCK:
        CREATE t-h-bill-line.
        BUFFER-COPY h-bill-line TO t-h-bill-line.
        ASSIGN t-h-bill-line.rec-id = RECID(h-bill-line).

        CREATE ordered-item.
        ASSIGN 
            ordered-item.dept    = t-h-bill-line.departement
            ordered-item.artnr   = t-h-bill-line.artnr    
            ordered-item.rec-id  = t-h-bill-line.rec-id   
            ordered-item.qty     = t-h-bill-line.anzahl   
            ordered-item.epreis  = t-h-bill-line.epreis   
            ordered-item.net-bet = t-h-bill-line.nettobetrag
            ordered-item.bill-date = t-h-bill-line.bill-datum
            ordered-item.betrag  = t-h-bill-line.betrag. 
    END. 
END. 

FOR EACH ordered-item:
    t-h-service = 0.
    t-h-mwst = 0.
    t-h-mwst2 = 0.
    h-service = 0.
    h-mwst = 0.
    service = 0.
    mwst = 0.

    FIND FIRST h-artikel WHERE h-artikel.departement EQ dept AND h-artikel.artnr EQ ordered-item.artnr 
        AND h-artikel.artart EQ 0 NO-LOCK NO-ERROR.
    IF AVAILABLE h-artikel THEN
    DO:
        netto-bet = netto-bet + (ordered-item.epreis * ordered-item.qty).
        IF NOT servtax-use-foart THEN
        DO:
            ASSIGN
                serv-code = h-artikel.service-code
                vat-code = h-artikel.mwst-code
            .
        END.
        ELSE
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
    END.

    IF AVAILABLE h-artikel THEN
    DO:
        IF ordered-item.artnr NE f-discArt THEN
        DO:
            IF serv-code NE 0 AND NOT incl-service THEN
            DO:
                FIND FIRST htparam WHERE htparam.paramnr EQ serv-code NO-LOCK NO-ERROR.                        
                IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
                DO:
                    IF NUM-ENTRIES(htparam.fchar, CHR(2)) GE 2 THEN
                        ASSIGN t-h-service = DECIMAL(ENTRY(2, htparam.fchar, CHR(2))) / 10000.
                    ELSE t-h-service = htparam.fdecimal.
                END.
            END.
            
            IF vat-code NE 0 AND NOT incl-mwst THEN
            DO:
                FIND FIRST htparam WHERE htparam.paramnr EQ vat-code NO-LOCK NO-ERROR. 
                IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
                DO: 
                    IF NUM-ENTRIES(htparam.fchar, CHR(2)) GE 2 THEN
                        ASSIGN t-h-mwst = DECIMAL(ENTRY(2, htparam.fchar, CHR(2))) / 10000.
                    ELSE t-h-mwst = htparam.fdecimal.

                    IF serv-vat AND NOT tax-vat THEN 
                        t-h-mwst = t-h-mwst + t-h-mwst * t-h-service / 100.
                    ELSE IF serv-vat AND tax-vat THEN 
                        t-h-mwst = t-h-mwst + t-h-mwst * (t-h-service + t-h-mwst2) / 100.
                    ELSE IF NOT serv-vat AND tax-vat THEN 
                        t-h-mwst = t-h-mwst + t-h-mwst * t-h-mwst2 / 100.

                    ASSIGN 
                        ct     = REPLACE(STRING(t-h-mwst), ".", ",")
                        l-deci = LENGTH(ENTRY(2, ct, ",")) NO-ERROR
                    .
                    IF l-deci LE 2     THEN t-h-mwst = ROUND(t-h-mwst, 2).
                    ELSE IF l-deci = 3 THEN t-h-mwst = ROUND(t-h-mwst, 3).
                    ELSE t-h-mwst = ROUND(t-h-mwst, 4).
                END.
            END.
           
        
            IF t-h-service NE 0 OR t-h-mwst NE 0 THEN
            DO:
                ASSIGN
                    t-h-service = t-h-service / 100
                    t-h-mwst = t-h-mwst / 100
                    t-h-mwst2 = t-h-mwst2 / 100
                .
   
                fact-scvat = 1 + t-h-service + t-h-mwst + t-h-mwst2. 
                h-service = ordered-item.betrag / fact-scvat * t-h-service.
                h-service = ROUND(h-service, 2).
                h-mwst = ordered-item.betrag / fact-scvat * t-h-mwst.
                h-mwst = ROUND(h-mwst, 2).

                IF NOT incl-service THEN service = service + h-service.
                
                IF NOT incl-mwst THEN 
                DO:
                    mwst   = mwst   + h-mwst.
                    mwst1  = mwst1  + h-mwst.
                END.  
            END.                      
        END.
        ELSE
        DO:
            IF serv-code NE 0 AND NOT incl-service AND serv-disc THEN
            DO:
                FIND FIRST htparam WHERE htparam.paramnr EQ serv-code NO-LOCK NO-ERROR.                        
                IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
                DO:
                    IF NUM-ENTRIES(htparam.fchar, CHR(2)) GE 2 THEN
                        ASSIGN t-h-service = DECIMAL(ENTRY(2, htparam.fchar, CHR(2))) / 10000.
                    ELSE t-h-service = htparam.fdecimal.
                END.
            END.
            
            IF vat-code NE 0 AND NOT incl-mwst AND vat-disc THEN
            DO:
                FIND FIRST htparam WHERE htparam.paramnr EQ vat-code NO-LOCK NO-ERROR. 
                IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
                DO: 
                    IF NUM-ENTRIES(htparam.fchar, CHR(2)) GE 2 THEN
                        ASSIGN t-h-mwst = DECIMAL(ENTRY(2, htparam.fchar, CHR(2))) / 10000.
                    ELSE t-h-mwst = htparam.fdecimal.

                    IF serv-vat AND NOT tax-vat THEN 
                        t-h-mwst = t-h-mwst + t-h-mwst * t-h-service / 100.
                    ELSE IF serv-vat AND tax-vat THEN 
                        t-h-mwst = t-h-mwst + t-h-mwst * (t-h-service + t-h-mwst2) / 100.
                    ELSE IF NOT serv-vat AND tax-vat THEN 
                        t-h-mwst = t-h-mwst + t-h-mwst * t-h-mwst2 / 100.

                    ASSIGN 
                        ct     = REPLACE(STRING(t-h-mwst), ".", ",")
                        l-deci = LENGTH(ENTRY(2, ct, ",")) NO-ERROR
                    .
                    IF l-deci LE 2     THEN t-h-mwst = ROUND(t-h-mwst, 2).
                    ELSE IF l-deci = 3 THEN t-h-mwst = ROUND(t-h-mwst, 3).
                    ELSE t-h-mwst = ROUND(t-h-mwst, 4).
                END.
            END.
           
            IF ordered-item.epreis NE ordered-item.betrag THEN
            DO:
                IF t-h-service NE 0 OR t-h-mwst NE 0 THEN
                DO:
                    ASSIGN
                        t-h-service = t-h-service / 100
                        t-h-mwst = t-h-mwst / 100
                        t-h-mwst2 = t-h-mwst2 / 100
                    .
       
                    fact-scvat = 1 + t-h-service + t-h-mwst + t-h-mwst2. 
                    h-service = ordered-item.betrag / fact-scvat * t-h-service.
                    h-service = ROUND(h-service, 2).
                    h-mwst = ordered-item.betrag / fact-scvat * t-h-mwst.
                    h-mwst = ROUND(h-mwst, 2).
    
                    IF NOT incl-service THEN service = service + h-service.
                    
                    IF NOT incl-mwst THEN 
                    DO:
                        mwst   = mwst   + h-mwst.
                        mwst1  = mwst1  + h-mwst.
                    END.  
                END.
            END.                                       
        END.

        ordered-item.service = service.
        ordered-item.tax     = mwst.
    END.
END.

FOR EACH ordered-item:
    sub-tot   = netto-bet.
    tot-serv  = tot-serv + ordered-item.service.
    tot-tax   = tot-tax + ordered-item.tax.
END.
grand-tot = sub-tot + tot-serv + tot-tax.

CREATE summary-bill.
ASSIGN 
    summary-bill.subtotal       = sub-tot
    summary-bill.total-service  = tot-serv
    summary-bill.total-tax      = tot-tax
    summary-bill.grand-total    = ROUND(grand-tot, 0)
    . 
/*
PROCEDURE cal-servat:  
    DEF INPUT PARAMETER depart          AS INT.  
    DEF INPUT PARAMETER h-artnr         AS INT.  
    DEF INPUT PARAMETER service-code    AS INT.  
    DEF INPUT PARAMETER mwst-code       AS INT.
    DEF INPUT PARAMETER inpDate         AS DATE.
    DEF OUTPUT PARAMETER serv%          AS DECIMAL INITIAL 0.  
    DEF OUTPUT PARAMETER mwst%          AS DECIMAL INITIAL 0.  
    DEF OUTPUT PARAMETER servat         AS DECIMAL INITIAL 0. 
      
    DEF VAR serv-htp AS DECIMAL            NO-UNDO.  
    DEF VAR vat-htp  AS DECIMAL            NO-UNDO.  
    DEF VAR vat2     AS DECIMAL INITIAL 0.  
      
    DEF BUFFER hbuff FOR vhp.h-artikel.  
    DEF BUFFER aBuff FOR vhp.artikel.  
      
        FIND FIRST hbuff WHERE hbuff.artnr = h-artnr AND hbuff.departement = depart NO-LOCK.    
        FIND FIRST abuff WHERE abuff.artnr = hbuff.artnrfront AND abuff.departement = depart NO-LOCK.  
    
        /* SY AUG 13 2017 */
        RUN calc-servtaxesbl.p(1, abuff.artnr, abuff.departement, inpDate, OUTPUT serv%, OUTPUT mwst%, OUTPUT vat2, OUTPUT servat).
        ASSIGN mwst% = mwst% + vat2.

END. 
*/
