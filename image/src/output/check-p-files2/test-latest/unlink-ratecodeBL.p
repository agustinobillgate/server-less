DEF INPUT PARAMETER child-code   AS CHAR    NO-UNDO.
DEF INPUT PARAMETER tb1-char3    AS CHAR    NO-UNDO.

FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = child-code.
ASSIGN queasy.char3 = tb1-char3.
FIND CURRENT queasy NO-LOCK.
