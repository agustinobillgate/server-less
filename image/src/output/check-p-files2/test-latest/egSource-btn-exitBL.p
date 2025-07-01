DEFINE TEMP-TABLE source LIKE queasy.


DEFINE BUFFER queri FOR queasy.

DEF INPUT PARAMETER TABLE FOR source.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

FIND FIRST source.
IF case-type = 1 THEN   /*MT add */
DO :
    FIND FIRST queri WHERE queri.number1 = SOURCE.number1 AND queri.KEY = 130 NO-LOCK NO-ERROR.
    IF AVAILABLE queri THEN
    DO:
        fl-code = 1.
        RETURN NO-APPLY.
    END.
    ELSE
    DO:
        FIND FIRST queri WHERE queri.char1 = SOURCE.char1 AND queri.KEY = 130 NO-LOCK NO-ERROR.
        IF AVAILABLE queri THEN
        DO:
            fl-code = 2.
            RETURN NO-APPLY.
        END.
        ELSE
        DO:
            CREATE  queasy.  
            RUN fill-new-queasy.
            fl-code = 3.
        END.
    END.
END.
ELSE IF case-type = 2 THEN   /*MT chg */
DO:
  FIND FIRST queasy WHERE RECID(queasy) = rec-id.
  FIND FIRST queri WHERE queri.number1 = source.number1 AND queri.number2 = 0 AND queri.deci2 = 0  
    AND queri.key = 130 AND ROWID(queri) NE ROWID(queasy) NO-LOCK NO-ERROR.
  IF AVAILABLE queri THEN
  DO:
    fl-code = 1.
    RETURN NO-APPLY.
  END.
  ELSE
  DO:
    FIND FIRST queri WHERE queri.char1 = source.char1 AND queri.number2 = 0 AND queri.deci2 = 0  
        AND queri.key = 130 AND ROWID(queri) NE ROWID(queasy) NO-LOCK NO-ERROR.
    IF AVAILABLE queri THEN
    DO:
        fl-code = 2.
        RETURN NO-APPLY.
    END.
    ELSE
    DO:
    
      FIND CURRENT queasy EXCLUSIVE-LOCK.  
      queasy.number1 = source.number1.
      queasy.char1 = source.char1.  
      FIND CURRENT queasy NO-LOCK .
      fl-code = 3.
    END.  
  END.
END.

PROCEDURE fill-new-queasy:  
  queasy.KEY = 130.  
  queasy.number1 = source.number1.  
  queasy.char1 = source.char1.  
END.  
