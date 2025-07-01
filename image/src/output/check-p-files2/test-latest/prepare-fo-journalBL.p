
DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.

DEF INPUT  PARAMETER from-dept  AS INT.
DEF INPUT  PARAMETER to-dept    AS INT.
DEF OUTPUT PARAMETER from-date  AS DATE.
DEF OUTPUT PARAMETER to-date    AS DATE.
DEF OUTPUT PARAMETER long-digit AS LOGICAL.
DEF OUTPUT PARAMETER depname1   AS CHAR.
DEF OUTPUT PARAMETER depname2   AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK NO-ERROR.  /*Invoicing DATE */ 
from-date = htparam.fdate. 
to-date = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK NO-ERROR. 
long-digit = htparam.flogical. 

FIND FIRST hoteldpt WHERE hoteldpt.num = from-dept NO-LOCK NO-ERROR. 
depname1 = hoteldpt.depart. 
FIND FIRST hoteldpt WHERE hoteldpt.num = to-dept NO-LOCK NO-ERROR. 
depname2 = hoteldpt.depart. 

FOR EACH hoteldpt NO-LOCK:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.
