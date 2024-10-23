
DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER close-date AS DATE.
DEF OUTPUT PARAMETER curr-close-year AS INT.
DEF OUTPUT PARAMETER p-418 AS CHAR.

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 

FIND FIRST htparam WHERE htparam.paramnr = 597 NO-LOCK.
ASSIGN close-date = htparam.fdate.

FIND FIRST htparam WHERE htparam.paramnr = 795 NO-LOCK. /* last close year */
ASSIGN curr-close-year = YEAR(htparam.fdate) + 1.

FIND FIRST htparam WHERE htparam.paramnr = 418 NO-LOCK.
p-418 = htparam.fchar.
