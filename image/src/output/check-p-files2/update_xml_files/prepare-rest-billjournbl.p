DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.

DEF OUTPUT PARAMETER from-date      AS DATE.
DEF OUTPUT PARAMETER to-date        AS DATE.
DEF OUTPUT PARAMETER price-decimal  AS INT.
DEF OUTPUT PARAMETER min-dept       AS INT INITIAL 99.
DEF OUTPUT PARAMETER max-dept       AS INT INITIAL 0.
DEF OUTPUT PARAMETER from-art       AS INT.
DEF OUTPUT PARAMETER to-art         AS INT.
DEF OUTPUT PARAMETER from-dept      AS INT.
DEF OUTPUT PARAMETER to-dept        AS INT.
DEF OUTPUT PARAMETER depname1       AS CHAR.
DEF OUTPUT PARAMETER depname2       AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

FIND FIRST hoteldpt WHERE hoteldpt.num GT 0 NO-LOCK NO-ERROR.
IF NOT AVAILABLE hoteldpt THEN RETURN NO-APPLY.

FIND FIRST htparam WHERE paramnr = 110 no-lock.  /*Invoicing DATE */ 
from-date = htparam.fdate. 
to-date = htparam.fdate. 

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 

min-dept = 999.
max-dept = 1.
FOR EACH hoteldpt WHERE hoteldpt.num GE 1 NO-LOCK BY hoteldpt.num: 
  IF min-dept GT hoteldpt.num THEN min-dept = hoteldpt.num.
  IF max-dept LT hoteldpt.num THEN max-dept = hoteldpt.num. 
END.

from-art = 0. 
to-art = 99999. 

from-dept = min-dept. 
to-dept = max-dept. 
 
FIND FIRST hoteldpt WHERE hoteldpt.num = from-dept NO-LOCK. 
depname1 = hoteldpt.depart. 
FIND FIRST hoteldpt WHERE hoteldpt.num = to-dept NO-LOCK. 
depname2 = hoteldpt.depart.

FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.
