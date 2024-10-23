
DEF INPUT  PARAMETER pay-list-s-recid   AS INT.
DEF OUTPUT PARAMETER success-flag       AS LOGICAL INIT NO.

DEFINE VARIABLE i-counter AS INTEGER.
DEFINE VARIABLE it-exist  AS LOGICAL INITIAL NO.

DEFINE BUFFER debt FOR l-kredit.

FIND FIRST htparam WHERE paramnr = 1118 NO-LOCK.  /* LAST A/P Transfer DATE */ 

FIND FIRST debt WHERE RECID(debt) = pay-list-s-recid NO-LOCK NO-ERROR. 
IF AVAILABLE debt AND debt.rgdatum LE htparam.fdate THEN RETURN.
  
FIND FIRST l-kredit WHERE l-kredit.counter = debt.counter
    AND l-kredit.zahlkonto = 0 NO-LOCK NO-ERROR.
IF AVAILABLE l-kredit THEN
DO TRANSACTION: 
    i-counter = l-kredit.counter. 
    FIND CURRENT debt EXCLUSIVE-LOCK. 
    DELETE debt. 
    FIND CURRENT l-kredit EXCLUSIVE-LOCK. 
    l-kredit.opart = 0. 
    FIND CURRENT l-kredit NO-LOCK. 
    success-flag = YES.
    
    FIND FIRST debt WHERE debt.counter = i-counter 
        AND debt.zahlkonto GT 0 AND debt.opart = 2 NO-LOCK NO-ERROR.
    IF AVAILABLE debt THEN DO:
        FOR EACH debt WHERE debt.counter = i-counter 
          AND debt.zahlkonto GT 0 AND debt.opart = 2: 
          debt.opart = 1. 
          it-exist = YES. 
        END. 
    END.
    ELSE DO:
        FOR EACH debt WHERE debt.counter = i-counter 
          AND debt.zahlkonto GT 0 AND debt.opart = 1: 
          it-exist = YES. 

        END. 
    END.

    IF NOT it-exist THEN 
    DO: 
      FIND CURRENT l-kredit EXCLUSIVE-LOCK. 
      l-kredit.counter = 0. 
      FIND CURRENT l-kredit NO-LOCK. 
    END. 
END. 
