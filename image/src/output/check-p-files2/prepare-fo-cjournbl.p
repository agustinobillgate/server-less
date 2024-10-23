
DEF INPUT PARAMETER from-dept AS INT.
DEF OUTPUT PARAMETER fdate AS DATE.
DEF OUTPUT PARAMETER long-digit AS LOGICAL.
DEF OUTPUT PARAMETER depname1 AS CHAR.
DEF OUTPUT PARAMETER depname2 AS CHAR.

FIND FIRST htparam WHERE paramnr = 110 no-lock.  /*Invoicing DATE */ 
fdate = htparam.fdate.
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 
FIND FIRST hoteldpt WHERE hoteldpt.num = from-dept NO-LOCK NO-ERROR. 
IF AVAILABLE hoteldpt THEN 
DO: 
  depname1 = hoteldpt.depart. 
  depname2 = hoteldpt.depart. 
END. 

