
DEF INPUT PARAMETER acct AS CHAR.
DEF OUTPUT PARAMETER avail-gl-acct AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER a-bez AS CHAR.
DEF OUTPUT PARAMETER a-main-nr AS INT.
DEF OUTPUT PARAMETER p-933 AS INT.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = acct NO-LOCK NO-ERROR.
IF AVAILABLE gl-acct THEN
DO:
    avail-gl-acct = YES.
    a-bez = gl-acct.bezeich.
    a-main-nr = gl-acct.main-nr.
    FIND FIRST htparam WHERE paramnr = 933 NO-LOCK.
    p-933 = htparam.finteger.
END.
