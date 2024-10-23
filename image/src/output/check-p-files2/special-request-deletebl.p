
DEF INPUT  PARAMETER number1        AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER msg-str        AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER success-flag   AS LOGICAL NO-UNDO INIT NO.

FIND FIRST queasy WHERE queasy.KEY = 189 AND queasy.number1 = number1 
    EXCLUSIVE-LOCK. 
DELETE queasy. 
success-flag = YES.
 
