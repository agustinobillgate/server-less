
DEF INPUT  PARAMETER lscheinnr      AS CHAR.
DEF INPUT  PARAMETER cost-acct      AS CHAR.
DEF OUTPUT PARAMETER cost-center    AS CHAR.
DEF OUTPUT PARAMETER avail-gl-acct  AS LOGICAL INIT NO.

FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = lscheinnr 
    AND l-ophdr.op-typ = "REQ" NO-LOCK NO-ERROR. 
FIND FIRST gl-acct WHERE gl-acct.fibukonto = cost-acct NO-LOCK NO-ERROR. 
IF AVAILABLE gl-acct THEN 
    ASSIGN
        cost-center = gl-acct.bezeich
        avail-gl-acct = YES.

