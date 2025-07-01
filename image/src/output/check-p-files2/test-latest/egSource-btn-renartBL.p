
DEF INPUT PARAMETER source-number1 AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

FIND FIRST eg-Request WHERE eg-Request.SOURCE = source-number1 NO-LOCK NO-ERROR.
IF AVAILABLE eg-Request THEN fl-code = 1.
