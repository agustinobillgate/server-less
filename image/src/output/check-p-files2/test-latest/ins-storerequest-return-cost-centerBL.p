
DEF INPUT  PARAMETER cost-center        AS CHAR.
DEF OUTPUT PARAMETER avail-glacct       AS LOGICAL INIT YES.
DEF OUTPUT PARAMETER gl-acct-fibukonto  AS CHAR.

FIND FIRST gl-acct WHERE gl-acct.bezeich = cost-center 
    AND gl-acct.activeflag NO-LOCK NO-ERROR. 
IF NOT AVAILABLE gl-acct OR TRIM(cost-center) = "" THEN
    avail-glacct = NO.
ELSE
DO:
    gl-acct-fibukonto = gl-acct.fibukonto.
END.
