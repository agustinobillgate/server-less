DEFINE TEMP-TABLE margt-list   LIKE prmarket.
DEFINE TEMP-TABLE mrmcat-list  LIKE prmarket.

DEF INPUT PARAMETER TABLE FOR margt-list.
DEF INPUT PARAMETER TABLE FOR mrmcat-list.
DEF INPUT PARAMETER market-bezeich AS CHAR.
DEF INPUT PARAMETER fix-rate AS LOGICAL.
DEF INPUT PARAMETER curr-sen AS LOGICAL.
DEF INPUT PARAMETER s AS CHAR.
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER nr AS INT.

FIND FIRST prmarket WHERE prmarket.nr = nr NO-LOCK NO-ERROR. 
IF AVAILABLE prmarket THEN /*FT serverless*/
DO:
    FIND CURRENT prmarket EXCLUSIVE-LOCK.
    prmarket.bezeich = market-bezeich. 
    FIND CURRENT prmarket NO-LOCK. 
    RELEASE prmarket.

    FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 = nr 
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        queasy.logi3 = fix-rate. 
        IF curr-sen THEN queasy.char3 = s. 
        FIND CURRENT queasy NO-LOCK. 
        RELEASE queasy.
    END.
    RUN update-array. 
END.
/*
DEF VAR a AS INT.
DEF VAR b AS INT.
FOR EACH mrmcat-list:
    a = a + 1.
END.
FOR EACH margt-list:
    b = b + 1.
END.

DISP a b.
*/


PROCEDURE update-array: 
DEFINE VARIABLE i AS INTEGER. 
  FIND FIRST prtable WHERE RECID(prtable) = rec-id NO-LOCK NO-ERROR.
  IF AVAILABLE prtable THEN /*FT serverless*/
  DO:
    FIND CURRENT prtable EXCLUSIVE-LOCK.
    DO i = 1 TO 99: 
      prtable.zikatnr[i] = 0. 
      prtable.argtnr[i] = 0. 
    END.
    
    i = 0. 
    FOR EACH mrmcat-list: 
      i = i + 1. 
      prtable.zikatnr[i] = mrmcat-list.nr. 
    END. 
    i = 0. 
    FOR EACH margt-list: 
      i = i + 1. 
      prtable.argtnr[i] = margt-list.nr.
        /*MESSAGE prtable.argtnr[i] margt-list.bezeich
            VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
    END. 
    FIND CURRENT prtable NO-LOCK. 
    RELEASE prtable.
  END.              
END. 
