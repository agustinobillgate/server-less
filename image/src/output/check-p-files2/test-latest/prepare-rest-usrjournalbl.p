
DEF OUTPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER long-digit AS LOGICAL.
DEF OUTPUT PARAMETER price-decimal AS INT.

FIND FIRST htparam WHERE paramnr = 110 no-lock.  /*Invoicing DATE */ 
from-date = htparam.fdate. 
to-date = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 
 
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 
