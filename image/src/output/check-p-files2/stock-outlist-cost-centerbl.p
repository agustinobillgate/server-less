
DEF INPUT PARAMETER cost-center AS CHAR.
DEF OUTPUT PARAMETER fibukonto AS CHAR.
DEF OUTPUT PARAMETER bezeich AS CHAR.
DEF OUTPUT PARAMETER avail-gl-acct AS LOGICAL INIT NO.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = cost-center NO-LOCK NO-ERROR.
IF AVAILABLE gl-acct THEN
DO:
    avail-gl-acct = YES.
    fibukonto = gl-acct.fibukonto.
    bezeich = gl-acct.bezeich.
END.
