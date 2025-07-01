
DEF OUTPUT PARAMETER bill-date AS DATE.
DEF OUTPUT PARAMETER rundung   AS INT.
DEF OUTPUT PARAMETER p-1118 AS DATE.

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
bill-date = htparam.fdate.

FIND FIRST htparam WHERE paramnr = 491 NO-LOCK. 
rundung = htparam.finteger. 
rundung = 2.

RUN htpdate.p (1118, OUTPUT p-1118).
