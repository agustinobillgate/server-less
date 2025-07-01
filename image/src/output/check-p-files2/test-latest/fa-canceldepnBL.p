
DEF INPUT  PARAMETER datum AS DATE.
DEF OUTPUT PARAMETER do-it AS LOGICAL INIT NO.

DEFINE VARIABLE last-date     AS DATE    INITIAL ? NO-UNDO.
DEFINE VARIABLE depn-value    AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE old-book-wert AS DECIMAL. 

DEFINE BUFFER fabuff FOR fa-artikel.
DEFINE BUFFER queasy-buff FOR queasy.

FOR EACH fa-artikel WHERE fa-artikel.last-depn  = datum AND 
    fa-artikel.loeschflag = 0  NO-LOCK,
    FIRST mathis WHERE mathis.nr = fa-artikel.nr NO-LOCK BY
    mathis.NAME :

    last-date = DATE(month(datum), 1, year(datum)) - 1.

    depn-value = 0.
    IF fa-artikel.anz-depn GE 1 THEN
        RUN get-depn-value. 
    
    IF old-book-wert NE 0 THEN
    DO:
        do-it = YES.

        FIND FIRST fabuff WHERE RECID(fabuff) = RECID(fa-artikel) EXCLUSIVE-LOCK.
        IF fa-artikel.anz-depn = 1 THEN
            ASSIGN
                fabuff.anz-depn = 0
                fabuff.depn-wert = 0
                fabuff.next-depn = datum
                fabuff.last-depn = ?
                fabuff.book-wert = fabuff.warenwert.
        ELSE
            ASSIGN 
            fabuff.depn-wert = fabuff.warenwert - old-book-wert
            fabuff.book-wert = old-book-wert
            fabuff.anz-depn  = fabuff.anz-depn - 1
            fabuff.last-depn = last-date
            fabuff.next-depn = datum.

        IF fabuff.first-depn = datum THEN
            fabuff.first-depn = ?.
        FIND CURRENT fabuff NO-LOCK.
    END.            
END.


IF do-it THEN
DO:
  FIND FIRST htparam WHERE paramnr = 881 EXCLUSIVE-LOCK.
  ASSIGN htparam.fdate = last-date.
  FIND CURRENT htparam NO-LOCK.

  /* Malik 4E136B -> delete FA history */
  FIND FIRST queasy WHERE queasy.key = 348 AND queasy.date1 = datum NO-LOCK NO-ERROR.
  IF AVAILABLE queasy THEN
  DO:
      FOR EACH queasy-buff WHERE queasy-buff.key = 348 AND queasy-buff.date1 = datum:
        DELETE queasy-buff.
      END.
  END.
  /* END Malik  */
END.

PROCEDURE get-depn-value: 
  DEFINE VARIABLE tot-anz AS INTEGER. 
  DEFINE VARIABLE num AS INTEGER. 
      
  old-book-wert = 0.
  FIND FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.katnr NO-LOCK. 
  IF fa-kateg.methode = 0 THEN 
  DO: 
      
    /* 
        depn-value = fa-artikel.warenwert * fa-kateg.rate / 100 
          / fa-kateg.nutzjahr / 12. 
        IF depn-value GT fa-artikel.book-wert THEN 
          depn-value = fa-artikel.book-wert. 
        ELSE IF (fa-artikel.book-wert - depn-value) LT (depn-value * 0.5) THEN 
          depn-value = fa-artikel.book-wert. 
    */ 
            
    old-book-wert = fa-artikel.warenwert.
    DO num = 1 TO (fa-artikel.anz-depn - 1):
        tot-anz = fa-kateg.nutzjahr * 12 - (num - 1). 
        old-book-wert = old-book-wert - (old-book-wert / tot-anz).
    END.    
    /*tot-anz = fa-kateg.nutzjahr * 12 - fa-artikel.anz-depn - 1. 
    IF tot-anz GT 0 THEN depn-value = old-book-wert / tot-anz. 
    ELSE depn-value = 0. */
  END. 
END. 

