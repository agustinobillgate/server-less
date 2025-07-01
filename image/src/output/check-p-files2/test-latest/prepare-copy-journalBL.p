
DEF OUTPUT PARAMETER last-acctdate AS DATE.
DEF OUTPUT PARAMETER datum AS DATE.
DEF OUTPUT PARAMETER fl-temp AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER finteger AS INTEGER.

FIND FIRST htparam WHERE paramnr = 558 no-lock.   /* LAST Acct Period */ 
last-acctdate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 372 NO-LOCK. 
datum = htparam.fdate.


FIND FIRST htparam WHERE htparam.paramnr = 1012 NO-LOCK.
IF htparam.paramgr = 38 AND htparam.feldtyp = 1 AND htparam.finteger GT 0 THEN
DO:
    fl-temp = YES.
    finteger = htparam.finteger.
END.
