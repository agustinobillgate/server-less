DEF TEMP-TABLE s-list 
    FIELD datum       LIKE umsatz.datum 
    FIELD departement LIKE artikel.departement COLUMN-LABEL "Dept" 
    FIELD artnr       LIKE artikel.artnr 
    FIELD artart      LIKE artikel.artart 
    FIELD bezeich     LIKE artikel.bezeich FORMAT "x(100)"
    FIELD betrag      LIKE umsatz.betrag COLUMN-LABEL "Gros Amount" 
    FIELD service     LIKE umsatz.betrag COLUMN-LABEL "Serv Charge" 
    FIELD vat         LIKE umsatz.betrag COLUMN-LABEL "VAT" 
    FIELD nett        LIKE umsatz.betrag COLUMN-LABEL "Nett Amount". 

DEF TEMP-TABLE t-gl-acct LIKE gl-acct.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER      NO-UNDO.
DEF INPUT  PARAMETER fibu           AS CHAR.
DEF INPUT  PARAMETER bemerk         AS CHAR.
DEF INPUT  PARAMETER from-date      AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-gl-acct.
DEF OUTPUT PARAMETER TABLE FOR s-list.

DEFINE VARIABLE artnr           AS INTEGER. 
DEFINE VARIABLE dept            AS INTEGER. 

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-detailFO".

FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibu NO-LOCK. 
CREATE t-gl-acct.
BUFFER-COPY gl-acct TO t-gl-acct.

RUN disp-it.


PROCEDURE disp-it: 
  DEFINE VARIABLE serv          AS DECIMAL. 
  DEFINE VARIABLE vat           AS DECIMAL. 
  DEFINE VARIABLE vat2          AS DECIMAL NO-UNDO.
  DEFINE VARIABLE wert          AS DECIMAL. 
  DEFINE VARIABLE fact          AS DECIMAL. 
  DEFINE VARIABLE serv-vat      AS LOGICAL. 
  DEFINE VARIABLE price-decimal AS INTEGER. 
 
  dept = INTEGER(ENTRY(3, bemerk, ";")). 
  artnr  = INTEGER(ENTRY(4, bemerk, ";")). 

  FIND FIRST artikel WHERE artikel.artnr = artnr AND artikel.departement = dept 
     NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE artikel THEN RETURN. 
 
  FIND FIRST umsatz WHERE umsatz.artnr = artikel.artnr 
    AND umsatz.departement = artikel.departement 
    AND umsatz.datum = from-date NO-LOCK NO-ERROR. 
 
    IF NOT AVAILABLE umsatz THEN RETURN. 
 
  IF artikel.artart = 5 THEN
  DO:
    FIND FIRST billjournal WHERE billjournal.artnr = artnr
      AND billjournal.departement = dept AND billjournal.bill-datum = from-date
      AND billjournal.anzahl NE 0 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE billjournal THEN LEAVE.
    RUN disp-deposit.
    RETURN.
  END.
 
  FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
  price-decimal = htparam.finteger.   /* non-digit OR digit version */ 
 
  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-vat = htparam.flogical. 
/* 
  serv = 0. 
  vat = 0. 
  RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service-code, 
             artikel.mwst-code, OUTPUT serv, OUTPUT vat).
  fact = 1.00 + serv + vat. 
*/
/* SY AUG 13 2017 */
    RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
        umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
    ASSIGN vat = vat + vat2.

  wert = umsatz.betrag / fact. 
 
  CREATE s-list. 
  ASSIGN 
    s-list.artnr       = artikel.artnr 
    s-list.departement = artikel.departement 
    s-list.artart      = artikel.artart 
    s-list.bezeich     = artikel.bezeich 
    s-list.datum       = umsatz.datum 
    s-list.betrag      = umsatz.betrag 
    s-list.service     = ROUND(wert * serv, price-decimal) 
    s-list.vat         = ROUND(wert * vat, price-decimal) 
    s-list.nett        = umsatz.betrag - s-list.service - s-list.vat. 
END. 


PROCEDURE disp-deposit: 
  DEFINE VARIABLE serv          AS DECIMAL NO-UNDO INIT 0. 
  DEFINE VARIABLE vat           AS DECIMAL NO-UNDO INIT 0. 
  DEFINE VARIABLE vat2          AS DECIMAL NO-UNDO INIT 0.
  DEFINE VARIABLE wert          AS DECIMAL. 
  DEFINE VARIABLE fact          AS DECIMAL NO-UNDO INIT 1. 
  DEFINE VARIABLE serv-vat      AS LOGICAL. 
  DEFINE VARIABLE price-decimal AS INTEGER. 
  DEFINE VARIABLE n             AS INTEGER.
  DEFINE VARIABLE m             AS INTEGER INITIAL 0.
  DEFINE VARIABLE resnr         AS INTEGER INITIAL 0.
  DEFINE VARIABLE s             AS CHAR.
 
  FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
  price-decimal = htparam.finteger.   /* non-digit OR digit version */ 
 
  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-vat = htparam.flogical. 
 
  FOR EACH billjournal WHERE billjournal.artnr = artnr
    AND billjournal.departement = dept AND billjournal.bill-datum = from-date
    AND billjournal.anzahl NE 0 NO-LOCK BY billjournal.zeit:
/*
    serv = 0. 
    vat = 0. 
    RUN calc-servvat.p(billjournal.departement, billjournal.artnr, billjournal.bill-datum, artikel.service-code, 
             artikel.mwst-code, OUTPUT serv, OUTPUT vat).
    fact = 1.00 + serv + vat. 
*/
/* not relevant for deposit article 
/* SY AUG 13 2017 */
    RUN calc-servTaxesbl.p(2, billjournal.artnr, billjournal.departement,
        billjournal.bill-datum, OUTPUT serv, OUTPUT vat, 
        OUTPUT vat2, OUTPUT fact).
    ASSIGN vat = vat + vat2.
*/
    wert = billjournal.betrag / fact. 
    CREATE s-list. 
    ASSIGN 
      s-list.artnr       = artikel.artnr 
      s-list.departement = artikel.departement 
      s-list.artart      = artikel.artart 
      s-list.bezeich     = billjournal.bezeich 
      s-list.datum       = billjournal.bill-datum 
      s-list.betrag      = billjournal.betrag 
      s-list.service     = ROUND(wert * serv, price-decimal) 
      s-list.vat         = ROUND(wert * vat, price-decimal) 
      s-list.nett        = billjournal.betrag - s-list.service - s-list.vat
    . 
    IF billjournal.rechnr NE 0 THEN 
    DO:
      s-list.bezeich = s-list.bezeich + "; " + translateExtended("BillNo",lvCAREA,"") 
        + " " + STRING(billjournal.rechnr).
      FIND FIRST bill WHERE bill.rechnr = billjournal.rechnr
        NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN 
        s-list.bezeich = s-list.bezeich + "; " + bill.NAME.
      ELSE
      DO:
        FIND FIRST billhis WHERE billhis.rechnr = billjournal.rechnr
          NO-LOCK.
        IF AVAILABLE billhis THEN
          s-list.bezeich = s-list.bezeich + "; " + billhis.NAME.
      END.
    END.
    ELSE IF billjournal.bezeich MATCHES ("*#*") THEN
    DO:
      s = billjournal.bezeich.
      m = 0.
      DO  n = 1 TO LENGTH(s):
        IF SUBSTR(s,n,1) = "#" THEN
        DO:
          m = n.
          s = SUBSTR(s, m).
          LEAVE.
        END.
      END.
      IF m > 0 THEN resnr = INTEGER(SUBSTR(ENTRY(1, s, " "),2)) NO-ERROR.
      IF resnr > 0 THEN
      DO:
        FIND FIRST reservation WHERE reservation.resnr = resnr 
          NO-LOCK NO-ERROR.
        IF AVAILABLE reservation THEN
          s-list.bezeich = s-list.bezeich + "; " + reservation.NAME.
      END.
    END.
  END.
END. 
