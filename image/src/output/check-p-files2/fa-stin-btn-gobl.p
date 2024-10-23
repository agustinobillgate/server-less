DEFINE TEMP-TABLE op-list LIKE fa-op
    FIELD NAME     AS CHAR
    FIELD location AS CHAR. 

DEFINE INPUT PARAMETER TABLE FOR op-list.
DEFINE INPUT PARAMETER billdate  AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER user-init AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER lscheinnr AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER lief-nr   AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER created  AS LOGICAL NO-UNDO.

DEFINE VARIABLE s-artnr     AS INTEGER NO-UNDO.
DEFINE VARIABLE qty         AS DECIMAL NO-UNDO. 
DEFINE VARIABLE price       AS DECIMAL NO-UNDO. 
DEFINE VARIABLE amount      AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t-amount    AS DECIMAL NO-UNDO. 


FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK NO-ERROR.

FOR EACH op-list: 
    s-artnr     = op-list.nr. 
    qty         = op-list.anzahl. 
    price       = op-list.warenwert / qty. 
    amount      = op-list.warenwert. 
    t-amount    = t-amount + op-list.warenwert. 
    RUN create-fa-op. 
    created = YES. 
END. 

IF lief-nr NE 0 AND t-amount NE 0 THEN RUN create-ap. 

PROCEDURE create-fa-op: 
  DEFINE VARIABLE next-date AS DATE. 
  DEFINE VARIABLE next-mon AS INTEGER. 
  DEFINE VARIABLE next-yr AS INTEGER. 
  DO transaction: 
    FIND FIRST mathis WHERE mathis.nr = s-artnr EXCLUSIVE-LOCK. 
    mathis.price = price. 
    mathis.supplier = l-lieferant.firma. 
    mathis.datum = billdate. 
    FIND CURRENT mathis NO-LOCK. 
    


    FIND FIRST fa-artikel WHERE fa-artikel.nr = s-artnr EXCLUSIVE-LOCK. 
    fa-artikel.lief-nr = l-lieferant.lief-nr. 
    fa-artikel.posted = YES. 
    fa-artikel.anzahl = qty. 
    fa-artikel.warenwert = amount. 
    fa-artikel.book-wert = amount. 

    /* Malik 
      FIND FIRST queasy WHERE queasy.key = 314 AND queasy.number1 = s-artnr NO-LOCK NO-ERROR.

      IF AVAILABLE queasy AND queasy.date1 NE ? THEN
      DO:
        next-mon = month(queasy.date1) + 1. 
        next-yr = year(queasy.date1). 
        IF next-mon = 13 THEN 
        DO: 
          next-mon = 1. 
          next-yr = next-yr + 1. 
        END. 
        next-date = DATE(next-mon, 1, next-yr) - 1. 
      
        FIND FIRST htparam WHERE paramnr = 880 NO-LOCK. 
        IF day(queasy.date1) LE htparam.finteger THEN fa-artikel.next-depn = next-date. 
        ELSE 
        DO: 
            /*
            next-mon = next-mon + 1. 
            IF next-mon = 13 THEN 
            DO: 
              next-mon = 1. 
              next-yr = next-yr + 1. 
            END. 
            next-date = DATE(next-mon, 1, next-yr) - 1. 
            fa-artikel.next-depn = next-date. 
            */
            fa-artikel.next-depn = next-date.
        END. 

        IF queasy.date1 LT TODAY THEN 
        DO:
          next-mon = month(TODAY) + 1. 
          next-yr = year(TODAY). 
          IF next-mon = 13 THEN 
          DO: 
            next-mon = 1. 
            next-yr = next-yr + 1. 
          END.    

          next-date = DATE(next-mon, 1, next-yr) - 1. 
          fa-artikel.next-depn = next-date.

          queasy.date1 = DATE(month(TODAY), day(queasy.date1), year(TODAY)).
        END.      
      END. 
      ELSE
      DO:
        next-mon = month(billdate) + 1. 
        next-yr = year(billdate). 
        IF next-mon = 13 THEN 
        DO: 
          next-mon = 1. 
          next-yr = next-yr + 1. 
        END. 
        next-date = DATE(next-mon, 1, next-yr) - 1. 
    
        FIND FIRST htparam WHERE paramnr = 880 NO-LOCK. 
        IF day(billdate) LE htparam.finteger THEN fa-artikel.next-depn = next-date. 
        ELSE 
        DO: 
          next-mon = next-mon + 1. 
          IF next-mon = 13 THEN 
          DO: 
            next-mon = 1. 
            next-yr = next-yr + 1. 
          END. 
          next-date = DATE(next-mon, 1, next-yr) - 1. 
          fa-artikel.next-depn = next-date. 
        END. 
      END.
    */
  /*    
    next-mon = month(billdate) + 1. 
    next-yr = year(billdate). 
    IF next-mon = 13 THEN 
    DO: 
      next-mon = 1. 
      next-yr = next-yr + 1. 
    END. 
    next-date = DATE(next-mon, 1, next-yr) - 1. 
 
    FIND FIRST htparam WHERE paramnr = 880 NO-LOCK. 
    IF day(billdate) LE htparam.finteger THEN fa-artikel.next-depn = next-date. 
    ELSE 
    DO: 
      next-mon = next-mon + 1. 
      IF next-mon = 13 THEN 
      DO: 
        next-mon = 1. 
        next-yr = next-yr + 1. 
      END. 
      next-date = DATE(next-mon, 1, next-yr) - 1. 
      fa-artikel.next-depn = next-date. 
    END. 
  */  
    FIND FIRST queasy WHERE queasy.key = 314 AND queasy.number1 = s-artnr NO-ERROR.
    IF AVAILABLE queasy AND queasy.date1 NE ? THEN
    DO:
        next-mon = month(queasy.date1) + 1. 
        next-yr = year(queasy.date1). 
        IF next-mon = 13 THEN 
        DO: 
            next-mon = 1. 
            next-yr = next-yr + 1. 
        END.    

        next-date = DATE(next-mon, 1, next-yr) - 1. 

        FIND FIRST htparam WHERE paramnr = 880 NO-LOCK. 
        IF day(queasy.date1) LE htparam.finteger THEN fa-artikel.next-depn = next-date. 
        ELSE 
        DO: 
            fa-artikel.next-depn = next-date. 
        END. 

        IF queasy.date1 LT TODAY THEN 
        DO:
            next-mon = month(TODAY) + 1. 
            next-yr = year(TODAY). 
            IF next-mon = 13 THEN 
            DO: 
                next-mon = 1. 
                next-yr = next-yr + 1. 
            END.    

            next-date = DATE(next-mon, 1, next-yr) - 1. 
            fa-artikel.next-depn = next-date.

            queasy.date1 = DATE(month(TODAY), day(queasy.date1), year(TODAY)).

        END.

    END.
    ELSE
    DO:
        next-mon = month(billdate) + 1. 
        next-yr = year(billdate). 
        IF next-mon = 13 THEN 
        DO: 
            next-mon = 1. 
            next-yr = next-yr + 1. 
        END. 

        next-date = DATE(next-mon, 1, next-yr) - 1. 

        FIND FIRST htparam WHERE paramnr = 880 NO-LOCK. 
        IF day(billdate) LE htparam.finteger THEN fa-artikel.next-depn = next-date. 
        ELSE 
        DO: 
            next-mon = next-mon + 1. 
            IF next-mon = 13 THEN 
            DO: 
                next-mon = 1. 
                next-yr = next-yr + 1. 
            END. 

            next-date = DATE(next-mon, 1, next-yr) - 1. 
            fa-artikel.next-depn = next-date. 
        END. 
    END.    
    
    /* FIND CURRENT queasy NO-LOCK. */
    FIND CURRENT fa-artikel NO-LOCK. 
 
    create fa-op.
    fa-op.nr = mathis.nr.
    fa-op.opart = 1.
    fa-op.datum = billdate.
    fa-op.zeit = TIME.
    fa-op.anzahl = qty.
    fa-op.einzelpreis = price.
    fa-op.warenwert = amount.
    fa-op.id = user-init.
    fa-op.lscheinnr = lscheinnr.
    fa-op.docu-nr = lscheinnr.
    fa-op.lief-nr = l-lieferant.lief-nr.
    release fa-op.
  END. 
END. 


PROCEDURE create-ap: 
  DEFINE buffer l-op1 FOR l-op.
  create l-kredit. 
  l-kredit.name         = lscheinnr. 
  l-kredit.lief-nr      = lief-nr. 
  l-kredit.lscheinnr    = lscheinnr. 
  l-kredit.rgdatum      = billdate. 
  l-kredit.datum        = ?. 
  l-kredit.saldo        = t-amount. 
  l-kredit.ziel         = 30. 
  l-kredit.netto        = t-amount. 
  l-kredit.bediener-nr  = bediener.nr.
  l-kredit.betriebsnr   = 2. 
 
  create ap-journal. 
  ap-journal.lief-nr = lief-nr. 
  ap-journal.docu-nr = lscheinnr. 
  ap-journal.lscheinnr = lscheinnr. 
  ap-journal.rgdatum = billdate. 
  ap-journal.saldo = t-amount. 
  ap-journal.netto = t-amount. 
 
  ap-journal.userinit = bediener.userinit. 
  ap-journal.zeit = time. 
 
END. 
 
