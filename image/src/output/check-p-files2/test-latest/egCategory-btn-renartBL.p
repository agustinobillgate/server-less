
DEF INPUT PARAMETER category-number1 AS INT.
DEF OUTPUT PARAMETER fl-code AS LOGICAL INIT NO.

FIND FIRST eg-Request WHERE eg-Request.category = category-number1 NO-LOCK NO-ERROR.
IF AVAILABLE eg-Request THEN fl-code = YES.
