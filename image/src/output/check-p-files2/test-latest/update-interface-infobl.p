DEFINE INPUT PARAMETER userSession AS CHAR.
DEFINE INPUT PARAMETER body AS CHAR.

FIND LAST queasy WHERE 
  queasy.KEY EQ 999 AND
  queasy.char1 EQ userSession AND
  queasy.logi1 EQ FALSE NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
  CREATE queasy.
  queasy.KEY = 999.
  queasy.char1 = userSession.
END.
  
IF body NE "" THEN
DO:
    IF body MATCHES "*ifStart*" THEN
    DO:
        queasy.logi1 = FALSE.
        queasy.date1 = TODAY.   
        queasy.number1 = TIME.
        queasy.char2 = body.
    END.
    ELSE
    DO:
        queasy.date1 = TODAY.   
        queasy.number1 = TIME.
        queasy.char2 = body.
        queasy.logi1 = TRUE.
    END.
END.


