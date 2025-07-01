
DEF INPUT  PARAMETER curr-select    AS CHAR.
DEF INPUT  PARAMETER source-number1 AS INT.
DEF OUTPUT PARAMETER err-code       AS INT INIT 0.

DEFINE BUFFER queasy1 FOR queasy.

IF curr-select = "chg" THEN
FIND FIRST queasy1 WHERE queasy1.number1 = source-number1
    AND queasy1.number2 = 0 AND queasy1.deci2 = 0
    AND queasy1.KEY = 130 AND ROWID(queasy1) NE ROWID(queasy)
    NO-LOCK NO-ERROR.
ELSE IF curr-select = "add" THEN
FIND FIRST queasy1 WHERE queasy1.number1 = source-number1
    AND queasy1.number2 = 0 AND queasy1.deci2 = 0
    AND queasy1.key = 130 NO-LOCK NO-ERROR.

IF AVAILABLE queasy1 THEN err-code = 1.
