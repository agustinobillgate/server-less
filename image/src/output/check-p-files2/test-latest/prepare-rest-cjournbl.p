DEF TEMP-TABLE t-hoteldpt  LIKE hoteldpt.

DEF OUTPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER long-digit AS LOGICAL.
DEF OUTPUT PARAMETER depname1 AS CHAR.
DEF OUTPUT PARAMETER depname2 AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

FIND FIRST htparam WHERE paramnr = 110 no-lock.  /*Invoicing DATE */ 
from-date = htparam.fdate. 
to-date = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical.

FIND FIRST hoteldpt WHERE hoteldpt.num = 1 NO-LOCK NO-ERROR. 
IF AVAILABLE hoteldpt THEN 
DO: 
  depname1 = hoteldpt.depart. 
  depname2 = hoteldpt.depart. 
END. 

FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.
