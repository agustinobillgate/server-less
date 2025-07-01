
DEF INPUT  PARAMETER cost-center AS CHAR.
DEF OUTPUT PARAMETER g-fibukonto AS CHAR INIT "".

FIND FIRST gl-acct WHERE gl-acct.bezeich = cost-center 
    AND gl-acct.activeflag NO-LOCK NO-ERROR. 
IF NOT AVAILABLE gl-acct OR TRIM(cost-center) = "" THEN RETURN NO-APPLY.

g-fibukonto = gl-acct.fibukonto. 
