

DEF INPUT PARAMETER curr-select AS CHAR.
DEF INPUT PARAMETER category-char1 AS CHAR.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER avail-queasy AS LOGICAL INIT NO.

DEFINE BUFFER queasy1 FOR queasy.

FIND FIRST queasy WHERE RECID(queasy) = rec-id.

IF curr-select = "chg" THEN
FIND FIRST queasy1 WHERE queasy1.char1 = category-char1   
    AND queasy1.number2 = 0 AND queasy1.deci2 = 0  
    AND queasy1.key = 132 AND ROWID(queasy1) NE ROWID(queasy)
    NO-LOCK NO-ERROR.
ELSE IF curr-select = "add" THEN
FIND FIRST queasy1 WHERE queasy1.char1 = category-char1   
    AND queasy1.number2 = 0 AND queasy1.deci2 = 0  
    AND queasy1.KEY = 132 NO-LOCK NO-ERROR.  
IF AVAILABLE queasy1 THEN avail-queasy = YES.
