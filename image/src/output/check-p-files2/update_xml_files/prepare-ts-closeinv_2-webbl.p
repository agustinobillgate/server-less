
DEFINE TEMP-TABLE b-list    LIKE h-bill-line
    FIELD rec-id AS INTEGER.
DEFINE TEMP-TABLE t-b-list  LIKE h-bill-line
    FIELD rec-id AS INTEGER
    FIELD t-time  AS CHAR. /*bernatd FA0A2F 2025*/ 
DEFINE TEMP-TABLE t-h-bill  LIKE h-bill
    FIELD rec-id AS INT.
DEFINE TEMP-TABLE t-h-artikel  LIKE h-artikel
    FIELD rec-id AS INT.
DEFINE TEMP-TABLE t-h-artsales LIKE h-artikel
    FIELD rec-id AS INT.

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

/**/
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER curr-dept      AS INT.
DEF INPUT  PARAMETER inp-rechnr     AS INT.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER user-name      AS CHAR.
DEF INPUT  PARAMETER curr-printer   AS INT.

DEF OUTPUT PARAMETER must-print     AS LOGICAL.
DEF OUTPUT PARAMETER rev-sign       AS INT INIT 1.
DEF OUTPUT PARAMETER cancel-exist   AS LOGICAL.
DEF OUTPUT PARAMETER price-decimal  AS INT.
DEF OUTPUT PARAMETER curr-local     AS CHAR.
DEF OUTPUT PARAMETER curr-foreign   AS CHAR.
DEF OUTPUT PARAMETER double-currency AS LOGICAL.
DEF OUTPUT PARAMETER foreign-rate   AS LOGICAL.
DEF OUTPUT PARAMETER exchg-rate     AS DECIMAL INIT 1.
DEF OUTPUT PARAMETER f-disc         AS INT INIT 0.
DEF OUTPUT PARAMETER b-artnr        AS INT INIT 0.
DEF OUTPUT PARAMETER b-title        AS CHAR.
DEF OUTPUT PARAMETER deptname       AS CHAR.
DEF OUTPUT PARAMETER curr-user      AS CHAR.
DEF OUTPUT PARAMETER curr-waiter    AS INT INIT 1.
DEF OUTPUT PARAMETER tischnr        AS INT.
DEF OUTPUT PARAMETER rechnr         AS INT.
DEF OUTPUT PARAMETER pax            AS INT.
DEF OUTPUT PARAMETER balance        AS DECIMAL.
DEF OUTPUT PARAMETER balance-foreign AS DECIMAL.
DEF OUTPUT PARAMETER bcol           AS INT INIT 2.
DEF OUTPUT PARAMETER printed        AS CHAR INIT "".

DEF OUTPUT PARAMETER bill-date      AS DATE.
DEF OUTPUT PARAMETER kreditlimit    AS DECIMAL.
DEF OUTPUT PARAMETER total-saldo    AS DECIMAL.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER msg-str1       AS CHAR.
DEF OUTPUT PARAMETER rec-kellner    AS INT.
DEF OUTPUT PARAMETER rec-bill-guest AS INT.
DEF OUTPUT PARAMETER cashless-flag  AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER cashless-artnr AS INTEGER NO-UNDO INIT ?.
DEF OUTPUT PARAMETER multi-cash     AS LOGICAL.
DEF OUTPUT PARAMETER o-disc         AS INT INIT 0.

DEF OUTPUT PARAMETER TABLE FOR t-b-list.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.
DEF OUTPUT PARAMETER TABLE FOR t-h-artikel.
DEF OUTPUT PARAMETER TABLE FOR t-h-artsales.
DEF OUTPUT PARAMETER TABLE FOR summary-bill. 
/*
DEF var  pvILanguage    AS INTEGER NO-UNDO.
DEF var  curr-dept      AS INT.
DEF var  inp-rechnr     AS INT.
DEF var  user-init      AS CHAR.
DEF var  user-name      AS CHAR.
DEF var  curr-printer   AS INT.
    
DEF var  must-print     AS LOGICAL.
DEF var  rev-sign       AS INT INIT 1.
DEF var  cancel-exist   AS LOGICAL.
DEF var  price-decimal  AS INT.
DEF var  curr-local     AS CHAR.
DEF var  curr-foreign   AS CHAR.
DEF var  double-currency AS LOGICAL.
DEF var  foreign-rate   AS LOGICAL.
DEF var  exchg-rate     AS DECIMAL INIT 1.
DEF var  f-disc         AS INT INIT 0.
DEF var  b-artnr        AS INT INIT 0.
DEF var  b-title        AS CHAR.
DEF var  deptname       AS CHAR.
DEF var  curr-user      AS CHAR.
DEF var  curr-waiter    AS INT INIT 1.
DEF var  tischnr        AS INT.
DEF var  rechnr         AS INT.
DEF var  pax            AS INT.
DEF var  balance        AS DECIMAL.
DEF var  balance-foreign AS DECIMAL.
DEF var  bcol           AS INT INIT 2.
DEF var  printed        AS CHAR INIT "".
    
DEF var  bill-date      AS DATE.
DEF var  kreditlimit    AS DECIMAL.
DEF var  total-saldo    AS DECIMAL.
DEF var  msg-str        AS CHAR.
DEF var  msg-str1       AS CHAR.
DEF var  rec-kellner    AS INT.
DEF var  rec-bill-guest AS INT.
DEF var  cashless-flag  AS LOGICAL NO-UNDO.
DEF var  cashless-artnr AS INTEGER NO-UNDO INIT ?.
DEF var  multi-cash     AS LOGICAL.


pvILanguage     = 1.
curr-dept       = 1.
inp-rechnr      = 7198.
user-init       = "01".
user-name       = "sindata".
curr-printer    = 99.
*/
{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-closeinv".

DEFINE VARIABLE fogl-date   AS DATE NO-UNDO.
DEFINE BUFFER   bill-guest  FOR vhp.guest. 

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

DEFINE VARIABLE netto-bet   AS DECIMAL. /*FD*/
DEFINE VARIABLE compli-flag AS LOGICAL. /*FD*/
DEFINE VARIABLE serv%       AS DECIMAL.
DEFINE VARIABLE vat%        AS DECIMAL.
DEFINE VARIABLE vat2%       AS DECIMAL.
DEFINE VARIABLE servat%     AS DECIMAL.

DEFINE BUFFER buff-hart FOR h-artikel.
DEFINE BUFFER aBuff FOR artikel. 

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
bill-date = vhp.htparam.fdate.

FIND FIRST vhp.htparam WHERE paramnr = 557 NO-LOCK. /*rest food disc artNo */   
IF vhp.htparam.finteger NE 0 THEN f-discArt = vhp.htparam.finteger.

/* SY 27/02/2014 */
FIND FIRST htparam WHERE htparam.paramnr = 834 NO-LOCK.
ASSIGN cashless-flag = htparam.flogical.
IF cashless-flag THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 569 NO-LOCK.
  IF htparam.paramnr NE 0 THEN 
    ASSIGN cashless-artnr = htparam.finteger.
END.

FIND FIRST vhp.htparam WHERE htpara.paramnr = 833 NO-LOCK. 
multi-cash = flogical. 

FIND FIRST vhp.htparam WHERE htpara.paramnr = 1003 NO-LOCK. 
fogl-date = vhp.htparam.fdate. 
FIND FIRST vhp.h-bill-line WHERE vhp.h-bill-line.departement = curr-dept 
  AND vhp.h-bill-line.rechnr = inp-rechnr NO-LOCK NO-ERROR.
IF AVAILABLE vhp.h-bill-line AND vhp.h-bill-line.bill-datum LE fogl-date THEN
DO:
  msg-str = msg-str + CHR(2) + "&W"
          + translateExtended ("Bill older than last transfer date to G/L (Param 1003).",lvCAREA,"").
END.

FIND FIRST vhp.htparam WHERE htpara.paramnr = 877 NO-LOCK. 
must-print = flogical. 
RUN determine-revsign.

FIND FIRST vhp.htparam WHERE htpara.paramnr = 867 NO-LOCK. 
FIND FIRST bill-guest WHERE bill-guest.gastnr = vhp.htparam.finteger 
  NO-LOCK NO-ERROR. 
IF NOT AVAILABLE bill-guest THEN 
DO:
  msg-str1 = msg-str1 + CHR(2)
           + translateExtended ("GuestNo (Param 867) for credit restaurant undefined",lvCAREA,"")
           + CHR(10)
           + translateExtended ("Posting not possible.",lvCAREA,"").
  RETURN. 
END. 

FIND FIRST vhp.queasy WHERE vhp.queasy.key = 11 NO-LOCK NO-ERROR. 
cancel-exist = AVAILABLE vhp.queasy. 
 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 491 NO-LOCK. 
price-decimal = vhp.htparam.finteger.   /* non-digit OR digit version */ 
 
FIND FIRST vhp.htparam WHERE paramnr = 152 NO-LOCK. 
curr-local = fchar. 
FIND FIRST vhp.htparam WHERE paramnr = 144 NO-LOCK. 
curr-foreign = fchar. 
 
FIND FIRST vhp.htparam WHERE paramnr = 240 NO-LOCK. 
double-currency = vhp.htparam.flogical.


FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 143 NO-LOCK. 
foreign-rate = vhp.htparam.flogical. 
 
IF FOREIGN-RATE OR DOUBLE-CURRENCY THEN 
DO: 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST vhp.waehrung WHERE vhp.waehrung.wabkurz 
    = vhp.htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.waehrung THEN exchg-rate 
    = vhp.waehrung.ankauf / vhp.waehrung.einheit. 
END. 
 
FIND FIRST vhp.htparam WHERE paramnr = 557 no-lock. /*rest artnr food disc*/ 
f-disc = vhp.htparam.finteger. 
FIND FIRST vhp.htparam WHERE paramnr = 596 no-lock. /*rest artnr bev disc*/ 
b-artnr = vhp.htparam.finteger.
FIND FIRST vhp.htparam WHERE paramnr = 556 no-lock. /*rest artnr food disc*/ 
o-disc = vhp.htparam.finteger. 
/* FDL Comment
FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.htparam.finteger 
  AND vhp.h-artikel.departement = curr-dept NO-LOCK NO-ERROR. 
IF AVAILABLE h-artikel THEN 
  FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.h-artikel.artnrfront 
  AND vhp.artikel.departement = curr-dept NO-LOCK. 
IF AVAILABLE vhp.artikel THEN b-artnr = vhp.artikel.artnr. 
*/
/*FD Dec 09, 2021*/
FIND FIRST hoteldpt WHERE hoteldpt.num EQ curr-dept NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN servtax-use-foart = hoteldpt.defult.

FIND FIRST htparam WHERE htparam.paramnr = 468 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN serv-disc = htparam.flogic.

FIND FIRST htparam WHERE htparam.paramnr = 469 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN vat-disc = htparam.flogic.

FIND FIRST vhp.htparam WHERE paramnr = 135 NO-LOCK. 
incl-service = vhp.htparam.flogical. 
 
FIND FIRST vhp.htparam WHERE paramnr = 134 NO-LOCK. 
incl-mwst = vhp.htparam.flogical. 

RUN htplogic.p(479, OUTPUT serv-vat).
RUN htplogic.p(483, OUTPUT tax-vat).

FIND FIRST vhp.hoteldpt WHERE vhp.hoteldpt.num = curr-dept NO-LOCK. 
b-title = vhp.hoteldpt.depart. 
IF AVAILABLE vhp.waehrung THEN 
  b-title = b-title + " ! " 
    + translateExtended ("Today's Exchange Rate",lvCAREA,"") 
    + " = " + STRING(exchg-rate). 
deptname = vhp.hoteldpt.depart. 

/* Eko 22 jan 2016 */
FIND FIRST htparam WHERE htparam.paramnr = 300 NO-LOCK. /* micros flag */
deptname = deptname + CHR(3) + STRING(htparam.flogical).

FIND FIRST vhp.h-bill WHERE vhp.h-bill.rechnr = inp-rechnr
  AND vhp.h-bill.departement = curr-dept NO-LOCK NO-ERROR.
IF AVAILABLE vhp.h-bill THEN 
DO:
    FIND FIRST vhp.kellner WHERE vhp.kellner.kellner-nr = vhp.h-bill.kellner-nr
      AND vhp.kellner.departement = vhp.h-bill.departement NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.kellner THEN curr-user = vhp.kellner.kellnername.
    ELSE curr-user = user-init + " " + user-name. 
         
    CREATE t-h-bill.
    BUFFER-COPY h-bill TO t-h-bill.
    ASSIGN t-h-bill.rec-id = RECID(h-bill).
END. 
ELSE curr-user = user-init + " " + user-name. 
IF AVAILABLE kellner THEN rec-kellner = RECID(kellner).
IF curr-printer NE 0 THEN curr-waiter = INTEGER(user-init). 
FIND FIRST vhp.kellner WHERE vhp.kellner.kellner-nr = curr-waiter 
  AND vhp.kellner.departement = curr-dept NO-LOCK NO-ERROR. 

RUN open-table.

RUN cal-total-saldo.

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
IF AVAILABLE bill-guest THEN rec-bill-guest = RECID(bill-guest).

FOR EACH h-artikel WHERE h-artikel.departement = curr-dept
    AND h-artikel.artart = 0 NO-LOCK:
    CREATE t-h-artsales.
    BUFFER-COPY h-artikel TO t-h-artsales.
    ASSIGN t-h-artsales.rec-id = INTEGER(RECID(h-artikel)).
END.

FOR EACH ordered-item:
    t-h-service = 0.
    t-h-mwst = 0.
    t-h-mwst2 = 0.
    h-service = 0.
    h-mwst = 0.
    service = 0.
    mwst = 0.

    IF ordered-item.bill-date LT bill-date THEN
    DO:
        FIND FIRST buff-hart WHERE buff-hart.artnr EQ ordered-item.artnr 
            AND buff-hart.departement EQ ordered-item.dept NO-LOCK.
        FIND FIRST abuff WHERE abuff.artnr EQ buff-hart.artnrfront  
            AND abuff.departement EQ buff-hart.departement NO-LOCK.

        /*FDL May 03, 2024 => Ticket C9F31A*/
        RUN calc-servtaxesbl.p(1, abuff.artnr, abuff.departement, 
            ordered-item.bill-date, OUTPUT serv%, OUTPUT vat%, OUTPUT vat2%, OUTPUT servat%).

        ordered-item.service = serv%.
        ordered-item.tax     = vat% + vat2%.
    END.
    ELSE
    DO:
        FIND FIRST h-artikel WHERE h-artikel.departement EQ ordered-item.dept 
            AND h-artikel.artnr EQ ordered-item.artnr 
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
END.

FOR EACH ordered-item,
    FIRST buff-hart WHERE buff-hart.artnr EQ ordered-item.artnr 
    AND buff-hart.departement EQ ordered-item.dept NO-LOCK:

    sub-tot   = netto-bet.
    tot-serv  = tot-serv + ordered-item.service.
    tot-tax   = tot-tax + ordered-item.tax.

    IF buff-hart.artart EQ 11 OR buff-hart.artart EQ 12 THEN compli-flag = YES.
END.
IF compli-flag THEN
DO:
    tot-serv = 0.
    tot-tax = 0.
END.

grand-tot = sub-tot + tot-serv + tot-tax.

CREATE summary-bill.
ASSIGN 
    summary-bill.subtotal       = sub-tot
    summary-bill.total-service  = tot-serv
    summary-bill.total-tax      = tot-tax
    summary-bill.grand-total    = ROUND(grand-tot,price-decimal)
    .

/*************************************PROCEDURE************************************/
PROCEDURE determine-revsign: 
DEFINE VARIABLE s AS DECIMAL INITIAL 0. 
  FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = inp-rechnr 
    AND vhp.h-bill-line.departement = curr-dept NO-LOCK, 
    FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.h-bill-line.artnr 
    AND vhp.h-artikel.departement = vhp.h-bill-line.departement 
    AND vhp.h-artikel.artart = 0 NO-LOCK: 
    s = s + vhp.h-bill-line.betrag. 
  END. 
  IF s LT 0 THEN rev-sign = - 1. 
END. 

PROCEDURE open-table:
  RUN create-blist.
 
  FIND FIRST vhp.htparam WHERE htpara.paramnr = 867 NO-LOCK.
  FIND FIRST bill-guest WHERE bill-guest.gastnr = vhp.htparam.finteger NO-LOCK 
    NO-ERROR.
  kreditlimit = bill-guest.kreditlimit. 
  
  FIND FIRST vhp.h-bill WHERE vhp.h-bill.departement = curr-dept 
    AND vhp.h-bill.rechnr = inp-rechnr AND vhp.h-bill.flag = 1 NO-LOCK NO-ERROR.
  IF AVAILABLE vhp.h-bill THEN 
  DO: 
    FIND FIRST vhp.tisch WHERE vhp.tisch.tischnr = vhp.h-bill.tischnr. 
    tischnr = vhp.tisch.tischnr. 
    rechnr = vhp.h-bill.rechnr. 
    RUN disp-bill-line.
 
    pax = vhp.h-bill.belegung. 
    balance = vhp.h-bill.saldo. 
    balance-foreign = vhp.h-bill.mwst[99]. 
    IF balance LE kreditlimit THEN bcol = 2. 
/*    ELSE bcol = 12. */ 
    IF vhp.h-bill.rgdruck = 0 THEN printed = "". 
    ELSE printed = "*". 
    /*MTDISP tischnr pax balance /*printed*/ WITH FRAME frame1.*/
    IF double-currency THEN 
    DO: 
      /*MTDISP balance-foreign WITH FRAME frame1. 
      b11:TITLE IN FRAME frame1 = b-title   + "  " 
          + translateExtended ("BillNo",lvCAREA,"") + " " + STRING(rechnr).*/
    END. 
    ELSE /*MTb1:TITLE IN FRAME frame1 = b-title + "  " 
        + translateExtended ("BillNo",lvCAREA,"") + " " + STRING(rechnr)*/.
    /*MTENABLE btn-cash btn-ccard btn-transfer WITH FRAME frame1.*/
    IF vhp.h-bill.betriebsnr NE 0 THEN 
    DO: 
      FIND FIRST vhp.queasy WHERE vhp.queasy.key = 10 
        AND vhp.queasy.number1 = vhp.h-bill.betriebsnr NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.queasy THEN 
      DO: 
        curr-user = TRIM(curr-user + " - " + vhp.queasy.char1). 
        /*MTDISP curr-user WITH FRAME frame1.*/
      END. 
    END. 
    /*MTIF double-currency THEN APPLY "entry" TO b11. 
    ELSE APPLY "entry" TO b1. */
    RETURN NO-APPLY. 
  END. 
END. 


PROCEDURE create-blist: 
DEFINE buffer h-art FOR vhp.h-artikel. 
DEFINE VARIABLE create-it AS LOGICAL. 
   
  FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = inp-rechnr 
    AND vhp.h-bill-line.departement = curr-dept NO-LOCK 
    BY vhp.h-bill-line.waehrungsnr: 
    create-it = YES. 
    FIND FIRST h-art WHERE h-art.artnr = vhp.h-bill-line.artnr 
      AND h-art.departement = vhp.h-bill-line.departement NO-LOCK NO-ERROR. 
    IF (AVAILABLE h-art AND h-art.artart NE 0) OR h-bill-line.artnr = 0 THEN 
    DO: 
      FIND FIRST b-list WHERE b-list.artnr = vhp.h-bill-line.artnr 
        AND b-list.betrag = - vhp.h-bill-line.betrag 
        AND b-list.bill-datum = vhp.h-bill-line.bill-datum NO-ERROR. 
      IF AVAILABLE b-list THEN 
      DO: 
        delete b-list. 
        create-it = NO. 
      END. 
      ELSE bill-date = vhp.h-bill-line.bill-datum. 
    END. 
    IF create-it THEN 
    DO: 
      CREATE b-list. 
      ASSIGN 
        b-list.rechnr = inp-rechnr 
        b-list.artnr = vhp.h-bill-line.artnr 
        b-list.bezeich = vhp.h-bill-line.bezeich 
        b-list.anzahl = vhp.h-bill-line.anzahl 
        b-list.nettobetrag = vhp.h-bill-line.nettobetrag 
        b-list.fremdwbetrag = vhp.h-bill-line.fremdwbetrag 
        b-list.betrag = vhp.h-bill-line.betrag 
        b-list.tischnr = vhp.h-bill-line.tischnr 
        b-list.departement = vhp.h-bill-line.departement 
        b-list.epreis = vhp.h-bill-line.epreis 
        b-list.zeit = vhp.h-bill-line.zeit 
        b-list.bill-datum = vhp.h-bill-line.bill-datum 
        b-list.sysdate = vhp.h-bill-line.sysdate 
        b-list.segmentcode = vhp.h-bill-line.segmentcode 
        b-list.waehrungsnr = vhp.h-bill-line.waehrungsnr 
        b-list.transferred = YES
        b-list.rec-id = RECID(h-bill-line). 
    END. 
  END. 
  IF vhp.htparam.fdate NE bill-date AND double-currency THEN 
  DO: 
    FIND FIRST vhp.exrate WHERE vhp.exrate.datum = bill-date NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.exrate THEN exchg-rate = vhp.exrate.betrag. 
  END. 
END. 

PROCEDURE disp-bill-line: 
  IF double-currency THEN 
  FOR EACH b-list WHERE b-list.rechnr = vhp.h-bill.rechnr 
      AND b-list.departement = curr-dept NO-LOCK 
      BY b-list.sysdate descending BY b-list.zeit descending:
      CREATE t-b-list.
      BUFFER-COPY b-list TO t-b-list.
      ASSIGN t-b-list.t-time = STRING(b-list.zeit, "HH:MM:SS"). /*bernatd FA0A2F 2025*/ 
    
      CREATE ordered-item.
        ASSIGN 
           ordered-item.dept    = b-list.departement
           ordered-item.artnr   = b-list.artnr    
           ordered-item.rec-id  = RECID(b-list)  
           ordered-item.qty     = b-list.anzahl   
           ordered-item.epreis  = b-list.epreis   
           ordered-item.net-bet = b-list.nettobetrag
           ordered-item.bill-date = b-list.bill-datum
           ordered-item.betrag  = b-list.betrag. 
  END.
  ELSE 
  FOR EACH b-list WHERE b-list.rechnr = vhp.h-bill.rechnr 
      AND b-list.departement = curr-dept NO-LOCK 
      BY b-list.sysdate descending BY b-list.zeit descending:
      CREATE t-b-list.
      BUFFER-COPY b-list TO t-b-list.
      ASSIGN t-b-list.t-time = STRING(b-list.zeit, "HH:MM:SS"). /*bernatd FA0A2F 2025*/ 

      CREATE ordered-item.
        ASSIGN 
           ordered-item.dept    = b-list.departement
           ordered-item.artnr   = b-list.artnr    
           ordered-item.rec-id  = RECID(b-list)    
           ordered-item.qty     = b-list.anzahl   
           ordered-item.epreis  = b-list.epreis   
           ordered-item.net-bet = b-list.nettobetrag
           ordered-item.bill-date = b-list.bill-datum
           ordered-item.betrag  = b-list.betrag.  
  END.
END. 

PROCEDURE cal-total-saldo: 
  total-saldo = 0. 
  FIND FIRST vhp.h-bill WHERE vhp.h-bill.rechnr = inp-rechnr /* Malik Serverless 623 add this find fisrt inside procedure because find first outsid procedure not recognize in python */
  AND vhp.h-bill.departement = curr-dept NO-LOCK NO-ERROR.
  IF AVAILABLE h-bill THEN 
  DO:
    FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr= inp-rechnr /* malik Serverless 623 vhp.h-bill.rechnr -> inp-rechnr */
      AND vhp.h-bill-line.departement = vhp.h-bill.departement 
      AND vhp.h-bill-line.artnr NE 0 NO-LOCK, 
      FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.h-bill-line.artnr 
      AND vhp.h-artikel.departement = vhp.h-bill-line.departement 
      AND vhp.h-artikel.artart = 0 NO-LOCK: 
      total-saldo = total-saldo + vhp.h-bill-line.betrag. 
    END.
  END.
END. 
