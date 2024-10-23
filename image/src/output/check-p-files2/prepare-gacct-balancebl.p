
DEF OUTPUT PARAMETER heute          AS DATE.
DEF OUTPUT PARAMETER billdate       AS DATE.
DEF OUTPUT PARAMETER long-digit     AS LOGICAL.
DEF OUTPUT PARAMETER price-decimal  AS INT.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK. 
ASSIGN
  heute    = htparam.fdate 
  billdate = htparam.fdate
. 
 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 
 
FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 
