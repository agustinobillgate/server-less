
DEF INPUT PARAMETER cost-center AS CHAR.
DEF OUTPUT PARAMETER a-fibu AS CHAR.
DEF OUTPUT PARAMETER avail-gl-acct AS LOGICAL INIT NO.

FIND FIRST gl-acct WHERE gl-acct.bezeich = cost-center 
    AND gl-acct.activeflag NO-LOCK NO-ERROR.
IF AVAILABLE gl-acct THEN 
DO:
    a-fibu = gl-acct.fibukonto.
    avail-gl-acct = YES.
END.
    
