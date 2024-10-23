
DEF INPUT PARAMETER cost-acct AS CHAR.
DEF OUTPUT PARAMETER avail-gl-acct AS LOGICAL.
DEF OUTPUT PARAMETER err AS INT INIT 0.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = cost-acct NO-LOCK NO-ERROR. 
IF NOT AVAILABLE gl-acct THEN avail-gl-acct = NO.
ELSE avail-gl-acct = YES.
/*
IF NOT AVAILABLE gl-acct THEN avail-gl-acct = NO.
ELSE IF AVAILABLE gl-acct /*AND gl-acct.acc-type NE 2 AND gl-acct.acc-type NE 5*/ THEN
    ASSIGN
    avail-gl-acct = YES
    err = 1.
ELSE avail-gl-acct = YES.
*/
