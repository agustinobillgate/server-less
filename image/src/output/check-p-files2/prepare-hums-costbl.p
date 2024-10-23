
DEF OUTPUT PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER double-currency AS LOGICAL.
DEF OUTPUT PARAMETER foreign-nr AS INT INIT 0.
DEF OUTPUT PARAMETER exchg-rate AS DECIMAL INIT 1.

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
to-date = htparam.fdate.         /* Rulita 211024 | Fixing for serverless */
from-date = DATE(month(to-date), 1, year(to-date)). 

FIND FIRST htparam WHERE paramnr = 240 no-lock. /* double currency */ 
double-currency = htparam.flogical. 
 
FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
IF htparam.fchar NE "" THEN 
DO: 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN 
  DO: 
    foreign-nr = waehrung.waehrungsnr. 
    exchg-rate = waehrung.ankauf / waehrung.einheit. 
  END. 
END. 
