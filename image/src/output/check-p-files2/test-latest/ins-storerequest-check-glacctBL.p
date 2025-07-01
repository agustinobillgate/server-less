
DEF INPUT  PARAMETER t-fibu         AS CHAR.
DEF OUTPUT PARAMETER avail-gl-acct  AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER gl-bezeich     AS CHAR.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = t-fibu NO-LOCK NO-ERROR. 
IF AVAILABLE gl-acct THEN 
    ASSIGN
        avail-gl-acct = YES
        gl-bezeich = gl-acct.bezeich.
