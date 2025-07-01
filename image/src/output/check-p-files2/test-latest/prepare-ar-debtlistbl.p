DEF OUTPUT PARAMETER from-date AS DATE      NO-UNDO.
DEF OUTPUT PARAMETER to-date   AS DATE      NO-UNDO.
DEF OUTPUT PARAMETER from-art  AS INTEGER   NO-UNDO INIT 999999.
DEF OUTPUT PARAMETER to-art    AS INTEGER   NO-UNDO INIT 0.
DEF OUTPUT PARAMETER from-bez  AS CHAR      NO-UNDO.
DEF OUTPUT PARAMETER to-bez    AS CHAR      NO-UNDO.

FIND FIRST htparam WHERE paramnr = 975 NO-LOCK. 
IF htparam.finteger GT 2 THEN /* FO license actice */ 
DO: 
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  to-date = htparam.fdate. 
END. 
ELSE to-date = TODAY. 
from-date = DATE(MONTH(to-date), 1, YEAR(to-date)). 
 
FOR EACH artikel WHERE artikel.departement = 0 
     AND (artikel.artart = 2 OR artikel.artart = 7) 
     AND artikel.activeflag = YES NO-LOCK: 
  IF from-art GT artikel.artnr THEN 
  DO: 
    from-art = artikel.artnr. 
    from-bez = artikel.bezeich. 
  END. 
  IF to-art LT artikel.artnr THEN 
  DO: 
    to-art = artikel.artnr. 
    to-bez = artikel.bezeich. 
  END. 
END. 
