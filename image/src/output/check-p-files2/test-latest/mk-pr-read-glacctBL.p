
DEF INPUT  PARAMETER acct     AS CHAR.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = acct NO-LOCK.
IF gl-acct.acc-type EQ 1 THEN 
    err-code = 1.
