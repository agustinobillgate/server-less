
DEF INPUT PARAMETER curr-select AS CHAR.
DEF INPUT PARAMETER maintask-number1 AS INT.
DEF OUTPUT PARAMETER avail-queasy AS LOGICAL INIT NO.

DEFINE BUFFER queasy1 FOR queasy.

IF curr-select = "chg" THEN
find first queasy1 where queasy1.number1 = maintask-number1
    and queasy1.number2 = 0 and queasy1.deci2 = 0
    and queasy1.key = 133 AND ROWID(queasy1) NE ROWID(queasy) no-lock no-error.
ELSE IF curr-select = "add" THEN
find first queasy1 where queasy1.number1 = maintask-number1
    and queasy1.number2 = 0 and queasy1.deci2 = 0
    and queasy1.key = 133 no-lock no-error.
if available queasy1 THEN avail-queasy = YES.
