
DEFINE INPUT PARAMETER dept AS INTEGER.
DEFINE INPUT PARAMETER subgrup-no AS INTEGER.
DEFINE INPUT PARAMETER subgrup AS CHARACTER.
DEFINE INPUT PARAMETER maingrup-no AS INTEGER.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

FIND FIRST queasy WHERE queasy.KEY EQ 229
  AND queasy.number1 EQ subgrup-no
  AND queasy.number2 EQ dept NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
  CREATE queasy.
  ASSIGN
    queasy.KEY      = 229
    queasy.number1  = subgrup-no
    queasy.number2  = dept
    queasy.number3  = maingrup-no
    queasy.char1    = subgrup    
  .
  success-flag    = YES.
END.
ELSE
DO:
  FIND CURRENT queasy EXCLUSIVE-LOCK.
  ASSIGN queasy.number3  = maingrup-no
  success-flag = YES.
  FIND CURRENT queasy NO-LOCK.
END.
