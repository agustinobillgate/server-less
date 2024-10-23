
DEF INPUT  PARAMETER m-list-name        AS CHAR.
DEF OUTPUT PARAMETER mathis1-model      AS CHAR.
DEF OUTPUT PARAMETER mathis1-supplier   AS CHAR.
DEF OUTPUT PARAMETER do-it              AS LOGICAL INIT NO.

DEF BUFFER mathis1 FOR mathis.

FIND FIRST mathis1 WHERE mathis1.name = m-list-name NO-LOCK NO-ERROR. 
IF AVAILABLE mathis1 THEN 
DO: 
    FIND FIRST fa-artikel WHERE fa-artikel.nr = mathis1.nr NO-LOCK.
    IF fa-artikel.loeschflag = 0 THEN
    DO:
        mathis1-model = mathis1.model.
        mathis1-supplier = mathis1.supplier.
        do-it = YES.
    END.
END. 
