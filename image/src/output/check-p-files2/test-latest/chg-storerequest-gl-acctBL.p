
DEF INPUT PARAMETER acct AS CHAR.
DEF OUTPUT PARAMETER t-desc AS CHAR.
DEF OUTPUT PARAMETER avail-gl-acct AS LOGICAL INIT NO.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = acct NO-LOCK NO-ERROR. 
IF AVAILABLE gl-acct THEN 
    ASSIGN
        avail-gl-acct = YES
        t-desc = gl-acct.bezeich.
