
DEF INPUT PARAMETER c-list-s-recid AS INT.
DEF OUTPUT PARAMETER successFlag AS LOGICAL.

FIND FIRST h-compli WHERE RECID(h-compli) = c-list-s-recid 
EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE h-compli THEN
DO:
    DELETE h-compli.
    ASSIGN successFlag = YES.
END.
ELSE ASSIGN successFlag = NO.
