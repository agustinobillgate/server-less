
DEF OUTPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER to-date   AS DATE.

FIND FIRST htparam WHERE paramnr = 110 no-lock.  /*Invoicing DATE */ 
from-date = htparam.fdate. 
to-date = htparam.fdate. 
