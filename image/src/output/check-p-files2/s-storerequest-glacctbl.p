
DEF INPUT PARAMETER acct AS CHAR.
DEF OUTPUT PARAMETER a-bez AS CHAR.
DEF OUTPUT PARAMETER a-fibu AS CHAR.
DEF OUTPUT PARAMETER avail-gl-acct AS LOGICAL INIT NO.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = acct NO-LOCK NO-ERROR.
IF AVAILABLE gl-acct THEN
DO:
   avail-gl-acct = YES.
   a-bez = gl-acct.bezeich.
   a-fibu = gl-acct.fibukonto.
END.
