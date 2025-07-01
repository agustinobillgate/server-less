
DEF INPUT PARAMETER curr-select AS CHAR.
DEF INPUT PARAMETER category-number1 AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER avail-queasy AS LOGICAL INIT NO.

FIND FIRST queasy WHERE RECID(queasy) = rec-id.
DEFINE BUFFER queasy1 FOR queasy.

IF curr-select = "chg" THEN
find first queasy1 where queasy1.number1 = category-number1
  and queasy1.number2 = 0 and queasy1.deci2 = 0  
  and queasy1.key = 132 AND ROWID(queasy1) NE ROWID(queasy)
  no-lock no-error.  
ELSE IF curr-select = "add" THEN
find first queasy1 where queasy1.number1 = category-number1
  and queasy1.number2 = 0 and queasy1.deci2 = 0  
  and queasy1.key = 132 no-lock no-error.
IF AVAILABLE queasy1 THEN avail-queasy = YES.
