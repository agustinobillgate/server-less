
DEF INPUT  PARAMETER fibukonto AS CHAR.
DEF OUTPUT PARAMETER do-it     AS LOGICAL INIT NO.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibukonto NO-LOCK NO-ERROR. 
IF NOT AVAILABLE gl-acct AND INTEGER(fibukonto) NE 0 THEN 
    do-it = YES.

