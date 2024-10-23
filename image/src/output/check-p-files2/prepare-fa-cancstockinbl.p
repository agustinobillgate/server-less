
DEF OUTPUT PARAMETER price-decimal  AS INT.
DEF OUTPUT PARAMETER from-date      AS DATE.
DEF OUTPUT PARAMETER to-date        AS DATE.
DEF OUTPUT PARAMETER beg-date       AS DATE.

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 

FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
from-date = htparam.fdate. 
to-date = from-date.

FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
beg-date = DATE(month(fdate), 1, year(fdate)). 
