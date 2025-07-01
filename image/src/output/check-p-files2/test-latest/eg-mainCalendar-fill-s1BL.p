
DEF INPUT PARAMETER awal AS DATE.
DEF INPUT PARAMETER akhir AS DATE.
DEF OUTPUT PARAMETER flag AS LOGICAL INIT NO.

FIND FIRST eg-maintain WHERE eg-maintain.estworkdate >= awal 
    AND eg-maintain.estworkdate <= akhir 
    AND eg-maintain.delete-flag = NO 
    OR eg-maintain.workdate >= awal 
    AND eg-maintain.workdate <= akhir 
    AND eg-maintain.delete-flag = NO NO-LOCK NO-ERROR.
IF AVAILABLE eg-maintain THEN flag = YES.
