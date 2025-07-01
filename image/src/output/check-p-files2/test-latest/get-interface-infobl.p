DEFINE INPUT PARAMETER userSession AS CHAR.
DEFINE OUTPUT PARAMETER data AS CHAR INIT ?.
DEFINE OUTPUT PARAMETER finishFlag AS LOGICAL INIT ?.

FIND LAST queasy WHERE 
  queasy.KEY EQ 999 AND
  queasy.char1 EQ userSession NO-ERROR.

IF AVAILABLE queasy THEN
DO:
  finishFlag = queasy.logi1.
  data = queasy.char2.

  IF finishFlag THEN
  DO:
    DELETE queasy.
  END.
END.


