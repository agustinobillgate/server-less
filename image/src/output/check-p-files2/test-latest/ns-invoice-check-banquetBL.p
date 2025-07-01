DEFINE INPUT  PARAMETER bill-rechnr AS INT.

DEFINE OUTPUT PARAMETER answer AS LOGICAL INITIAL YES. 

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK. 
FIND FIRST bk-veran WHERE bk-veran.rechnr = bill-rechnr NO-LOCK NO-ERROR. 
IF AVAILABLE bk-veran AND bk-veran.activeflag = 0 THEN 
DO: 
    FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr 
      AND bk-reser.datum GT htparam.fdate 
      AND bk-reser.resstatus LE 3 NO-LOCK NO-ERROR. 
    IF AVAILABLE bk-reser THEN 
    DO: 
      answer = NO. 
      RETURN. 
    END. 
 
    FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr 
      AND bk-reser.datum = htparam.fdate AND bk-reser.resstatus = 1 
      AND (bk-reser.bis-i * 1800) GT TIME NO-LOCK NO-ERROR. 
    IF AVAILABLE bk-reser THEN 
    DO: 
      answer = NO. 
      RETURN. 
    END. 
 
    /*FIND FIRST bk-rart WHERE bk-rart.veran-nr = bk-veran.veran-nr 
      AND bk-rart.preis > 0 AND bk-rart.anzahl NE 0 
      AND bk-rart.fakturiert = 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE bk-rart THEN RUN ba-NPartikel.p(bk-veran.veran-nr). */
END. 

