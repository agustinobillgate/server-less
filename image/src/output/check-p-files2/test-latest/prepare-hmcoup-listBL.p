
DEF TEMP-TABLE t-hoteldpt
    FIELD num    LIKE hoteldpt.num
    FIELD depart LIKE hoteldpt.depart.

DEF OUTPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER from-art AS INT INIT 0.
DEF OUTPUT PARAMETER to-art AS INT INIT 99999.
DEF OUTPUT PARAMETER from-dept AS INT INIT 1.
DEF OUTPUT PARAMETER to-dept AS INT INIT 99.
DEF OUTPUT PARAMETER depname1 AS CHAR.
DEF OUTPUT PARAMETER depname2 AS CHAR.
DEF OUTPUT PARAMETER double-currency AS LOGICAL INITIAL NO.
DEF OUTPUT PARAMETER foreign-nr AS INTEGER INITIAL 0.
DEF OUTPUT PARAMETER exchg-rate AS DECIMAL INITIAL 1.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

DEFINE VARIABLE min-dept AS INTEGER INITIAL 99. 
DEFINE VARIABLE max-dept AS INTEGER INITIAL 0. 
DEFINE VARIABLE min-art  AS INTEGER INITIAL 9999. 
DEFINE VARIABLE max-art  AS INTEGER INITIAL 0. 
FIND FIRST htparam WHERE paramnr = 110 no-lock.  /*Invoicing DATE */ 
billdate = htparam.fdate. 
from-date = htparam.fdate - 1. 
to-date = htparam.fdate - 1. 

/*MT 14/01/15
min-dept = 1. 
FOR EACH hoteldpt WHERE hoteldpt.num GE 1 NO-LOCK BY hoteldpt.num: 
    IF max-dept LT hoteldpt.num THEN max-dept = hoteldpt.num. 
END.
*/ 
min-art = 0.    /* e.g. room transfer */ 
max-art = 99999. 
from-art = min-art. 
to-art = max-art. 
from-dept = min-dept. 
to-dept = max-dept. 
 
FIND FIRST hoteldpt WHERE hoteldpt.num = from-dept NO-LOCK NO-ERROR. 
IF AVAILABLE hoteldpt THEN depname1 = hoteldpt.depart. 
FIND FIRST hoteldpt WHERE hoteldpt.num = to-dept NO-LOCK NO-ERROR. 
IF AVAILABLE hoteldpt THEN depname2 = hoteldpt.depart. 
 
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

FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    ASSIGN
    t-hoteldpt.num    = hoteldpt.num
    t-hoteldpt.depart = hoteldpt.depart.
END.
