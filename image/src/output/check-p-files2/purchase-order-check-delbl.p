
DEF INPUT  PARAMETER q2-list-docu-nr AS CHAR.
DEF OUTPUT PARAMETER err-code        AS INT INIT 0.

DEFINE buffer l-order1 FOR l-order.
DEFINE VARIABLE found AS LOGICAL INITIAL NO.

DO: 
    FIND FIRST l-order1 WHERE l-order1.docu-nr = q2-list-docu-nr
      AND l-order1.pos GT 0 AND l-order1.loeschflag = 0 
      AND (l-order1.anzahl NE l-order1.geliefert) NO-LOCK NO-ERROR. 
    IF AVAILABLE l-order1 THEN found = YES. 
    ELSE 
    DO WHILE (NOT found) AND  AVAILABLE l-order1: 
      FIND NEXT l-order1 WHERE l-order1.docu-nr = q2-list-docu-nr 
        AND l-order1.pos GT 0 AND l-order1.loeschflag = 0 
        AND (l-order1.anzahl NE l-order1.geliefert) NO-LOCK NO-ERROR. 
      IF AVAILABLE l-order1 THEN found = YES. 
    END. 
    IF NOT found THEN err-code = 1.
    ELSE err-code = 2.
END.
