DEF INPUT PARAMETER docu-nr AS CHAR.
DEF INPUT PARAMETER flag AS INT.

FIND FIRST gc-pi WHERE gc-pi.docu-nr = docu-nr EXCLUSIVE-LOCK.
IF flag = 1 THEN
    ASSIGN gc-pi.printed1 = YES.
ELSE IF flag = 2 THEN
    ASSIGN gc-pi.printed1A = YES.
FIND CURRENT gc-pi NO-LOCK.
