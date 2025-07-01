
DEF INPUT  PARAMETER billart    AS INT.
DEF INPUT  PARAMETER bil-recid  AS INT.
DEF OUTPUT PARAMETER amt        AS DECIMAL INITIAL 0           NO-UNDO.

DEFINE BUFFER bline      FOR bill-line.
DEFINE BUFFER foart      FOR artikel.
DEFINE BUFFER vatBuff    FOR artikel.

DEFINE VARIABLE serv-vat AS LOGICAL             NO-UNDO.
DEFINE VARIABLE serv     AS DECIMAL INITIAL 0   NO-UNDO.
DEFINE VARIABLE vat      AS DECIMAL INITIAL 0   NO-UNDO.
DEFINE VARIABLE vat2     AS DECIMAL INITIAL 0   NO-UNDO.
DEFINE VARIABLE fact     AS DECIMAL INITIAL 1   NO-UNDO.

FIND FIRST bill WHERE RECID(bill) = bil-recid NO-LOCK.
FIND FIRST vatBuff WHERE vatBuff.artnr = billart
      AND vatBuff.departement = 0 NO-LOCK.

FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
serv-vat = htparam.flogical. 
  
FOR EACH bline WHERE bline.rechnr = bill.rechnr NO-LOCK:
    FIND FIRST foart WHERE foart.artnr = bline.artnr 
      AND foart.departement = bline.departement NO-LOCK NO-ERROR. 
    IF AVAILABLE foart AND foart.mwst-code = vatBuff.mwst-code THEN 
    DO: 
      IF bline.orts-tax NE 0 THEN amt = amt - bline.orts-tax.
      ELSE
      DO:
/*
        FIND FIRST htparam WHERE htparam.paramnr = foart.service-code 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE htparam THEN serv = htparam.fdecimal / 100. 
        FIND FIRST htparam WHERE htparam.paramnr = foart.mwst-code NO-LOCK 
          NO-ERROR. 
        IF AVAILABLE htparam THEN 
        DO:    
          vat = htparam.fdecimal / 100. 
          IF serv-vat THEN vat = vat + vat * serv.
        END.
        ELSE vat = 0. 
*/               
/* SY AUG 13 2017 */
        RUN calc-servtaxesbl.p(1, foart.artnr, foart.departement,
            bline.bill-datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, 
            OUTPUT fact).
        ASSIGN vat = vat + vat2.
        IF vat NE 0 THEN amt = amt - bline.betrag * (1 - 1 / (1 + vat)).
      END.
    END.
END.
