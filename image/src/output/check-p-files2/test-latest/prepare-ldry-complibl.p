
DEF OUTPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER from-dept AS INT.
DEF OUTPUT PARAMETER double-currency AS LOGICAL.
DEF OUTPUT PARAMETER foreign-nr AS INT.
DEF OUTPUT PARAMETER exchg-rate AS DECIMAL.

FIND FIRST htparam WHERE paramnr = 110 no-lock.  /* Invoicing DATE */ 
billdate = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 1081 NO-LOCK. 
from-dept = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  

FIND FIRST htparam WHERE paramnr = 240 no-lock.  /* double currency flag */ 
IF htparam.flogical THEN 
DO: 
  double-currency = YES. 
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN 
  DO: 
    foreign-nr = waehrung.waehrungsnr. 
    exchg-rate = waehrung.ankauf / waehrung.einheit. 
  END. 
  ELSE exchg-rate = 1. 
END. 
 
