
DEF OUTPUT PARAMETER order-date AS DATE.
DEF OUTPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER enforce-rflag AS LOGICAL.

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
order-date = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 222 NO-LOCK. 
enforce-rflag = flogical. 
 
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
billdate = htparam.fdate.
