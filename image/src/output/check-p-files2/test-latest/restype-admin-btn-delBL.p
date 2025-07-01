
DEF INPUT  PARAMETER source-code  AS INTEGER.
DEF OUTPUT PARAMETER flag         AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST reservation WHERE 
  reservation.resart = source-code NO-LOCK NO-ERROR. 
IF AVAILABLE reservation THEN
  flag = YES.
ELSE 
DO: 
    FIND FIRST sourccod WHERE sourccod.source-code = source-code EXCLUSIVE-LOCK.
    DELETE sourccod.
    success-flag = YES.
END.
