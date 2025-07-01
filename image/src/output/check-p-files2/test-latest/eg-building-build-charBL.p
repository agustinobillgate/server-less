
DEF INPUT PARAMETER curr-select AS CHAR.
DEF INPUT PARAMETER build-char1 AS CHAR.
DEF OUTPUT PARAMETER avail-queasy AS LOGICAL INIT NO.

DEFINE BUFFER queasy1 FOR queasy.  

IF curr-select = "chg" THEN
    FIND FIRST queasy1 WHERE queasy1.char1 = build-char1   
    AND queasy1.number2 = 0 AND queasy1.deci2 = 0  
    AND queasy1.key = 135 AND ROWID(queasy1) NE ROWID(queasy)
    NO-LOCK NO-ERROR.
ELSE IF curr-select = "add" THEN
    FIND FIRST queasy1 WHERE queasy1.char1 = build-char1   
    AND queasy1.number2 = 0 AND queasy1.deci2 = 0  
    AND queasy1.KEY = 135 NO-LOCK NO-ERROR.  

if available queasy1 THEN avail-queasy = YES.
