
DEF INPUT  PARAMETER fa-art-katnr       AS INT.
DEF OUTPUT PARAMETER fa-kateg-nutzjahr  LIKE fa-kateg.nutzjahr.
DEF OUTPUT PARAMETER avail-fa-kateg     AS LOGICAL INIT NO.

FIND FIRST fa-kateg WHERE fa-kateg.katnr = fa-art-katnr 
  NO-LOCK NO-ERROR. 
IF AVAILABLE fa-kateg AND fa-kateg.methode = 0 THEN 
    ASSIGN avail-fa-kateg = YES
           fa-kateg-nutzjahr = fa-kateg.nutzjahr.
