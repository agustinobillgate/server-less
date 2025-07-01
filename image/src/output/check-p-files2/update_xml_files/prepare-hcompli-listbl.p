DEF TEMP-TABLE t-hoteldpt
    FIELD num       LIKE hoteldpt.num
    FIELD depart    LIKE hoteldpt.depart.

DEF OUTPUT PARAMETER from-dept AS INT INIT 1.
DEF OUTPUT PARAMETER to-dept AS INT INIT 99.
DEF OUTPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER avail-queasy AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER min-dept AS INTEGER INITIAL 99. 
DEF OUTPUT PARAMETER max-dept AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER depname1 AS CHAR.
DEF OUTPUT PARAMETER depname2 AS CHAR.
DEF OUTPUT PARAMETER double-currency AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER exchg-rate AS DECIMAL INIT 1.
DEF OUTPUT PARAMETER foreign-nr AS INT INIT 0.
DEF OUTPUT PARAMETER min-art AS INT INIT 9999.
DEF OUTPUT PARAMETER max-art AS INT INIT 0.
DEF OUTPUT PARAMETER from-art AS INT.
DEF OUTPUT PARAMETER to-art AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

DEFINE VARIABLE ldry AS INTEGER. 
DEFINE VARIABLE dstore AS INTEGER. 

FIND FIRST hoteldpt WHERE hoteldpt.num GT 0 NO-LOCK NO-ERROR.
IF NOT AVAILABLE hoteldpt THEN RETURN NO-APPLY.

FIND FIRST htparam WHERE paramnr = 110 no-lock.  /* Invoicing DATE */ 
billdate = htparam.fdate. 

RUN select-dept. 

min-art = 0.    /* e.g. room transfer */ 
max-art = 99999. 
 
from-art = min-art. 
to-art = max-art. 

FIND FIRST queasy WHERE queasy.key = 105 NO-LOCK NO-ERROR. 
IF AVAILABLE queasy THEN avail-queasy = YES.

/* SY 29/12/2014
min-dept = 99. 
FOR EACH hoteldpt WHERE hoteldpt.num GE 1 NO-LOCK BY hoteldpt.num: 
  IF min-dept GT hoteldpt.num THEN min-dept = hoteldpt.num.
  IF max-dept LT hoteldpt.num THEN max-dept = hoteldpt.num. 
END. 
*/
from-dept = min-dept. 
to-dept = max-dept. 
FIND FIRST hoteldpt WHERE hoteldpt.num = from-dept NO-LOCK. 
depname1 = hoteldpt.depart. 
FIND FIRST hoteldpt WHERE hoteldpt.num = to-dept NO-LOCK. 
depname2 = hoteldpt.depart. 

FIND FIRST htparam WHERE paramnr = 240 no-lock.  /* double currency flag */ 
IF htparam.flogical THEN 
DO: 
  double-currency = YES. 
END. 

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
IF htparam.fchar NE "" THEN 
DO: 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN 
  DO: 
    exchg-rate = waehrung.ankauf / waehrung.einheit. 
    foreign-nr = waehrung.waehrungsnr. 
  END. 
  ELSE exchg-rate = 1. 
END. 

FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    ASSIGN
        t-hoteldpt.num       = hoteldpt.num
        t-hoteldpt.depart    = hoteldpt.depart.
END.


PROCEDURE select-dept: 
  FIND FIRST htparam WHERE paramnr = 1081 NO-LOCK. 
  ldry = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 1082 NO-LOCK. 
  dstore = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  ASSIGN
      min-dept = 999
      max-dept = 1
  . 
  FOR EACH hoteldpt WHERE hoteldpt.num GE 1 AND hoteldpt.num NE ldry 
      AND hoteldpt.num NE dstore NO-LOCK BY hoteldpt.num: 
      IF min-dept GT hoteldpt.num THEN min-dept = hoteldpt.num.
      IF max-dept LT hoteldpt.num THEN max-dept = hoteldpt.num. 
  END. 
END. 
