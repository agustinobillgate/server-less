
DEF INPUT  PARAMETER m-list-asset   AS CHAR.
DEF INPUT  PARAMETER recid-mathis   AS INT.
DEF OUTPUT PARAMETER avail-mathis1  AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER mathis1-name   AS CHAR.

DEF BUFFER mathis1 FOR mathis.

FIND FIRST mathis1 WHERE mathis1.asset = m-list-asset 
  AND RECID(mathis1) NE recid-mathis NO-LOCK NO-ERROR. 
IF AVAILABLE mathis1 THEN 
    ASSIGN avail-mathis1 = YES
           mathis1-name  = mathis1.name.
