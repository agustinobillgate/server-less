
DEF TEMP-TABLE t-hoteldpt
    FIELD num    LIKE hoteldpt.num
    FIELD depart LIKE hoteldpt.depart.

DEF INPUT PARAMETER min-dept AS INT.
DEF INPUT PARAMETER max-dept AS INT.
DEF OUTPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER long-digit AS LOGICAL.
DEF OUTPUT PARAMETER min-art AS INT INIT 9999.
DEF OUTPUT PARAMETER max-art AS INT INIT 0.
DEF OUTPUT PARAMETER from-art AS INT INIT 0.
DEF OUTPUT PARAMETER to-art AS INT INIT 9999.
DEF OUTPUT PARAMETER from-dept AS INT INIT 1.
DEF OUTPUT PARAMETER to-dept AS INT INIT 99.
DEF OUTPUT PARAMETER depname1 AS CHAR.
DEF OUTPUT PARAMETER depname2 AS CHAR.
DEF OUTPUT PARAMETER double-currency AS LOGICAL INITIAL NO.
DEF OUTPUT PARAMETER exchg-rate AS DECIMAL INITIAL 1.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

FIND FIRST htparam WHERE paramnr = 110 no-lock.  /* Invoicing DATE */ 
billdate = htparam.fdate. 
from-date = htparam.fdate - 1. 
to-date = htparam.fdate - 1. 
 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

RUN select-dept. 
min-art = 0.    /* e.g. room transfer */ 
max-art = 99999. 
 
from-art = min-art. 
to-art = max-art. 
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
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
  ELSE exchg-rate = 1. 
END. 

FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    ASSIGN
    t-hoteldpt.num    = hoteldpt.num
    t-hoteldpt.depart = hoteldpt.depart.
END.

PROCEDURE select-dept: 
DEFINE VARIABLE ldry AS INTEGER. 
DEFINE VARIABLE dstore AS INTEGER. 
  FIND FIRST htparam WHERE paramnr = 1081 NO-LOCK. 
  ldry = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 1082 NO-LOCK. 
  dstore = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  min-dept = 1. 
  FOR EACH hoteldpt WHERE hoteldpt.num GE 1 AND hoteldpt.num NE ldry 
    AND hoteldpt.num NE dstore NO-LOCK BY hoteldpt.num: 
    IF max-dept LT hoteldpt.num THEN max-dept = hoteldpt.num. 
  END. 
END. 

