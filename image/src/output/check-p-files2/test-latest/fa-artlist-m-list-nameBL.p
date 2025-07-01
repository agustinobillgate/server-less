
DEF BUFFER mathis1 FOR mathis.

DEF INPUT  PARAMETER m-list-name   AS CHAR.
DEF OUTPUT PARAMETER mathis1-model AS CHAR.
DEF OUTPUT PARAMETER avail-mathis1 AS LOGICAL INIT NO.

FIND FIRST mathis1 WHERE mathis1.name = m-list-name NO-LOCK NO-ERROR. 
IF AVAILABLE mathis1 THEN 
DO:
    avail-mathis1 = YES.
    mathis1-model = mathis1.model.
END.
