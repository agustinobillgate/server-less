
DEF OUTPUT PARAMETER long-stay AS INTEGER.
DEF OUTPUT PARAMETER curr-date AS DATE.

FIND FIRST htparam WHERE htparam.paramnr = 139 NO-LOCK.
long-stay = htparam.finteger.

IF long-stay = 0 THEN RETURN.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
curr-date = htparam.fdate.
