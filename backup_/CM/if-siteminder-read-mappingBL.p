
DEF INPUT  PARAMETER icase  AS INT.
DEF INPUT  PARAMETER p-char AS CHAR.
DEF OUTPUT PARAMETER n-char AS CHAR.

n-char = p-char.
IF icase EQ 1 THEN  /*get currency*/
DO:
    FIND FIRST queasy WHERE queasy.KEY = 164 AND queasy.char2 NE "" AND queasy.char2 = p-char
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN n-char = queasy.char1.
END.
ELSE                /*get nation*/
DO:
    FIND FIRST queasy WHERE queasy.KEY = 165 AND queasy.char2 NE "" AND queasy.char2 = p-char
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN n-char = queasy.char1.
END.
