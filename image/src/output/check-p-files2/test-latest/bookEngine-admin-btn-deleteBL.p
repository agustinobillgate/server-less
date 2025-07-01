
DEF INPUT  PARAMETER number1 AS INT.

FIND FIRST queasy WHERE queasy.KEY = 159
    AND queasy.number1 = number1 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    FIND CURRENT queasy EXCLUSIVE-LOCK.
    DELETE queasy.
    RELEASE queasy.
END.
