
DEF INPUT  PARAMETER fa-art-katnr   AS CHAR.
DEF OUTPUT PARAMETER avail-fa-kateg AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER fa-kateg-rate  LIKE fa-kateg.rate.

FIND FIRST fa-kateg WHERE fa-kateg.katnr = INTEGER(fa-art-katnr)
  NO-LOCK NO-ERROR. 
IF AVAILABLE fa-kateg THEN 
    ASSIGN avail-fa-kateg = YES
           fa-kateg-rate  = fa-kateg.rate.
